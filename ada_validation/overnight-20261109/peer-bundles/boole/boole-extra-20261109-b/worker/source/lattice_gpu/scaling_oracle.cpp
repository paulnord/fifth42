// Independent exact positive-domain oracle. No lattice or modular filters.
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Wide = __int128;
struct Hit { int a, b, c; long long residual; };

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: near-oracle BOUND CAP");
        std::size_t used = 0;
        const long long parsed = std::stoll(argv[1], &used);
        if (used != std::string(argv[1]).size() || parsed < 1 || parsed > 32000)
            throw std::runtime_error("bound outside [1,32000]");
        const auto cap = std::stoll(argv[2], &used);
        if (used != std::string(argv[2]).size() || cap < 0 || cap > 1000000)
            throw std::runtime_error("cap outside [0,1000000]");
        const int bound = static_cast<int>(parsed);
        const auto start = std::chrono::steady_clock::now();
        // 3*32000^5 < 2^127; every power and residual is exact.
        std::vector<Wide> powers(static_cast<std::size_t>(bound + 1));
        for (int n = 0; n <= bound; ++n) {
            Wide p = 1;
            for (int k = 0; k < 5; ++k) p *= n;
            powers[static_cast<std::size_t>(n)] = p;
        }
        std::vector<Hit> hits;
        std::uint64_t pairs = 0;
        for (int c = 2; c <= bound; ++c) {
            int upper = c - 1;
            for (int a = 1; a < c; ++a) {
                const Wide base = powers[static_cast<std::size_t>(a)] - powers[static_cast<std::size_t>(c)];
                while (upper >= a && base + powers[static_cast<std::size_t>(upper)] > cap) {
                    --upper;
                    ++pairs;
                }
                if (upper < a) break;
                ++pairs;
                for (int b = upper; b >= a; --b) {
                    const Wide residual = base + powers[static_cast<std::size_t>(b)];
                    if (residual < -cap) break;
                    if (hits.size() >= 1000000) throw std::runtime_error("hit capacity exhausted");
                    hits.push_back({a, b, c, static_cast<long long>(residual)});
                }
            }
        }
        const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout << std::setprecision(17) << "{\"complete\":true,\"bound\":" << bound
                  << ",\"cap\":" << cap << ",\"domain\":\"1 <= a <= b < c <= bound\""
                  << ",\"arithmetic_bits\":128,\"pair_steps\":" << pairs
                  << ",\"seconds\":" << elapsed << ",\"hits\":[";
        for (std::size_t i = 0; i < hits.size(); ++i) {
            if (i) std::cout << ',';
            const auto h = hits[i];
            std::cout << '[' << h.a << ',' << h.b << ',' << h.c << ',' << h.residual << ']';
        }
        std::cout << "]}\n";
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 2;
    }
}
