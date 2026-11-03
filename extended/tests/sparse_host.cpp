#include "row_search.hpp"
#include "gmp_oracle.hpp"
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>
struct Collect {
    std::vector<std::pair<int,int>>* pairs;
    void operator()(int i,int j) const {pairs->push_back({i,j});}
};
int main() {
    std::vector<int> xs{-MAX_BOUND,-70000000,-50000000,-44275339,-35,-1,0,2,35,44275339,50000000,70000000,MAX_BOUND};
    std::vector<I192> powers;
    std::vector<std::uint64_t> lows;
    std::vector<Upper128> highs;
    std::vector<mpz_class> native;
    for(int x:xs) {
        auto p=fifth(x);auto expected=arbitrary_fifth(x);
        if(arbitrary(p)!=expected)throw std::runtime_error("GMP fifth-power mismatch");
        powers.push_back(p);lows.push_back(p.lo);highs.push_back(p.hi);native.push_back(expected);
    }
    unsigned checks=0;
    const int n=static_cast<int>(xs.size());
    for(int a=0;a<n;++a)for(int b=a;b<n;++b)for(int delta:{-1,0,1}) {
        const mpz_class target=mpz_class(native[static_cast<std::size_t>(a)]+native[static_cast<std::size_t>(b)])+delta;
        const auto goal=from_arbitrary(target);
        mpz_class half;mpz_fdiv_q_2exp(half.get_mpz_t(),target.get_mpz_t(),1);
        if(arbitrary(goal.floor_half())!=half)throw std::runtime_error("floor-half/GMP mismatch");
        std::vector<std::pair<int,int>> expected;
        for(int i=0;i<n;++i)for(int j=i;j<n;++j)
            if(mpz_class(native[static_cast<std::size_t>(i)]+native[static_cast<std::size_t>(j)])==target)expected.push_back({i,j});
        for(Variant v:{Variant::baseline,Variant::cached,Variant::pruned,Variant::highword}) {
            std::vector<std::pair<int,int>> actual;Collect emit{&actual};
            const PackedPowers p{powers.data()};
            if(v==Variant::baseline)baseline_row(p,n,goal,emit);
            else if(v==Variant::cached)cached_row<false>(p,n,goal,emit);
            else if(v==Variant::pruned)cached_row<true>(p,n,goal,emit);
            else highword_row(SplitPowers{lows.data(),highs.data()},n,goal,emit);
            std::sort(actual.begin(),actual.end());
            if(actual!=expected)throw std::runtime_error("large sparse row/GMP mismatch");
            ++checks;
        }
    }
    std::cout << "{\"large_sparse_row_checks\":" << checks << ",\"status\":\"passed\"}\n";
}
