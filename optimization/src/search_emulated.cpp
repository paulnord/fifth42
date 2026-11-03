#include "tuning_options.hpp"

// Exercise the exact same row routines as the GPU with a CPU emitter.
// This is explicitly emulation, never evidence of GPU execution/coverage.
struct HostEmit {
    std::vector<Hit>* hits;
    const std::vector<int>* xs;
    int z;
    unsigned capacity;
    void operator()(int i, int j) const {
        if (hits->size() == capacity) throw std::runtime_error("hit buffer full; no coverage emitted");
        hits->push_back({(*xs)[static_cast<std::size_t>(i)],(*xs)[static_cast<std::size_t>(j)],z});
    }
};
int main(int argc, char** argv) {
    try {
        const auto begin_setup = Clock::now();
        const auto tuning = tuning_options(argc,argv);
        const auto o = tuning.search;
        const auto t = make_table(o);
        std::vector<I128> packed;
        std::vector<std::uint64_t> lows,highs;
        for (auto p : t.powers) {
            const auto v = pack(p);
            packed.push_back(v); lows.push_back(v.lo); highs.push_back(v.hi);
        }
        const double setup = seconds_since(begin_setup);
        const auto begin = Clock::now();
        std::vector<Hit> hits;
        unsigned long long steps = 0;
        for (auto row = o.start; row < o.stop; ++row) {
            const int z = row_z(o,static_cast<std::size_t>(row));
            const I128 goal = pack(static_cast<__int128>(o.target)-fifth(z));
            const int n = static_cast<int>(t.xs.size());
            const HostEmit emit{&hits,&t.xs,z,o.capacity};
            const PackedPowers p{packed.data()};
            if (tuning.variant == Variant::baseline) steps += baseline_row(p,n,goal,emit);
            else if (tuning.variant == Variant::cached) steps += cached_row<false>(p,n,goal,emit);
            else if (tuning.variant == Variant::pruned) steps += cached_row<true>(p,n,goal,emit);
            else steps += highword_row(SplitPowers{lows.data(),highs.data()},n,goal,emit);
        }
        std::sort(hits.begin(),hits.end(),hit_less);
        print_result("emulated",o,t,hits,steps,seconds_since(begin),setup);
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
