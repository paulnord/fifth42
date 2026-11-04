#pragma once
#include <cstdint>
#ifdef __CUDACC__
#define HD __host__ __device__
#else
#define HD
#endif
struct Upper128 {
    std::uint64_t lo,hi;
    HD Upper128(std::uint64_t l=0,std::uint64_t h=0):lo(l),hi(h) {}
    HD Upper128 operator+(Upper128 b) const {
        const auto l=lo+b.lo;
        return {l,hi+b.hi+static_cast<std::uint64_t>(l<lo)};
    }
    HD bool operator==(Upper128 b) const {return lo==b.lo&&hi==b.hi;}
    HD bool operator<(Upper128 b) const {
        const auto sign=UINT64_C(1)<<63;
        return hi==b.hi?lo<b.lo:(hi^sign)<(b.hi^sign);
    }
};
// Signed two's-complement 192-bit value. All limb arithmetic is unsigned.
struct I192 {
    std::uint64_t lo;
    Upper128 hi;
    HD I192(std::uint64_t l=0,Upper128 h=Upper128{}):lo(l),hi(h) {}
    HD static I192 from_i64(std::int64_t n) {
        return {static_cast<std::uint64_t>(n),n<0?Upper128{UINT64_MAX,UINT64_MAX}:Upper128{}};
    }
    HD I192 operator+(I192 b) const {
        const auto l=lo+b.lo;
        return {l,hi+b.hi+Upper128{static_cast<std::uint64_t>(l<lo)}};
    }
    HD I192 operator-() const {
        const auto l=~lo+1;
        return {l,Upper128{~hi.lo,~hi.hi}+Upper128{static_cast<std::uint64_t>(l==0)}};
    }
    HD bool operator==(I192 b) const {return lo==b.lo&&hi==b.hi;}
    HD bool operator<(I192 b) const {return hi==b.hi?lo<b.lo:hi<b.hi;}
    HD I192 floor_half() const {
        const auto sign=UINT64_C(1)<<63;
        return {(lo>>1)|(hi.lo<<63),Upper128{(hi.lo>>1)|(hi.hi<<63),(hi.hi>>1)|(hi.hi&sign)}};
    }
};
static_assert(sizeof(I192)==24,"three limbs without padding");
static_assert(sizeof(Upper128)==16,"two upper limbs");
inline I192 pack(I192 n) {return n;}
inline I192 pack(__int128 n) {
    const auto u=static_cast<unsigned __int128>(n);
    return {static_cast<std::uint64_t>(u),Upper128{static_cast<std::uint64_t>(u>>64),n<0?UINT64_MAX:0}};
}
constexpr int MAX_BOUND=100000000;
// 3*B^5+2^63 < 2^191. Each limb multiplication intermediate fits uint128.
inline I192 fifth(int n) {
    const auto x=static_cast<std::uint32_t>(n<0?-static_cast<std::int64_t>(n):n);
    I192 r{1};
    for(int i=0;i<5;++i) {
        auto t=static_cast<unsigned __int128>(r.lo)*x;
        r.lo=static_cast<std::uint64_t>(t);
        auto carry=static_cast<std::uint64_t>(t>>64);
        t=static_cast<unsigned __int128>(r.hi.lo)*x+carry;
        r.hi.lo=static_cast<std::uint64_t>(t);
        carry=static_cast<std::uint64_t>(t>>64);
        t=static_cast<unsigned __int128>(r.hi.hi)*x+carry;
        r.hi.hi=static_cast<std::uint64_t>(t);
    }
    return n<0?-r:r;
}
inline I192 residual(std::int64_t target,int z) {return I192::from_i64(target)+(-fifth(z));}
