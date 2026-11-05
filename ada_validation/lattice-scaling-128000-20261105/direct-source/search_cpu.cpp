#include "search_common.hpp"

int main(int argc, char** argv) {
    try {
        const auto setup = Clock::now();
        auto o = parse_options(argc, argv);
        check_rows(o);
        const auto t = make_table(o);
        std::vector<Hit> hits;
        std::uint64_t steps = 0;
        const double setup_seconds = seconds_since(setup);
        const auto begin = Clock::now();
        for (long long row = o.start; row < o.stop; ++row) {
            const int z = row_z(o, static_cast<std::size_t>(row));
            // Native signed 128-bit CPU search, independent of GPU limb compare/add.
            const __int128 goal = static_cast<__int128>(o.target) - fifth(z);
            long long i = 0, j = static_cast<long long>(t.xs.size()) - 1;
            while (i <= j) {
                const __int128 s = t.powers[static_cast<std::size_t>(i)]
                                 + t.powers[static_cast<std::size_t>(j)];
                ++steps;
                if (s < goal) ++i;
                else if (s > goal) --j;
                else {
                    if (hits.size() == o.capacity) throw std::runtime_error("hit buffer full; no coverage emitted");
                    hits.push_back({t.xs[static_cast<std::size_t>(i)], t.xs[static_cast<std::size_t>(j)], z});
                    ++i;
                    --j;
                }
            }
        }
        std::sort(hits.begin(), hits.end(), hit_less);
        print_result("cpu", o, t, hits, steps, seconds_since(begin), setup_seconds);
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
