#include "row_search.hpp"
#include <iostream>
#include <random>
#include <vector>

void emit(I192 a) { std::cout << '[' << a.lo << ',' << a.hi.lo << ',' << a.hi.hi << ']'; }
int main() {
    std::vector<I192> v{{0,0},{1,0},{UINT64_MAX,0},{0,1},{UINT64_MAX,UINT64_MAX},
        {0,UINT64_MAX},{0,UINT64_C(1)<<63},{UINT64_MAX,(UINT64_C(1)<<63)-1},
        pack(fifth(MAX_BOUND)),pack(fifth(-MAX_BOUND))};
    std::mt19937_64 rng(42);
    for (int i = 0; i < 64; ++i) v.push_back({rng(),Upper128{rng(),rng()}});
    std::size_t count = 0;
    for (auto a : v) for (auto b : v) {
        const I192 sum = a+b;
        for (auto goal : {sum,sum+I192{1,0},sum+(-I192{1,0}),v[(count++)%v.size()]}) {
            const std::uint64_t lows[]{a.lo,b.lo};
            const int c = compare_high_first(SplitPowers{lows,nullptr},0,1,a.hi,b.hi,goal);
            emit(a); std::cout << ' '; emit(b); std::cout << ' '; emit(goal);
            std::cout << ' ' << c << '\n';
        }
    }
}
