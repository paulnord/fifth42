#include "exact.hpp"
#include <array>
#include <iostream>
#include <random>
#include <string>
#include <vector>

void emit(I192 n) { std::cout << '[' << n.lo << ',' << n.hi.lo << ',' << n.hi.hi << ']'; }

int main(int argc, char** argv) {
    if (argc > 1 && std::string(argv[1]) == "--native-extremes") {
        const int points[] = {-MAX_BOUND, -MAX_BOUND+1, 0, MAX_BOUND-1, MAX_BOUND};
        for (int a : points) for (int b : points) for (int z : points)
            for (std::int64_t target : std::array<std::int64_t,3>{42, INT64_MIN, INT64_MAX}) {
                const I192 pair = fifth(a) + fifth(b);
                const I192 goal = residual(target,z);
                const I192 total = pair + fifth(z);
                std::cout << a << ' ' << b << ' ' << z << ' ' << target << ' ';
                emit(pack(pair)); std::cout << ' '; emit(pack(goal));
                std::cout << ' '; emit(pack(total)); std::cout << '\n';
            }
        return 0;
    }
    if (argc > 1) {
        for (int n : {0, 1, -1, 6208, -6208, 6209, -6209, 100000, -100000,
                      10000000, -10000000, 44275338, -44275338, 44275339, -44275339, 70000000, -70000000, MAX_BOUND-1, -MAX_BOUND+1, MAX_BOUND, -MAX_BOUND}) {
            std::cout << n << ' '; emit(pack(fifth(n))); std::cout << '\n';
        }
        return 0;
    }
    std::vector<I192> v;
    for (int n : {0, 1, -1, 6208, -6208, 6209, -6209, 100000, -100000,
                  10000000, -10000000, 44275338, -44275338, 44275339, -44275339, 70000000, -70000000, MAX_BOUND-1, -MAX_BOUND+1, MAX_BOUND, -MAX_BOUND})
        v.push_back(pack(fifth(n)));
    for (int bit : {0, 31, 32, 63, 64, 65, 117, 118, 125, 126}) {
        const __int128 n = static_cast<__int128>(1) << bit;
        v.push_back(pack(n - 1));
        v.push_back(pack(n));
        v.push_back(pack(-n));
    }
    // Include sign boundary and minimum value; Python checks modulo-2^128 rules.
    v.push_back({UINT64_MAX, Upper128{UINT64_MAX,(UINT64_C(1)<<63)-1}});
    v.push_back({0, Upper128{0,UINT64_C(1)<<63}});
    std::mt19937_64 rng(42);
    for (int i = 0; i < 64; ++i) v.push_back({rng(), Upper128{rng(),rng()}});
    for (auto a : v) for (auto b : v) {
        emit(a); std::cout << ' '; emit(b); std::cout << ' ';
        emit(a+b); std::cout << ' '; emit(-a);
        std::cout << ' ' << (a < b) << ' ' << (a == b) << '\n';
    }
}
