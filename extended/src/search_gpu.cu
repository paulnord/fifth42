#include "tuning_options.hpp"
#include "gmp_oracle.hpp"
#include <cuda_runtime.h>
#include <random>

inline void checked(cudaError_t e, const char* op) {
    if (e != cudaSuccess) throw std::runtime_error(std::string(op) + ": " + cudaGetErrorString(e));
}
template<class T> struct DeviceBuffer {
    T* p = nullptr;
    explicit DeviceBuffer(std::size_t n) {
        checked(cudaMalloc(&p, std::max<std::size_t>(n, 1) * sizeof(T)), "cudaMalloc");
    }
    ~DeviceBuffer() { if (p) cudaFree(p); }
    DeviceBuffer(const DeviceBuffer&) = delete;
    DeviceBuffer& operator=(const DeviceBuffer&) = delete;
};

struct DeviceEmit {
    Hit* out;
    unsigned long long* count;
    unsigned capacity;
    int z;
    __device__ void operator()(int i, int j) const {
        const auto k = atomicAdd(count,1ULL);
        if (k < capacity) out[k] = {i,j,z};
    }
};

// Each emitted pair stores indices. Host decoding avoids a GPU allocation
// and upload of the entire x-value array, which is unused on rows without hits.
template<Variant V>
__global__ void search_rows(const I192* __restrict__ p,
                            const std::uint64_t* __restrict__ lows,
                            const Upper128* __restrict__ highs, int n,
                            const I192* __restrict__ goals, const int* __restrict__ zs, unsigned rows,
                            Hit* out, unsigned long long* count, unsigned capacity,
                            unsigned long long* row_steps) {
    const unsigned r = blockIdx.x * blockDim.x + threadIdx.x;
    if (r >= rows) return;
    const DeviceEmit emit{out,count,capacity,zs[r]};
    if constexpr (V == Variant::baseline) row_steps[r] = baseline_row(PackedPowers{p},n,goals[r],emit);
    else if constexpr (V == Variant::cached) row_steps[r] = cached_row<false>(PackedPowers{p},n,goals[r],emit);
    else if constexpr (V == Variant::pruned) row_steps[r] = cached_row<true>(PackedPowers{p},n,goals[r],emit);
    else row_steps[r] = highword_row(SplitPowers{lows,highs},n,goals[r],emit);
}

struct ArithmeticCase { I192 a, b, goal; };
struct ArithmeticResult { I192 sum, neg; int lt, eq, sum_cmp; };
__global__ void arithmetic_kernel(const ArithmeticCase* in, ArithmeticResult* out, int n) {
    const int i = static_cast<int>(blockIdx.x * blockDim.x + threadIdx.x);
    if (i < n) {
        const std::uint64_t lo[] = {in[i].a.lo,in[i].b.lo};
        const int cmp = compare_high_first(SplitPowers{lo,nullptr},0,1,in[i].a.hi,in[i].b.hi,in[i].goal);
        out[i] = {in[i].a + in[i].b, -in[i].a,
                  in[i].a < in[i].b, in[i].a == in[i].b,cmp};
    }
}
void sparse_gpu_self_test();
void arithmetic_self_test() {
    std::vector<I192> v{pack(0),pack(1),pack(-1),fifth(MAX_BOUND),fifth(-MAX_BOUND)};
    for(int bit:{63,64,127,128,130,190,191}) {
        const mpz_class n=mpz_class{1}<<bit;
        v.push_back(from_arbitrary(n));v.push_back(from_arbitrary(-n));
    }
    std::mt19937_64 rng(42);
    for (int i = 0; i < 128; ++i) {
        v.push_back(I192{rng(),Upper128{rng(),rng()}});
    }
    std::vector<ArithmeticCase> in;
    std::vector<ArithmeticResult> expect;
    for (auto a : v) for (auto b : v) {
        const auto goal = v[(in.size()*17) % v.size()];
        in.push_back({pack(a), pack(b),pack(goal)});
        const auto sum=from_arbitrary(arbitrary(a)+arbitrary(b));
        const auto cmp=mpz_cmp(arbitrary(sum).get_mpz_t(),arbitrary(goal).get_mpz_t());
        expect.push_back({sum,from_arbitrary(-arbitrary(a)),
                          arbitrary(a)<arbitrary(b),arbitrary(a)==arbitrary(b),cmp<0?-1:cmp>0?1:0});
    }
    DeviceBuffer<ArithmeticCase> d_in(in.size());
    DeviceBuffer<ArithmeticResult> d_out(in.size());
    checked(cudaMemcpy(d_in.p, in.data(), in.size()*sizeof(in[0]), cudaMemcpyHostToDevice), "self-test upload");
    arithmetic_kernel<<<static_cast<unsigned>((in.size()+127)/128), 128>>>(d_in.p, d_out.p, static_cast<int>(in.size()));
    checked(cudaGetLastError(), "self-test launch");
    std::vector<ArithmeticResult> out(in.size());
    checked(cudaMemcpy(out.data(), d_out.p, out.size()*sizeof(out[0]), cudaMemcpyDeviceToHost), "self-test download");
    for (std::size_t i = 0; i < out.size(); ++i)
        if (!(out[i].sum == expect[i].sum) || !(out[i].neg == expect[i].neg)
            || out[i].lt != expect[i].lt || out[i].eq != expect[i].eq
            || out[i].sum_cmp != expect[i].sum_cmp)
            throw std::runtime_error("GPU arithmetic self-test mismatch at " + std::to_string(i));
    sparse_gpu_self_test();
    std::cout << "{\"gpu_arithmetic_cases\":" << out.size() << ",\"gpu_sparse_large_power_rows\":\"passed\",\"status\":\"pass\"}\n";
}

#include "sparse_self_test.inc"

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            arithmetic_self_test();
            return 0;
        }
        const auto setup = Clock::now();
        const auto tuning = tuning_options(argc,argv);
        const auto o = tuning.search;
        int devices = 0;
        checked(cudaGetDeviceCount(&devices), "cudaGetDeviceCount");
        if (devices == 0) throw std::runtime_error("no CUDA devices");
        const auto t = make_table(o);
        std::vector<I192> packed;
        std::vector<std::uint64_t> lows;
        std::vector<Upper128> highs;
        if (tuning.variant == Variant::highword) {
            lows.reserve(t.powers.size()); highs.reserve(t.powers.size());
            for (auto p : t.powers) { const auto v = pack(p); lows.push_back(v.lo); highs.push_back(v.hi); }
        } else {
            packed.reserve(t.powers.size());
            for (auto p : t.powers) packed.push_back(pack(p));
        }
        const auto rows = static_cast<unsigned>(o.stop - o.start);
        std::vector<I192> goals(rows);
        std::vector<int> zs(rows);
        for (unsigned r = 0; r < rows; ++r) {
            zs[r] = row_z(o, static_cast<std::size_t>(o.start) + r);
            goals[r] = residual(o.target,zs[r]);
        }
        DeviceBuffer<I192> dp(packed.size()), dg(rows);
        DeviceBuffer<std::uint64_t> dl(lows.size());
        DeviceBuffer<Upper128> dhigh(highs.size());
        DeviceBuffer<int> dz(rows);
        DeviceBuffer<Hit> dh(o.capacity);
        DeviceBuffer<unsigned long long> dc(1), ds(rows);
        if (!packed.empty()) {
            checked(cudaMemcpy(dp.p, packed.data(), packed.size()*sizeof(I192), cudaMemcpyHostToDevice), "upload powers");
        }
        if (!lows.empty()) {
            checked(cudaMemcpy(dl.p,lows.data(),lows.size()*sizeof(lows[0]),cudaMemcpyHostToDevice),"upload low words");
            checked(cudaMemcpy(dhigh.p,highs.data(),highs.size()*sizeof(highs[0]),cudaMemcpyHostToDevice),"upload high words");
        }
        if (rows) {
            checked(cudaMemcpy(dg.p, goals.data(), rows*sizeof(I192), cudaMemcpyHostToDevice), "upload goals");
            checked(cudaMemcpy(dz.p, zs.data(), rows*sizeof(int), cudaMemcpyHostToDevice), "upload z");
        }
        checked(cudaMemset(dc.p, 0, sizeof(unsigned long long)), "clear counter");
        const double setup_seconds = seconds_since(setup);
        const auto begin = Clock::now();
        if (rows) {
            const auto blocks = (rows+static_cast<unsigned>(tuning.block_size)-1)/static_cast<unsigned>(tuning.block_size);
#define LAUNCH_VARIANT(v) search_rows<v><<<blocks,tuning.block_size>>>(dp.p,dl.p,dhigh.p,static_cast<int>(t.xs.size()),dg.p,dz.p,rows,dh.p,dc.p,o.capacity,ds.p)
            switch (tuning.variant) {
                case Variant::baseline: LAUNCH_VARIANT(Variant::baseline); break;
                case Variant::cached: LAUNCH_VARIANT(Variant::cached); break;
                case Variant::pruned: LAUNCH_VARIANT(Variant::pruned); break;
                case Variant::highword: LAUNCH_VARIANT(Variant::highword); break;
            }
#undef LAUNCH_VARIANT
            checked(cudaGetLastError(), "search launch");
        }
        checked(cudaDeviceSynchronize(), "search synchronize");
        const double search_seconds = seconds_since(begin);
        unsigned long long count = 0;
        checked(cudaMemcpy(&count, dc.p, sizeof(count), cudaMemcpyDeviceToHost), "download hit count");
        if (count > o.capacity) throw std::runtime_error("hit buffer overflow; no coverage emitted");
        std::vector<Hit> hits(static_cast<std::size_t>(count));
        if (!hits.empty()) checked(cudaMemcpy(hits.data(), dh.p, hits.size()*sizeof(Hit), cudaMemcpyDeviceToHost), "download hits");
        for (auto& h : hits) {
            if (h.a < 0 || h.b < 0 || static_cast<std::size_t>(h.a) >= t.xs.size() || static_cast<std::size_t>(h.b) >= t.xs.size())
                throw std::runtime_error("invalid hit indices returned by GPU");
            h.a = t.xs[static_cast<std::size_t>(h.a)];
            h.b = t.xs[static_cast<std::size_t>(h.b)];
        }
        std::vector<unsigned long long> rs(rows);
        if (rows) checked(cudaMemcpy(rs.data(), ds.p, rows*sizeof(rs[0]), cudaMemcpyDeviceToHost), "download step counts");
        std::uint64_t steps = 0;
        for (auto s : rs) steps += s;
        std::sort(hits.begin(), hits.end(), hit_less);
        print_result("gpu", o, t, hits, steps, search_seconds, setup_seconds);
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
