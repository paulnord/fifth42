#include "search_common.hpp"
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

// One thread owns one z row. Monotonicity of the sorted fifth powers permits
// an exact staircase through all a <= b; no floating-point root is used.
__global__ void search_rows(const I128* p, const int* xs, int n,
                            const I128* goals, const int* zs, unsigned rows,
                            Hit* out, unsigned long long* count, unsigned capacity,
                            unsigned long long* row_steps) {
    const unsigned r = blockIdx.x * blockDim.x + threadIdx.x;
    if (r >= rows) return;
    int i = 0, j = n - 1;
    unsigned long long steps = 0;
    const I128 goal = goals[r];
    while (i <= j) {
        const I128 sum = p[i] + p[j];
        ++steps;
        if (sum < goal) ++i;
        else if (goal < sum) --j;
        else {
            const auto k = atomicAdd(count, 1ULL);
            if (k < capacity) out[k] = {xs[i], xs[j], zs[r]};
            ++i;
            --j;
        }
    }
    row_steps[r] = steps;
}

struct ArithmeticCase { I128 a, b; };
struct ArithmeticResult { I128 sum, neg; int lt, eq; };
__global__ void arithmetic_kernel(const ArithmeticCase* in, ArithmeticResult* out, int n) {
    const int i = static_cast<int>(blockIdx.x * blockDim.x + threadIdx.x);
    if (i < n) out[i] = {in[i].a + in[i].b, -in[i].a,
                        in[i].a < in[i].b, in[i].a == in[i].b};
}
void arithmetic_self_test() {
    std::vector<__int128> v{0, 1, -1, static_cast<__int128>(1) << 63,
        -(static_cast<__int128>(1) << 63), static_cast<__int128>(1) << 64,
        -(static_cast<__int128>(1) << 64), fifth(MAX_BOUND), fifth(-MAX_BOUND)};
    std::mt19937_64 rng(42);
    for (int i = 0; i < 128; ++i) {
        auto n = static_cast<__int128>(rng() & ((UINT64_C(1) << 54) - 1));
        n = (n << 64) | static_cast<__int128>(rng());
        v.push_back(i % 2 ? -n : n);
    }
    std::vector<ArithmeticCase> in;
    std::vector<ArithmeticResult> expect;
    for (auto a : v) for (auto b : v) {
        in.push_back({pack(a), pack(b)});
        expect.push_back({pack(a+b), pack(-a), a < b, a == b});
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
            || out[i].lt != expect[i].lt || out[i].eq != expect[i].eq)
            throw std::runtime_error("GPU arithmetic self-test mismatch at " + std::to_string(i));
    std::cout << "{\"gpu_arithmetic_cases\":" << out.size() << ",\"status\":\"pass\"}\n";
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            arithmetic_self_test();
            return 0;
        }
        const auto setup = Clock::now();
        auto o = parse_options(argc, argv);
        check_rows(o);
        int devices = 0;
        checked(cudaGetDeviceCount(&devices), "cudaGetDeviceCount");
        if (devices == 0) throw std::runtime_error("no CUDA devices");
        const auto t = make_table(o);
        std::vector<I128> packed;
        packed.reserve(t.powers.size());
        for (auto p : t.powers) packed.push_back(pack(p));
        const auto rows = static_cast<unsigned>(o.stop - o.start);
        std::vector<I128> goals(rows);
        std::vector<int> zs(rows);
        for (unsigned r = 0; r < rows; ++r) {
            zs[r] = row_z(o, static_cast<std::size_t>(o.start) + r);
            goals[r] = pack(static_cast<__int128>(o.target) - fifth(zs[r]));
        }
        DeviceBuffer<I128> dp(t.powers.size()), dg(rows);
        DeviceBuffer<int> dx(t.xs.size()), dz(rows);
        DeviceBuffer<Hit> dh(o.capacity);
        DeviceBuffer<unsigned long long> dc(1), ds(rows);
        if (!packed.empty()) {
            checked(cudaMemcpy(dp.p, packed.data(), packed.size()*sizeof(I128), cudaMemcpyHostToDevice), "upload powers");
            checked(cudaMemcpy(dx.p, t.xs.data(), t.xs.size()*sizeof(int), cudaMemcpyHostToDevice), "upload x");
        }
        if (rows) {
            checked(cudaMemcpy(dg.p, goals.data(), rows*sizeof(I128), cudaMemcpyHostToDevice), "upload goals");
            checked(cudaMemcpy(dz.p, zs.data(), rows*sizeof(int), cudaMemcpyHostToDevice), "upload z");
        }
        checked(cudaMemset(dc.p, 0, sizeof(unsigned long long)), "clear counter");
        const double setup_seconds = seconds_since(setup);
        const auto begin = Clock::now();
        if (rows) {
            search_rows<<<(rows+127)/128, 128>>>(dp.p, dx.p, static_cast<int>(t.xs.size()), dg.p, dz.p,
                rows, dh.p, dc.p, o.capacity, ds.p);
            checked(cudaGetLastError(), "search launch");
        }
        checked(cudaDeviceSynchronize(), "search synchronize");
        const double search_seconds = seconds_since(begin);
        unsigned long long count = 0;
        checked(cudaMemcpy(&count, dc.p, sizeof(count), cudaMemcpyDeviceToHost), "download hit count");
        if (count > o.capacity) throw std::runtime_error("hit buffer overflow; no coverage emitted");
        std::vector<Hit> hits(static_cast<std::size_t>(count));
        if (!hits.empty()) checked(cudaMemcpy(hits.data(), dh.p, hits.size()*sizeof(Hit), cudaMemcpyDeviceToHost), "download hits");
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
