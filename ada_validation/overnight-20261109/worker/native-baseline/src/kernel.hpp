#pragma once
#include "../vendor/exact.hpp"
#include <cstdint>

using U64=unsigned long long;
using S64=std::int64_t;
constexpr std::uint64_t LATTICE_MAX_BASE=200000000000ULL;
constexpr std::uint64_t MAX_PACKET_POINTS=50000000;
constexpr std::uint64_t MAX_PATCH_POINTS=10000000;
constexpr unsigned MAX_TASKS=4096;
struct Task { S64 cmin,cmax,U[9]; std::uint64_t J[3],points; };
struct Chunk { unsigned task; std::uint64_t first,count; };
struct Candidate { unsigned task; std::uint64_t linear; S64 a,b,c; };
struct ArithmeticCase { S64 a,b; };
struct ArithmeticResult { I192 p,q,sum,negative,square5; int lt,eq; };
static_assert(sizeof(ArithmeticResult)==128,"arithmetic result layout");

HD inline std::uint64_t high_product(std::uint64_t a,std::uint64_t b) {
#ifdef __CUDA_ARCH__
    return __umul64hi(static_cast<U64>(a),static_cast<U64>(b));
#else
    return static_cast<std::uint64_t>((static_cast<unsigned __int128>(a)*b)>>64);
#endif
}
// Exact low 192 bits. The caller's range proof excludes discarded high bits.
HD inline I192 multiply_word(I192 a,std::uint64_t x) {
    const auto low=a.lo*x,carry=high_product(a.lo,x);
    const auto mid_product=a.hi.lo*x,mid=mid_product+carry;
    const auto next=high_product(a.hi.lo,x)+static_cast<std::uint64_t>(mid<mid_product);
    return {low,Upper128{mid,a.hi.hi*x+next}};
}
HD inline I192 fifth64(S64 x) {
    const auto m=static_cast<std::uint64_t>(x<0?-x:x);I192 value{1};
    for(int i=0;i<5;++i)value=multiply_word(value,m);
    return x<0?-value:value;
}
// Exact fifth power modulo 2^64; unsigned wraparound is intentional.
HD inline std::uint64_t fifth_low64(std::uint64_t x) {
    const auto square=x*x;return square*square*x;
}
HD inline I192 five_square(S64 x) {
    const auto m=static_cast<std::uint64_t>(x<0?-x:x);
    return multiply_word(multiply_word(I192{5},m),m);
}
HD inline ArithmeticResult arithmetic(ArithmeticCase in) {
    const auto p=fifth64(in.a),q=fifth64(in.b),sum=p+q;
    return {p,q,sum,-sum,five_square(in.a),p<q,p==q};
}
HD inline bool evaluate(const Task& t,unsigned task,std::uint64_t index,int mode,std::uint64_t cap,Candidate& out) {
    auto remainder=index;S64 n[3];
    for(int i=0;i<3;++i){const auto width=2*t.J[i]+1;n[i]=static_cast<S64>(remainder%width)-static_cast<S64>(t.J[i]);remainder/=width;}
    S64 v[3]={0,0,0};
    // Host validation proves sum_i J_i*abs(U_ij) <= INT64_MAX.
    for(int col=0;col<3;++col)for(int i=0;i<3;++i)v[col]+=n[i]*t.U[3*i+col];
    const auto c=v[0],a=v[1],b=v[2];
    if(c<t.cmin||c>t.cmax||a<1||a>b||b>=c)return false;
    // Constant-cap mode only: a true |residual|<=cap survives modulo 2^64.
    // Healy mode keeps its original wide bound and acceptance path.
    if(!mode) {
        const auto low=fifth_low64(a)+fifth_low64(b)-fifth_low64(c);
        if(low>cap && (std::uint64_t(0)-low)>cap)return false;
    }
    const auto residual=fifth64(a)+fifth64(b)+(-fifth64(c));
    const auto limit=mode?five_square(c):I192::from_i64(static_cast<S64>(cap));
    if(residual<(-limit)||limit<residual)return false;
    out={task,index,a,b,c};return true;
}
