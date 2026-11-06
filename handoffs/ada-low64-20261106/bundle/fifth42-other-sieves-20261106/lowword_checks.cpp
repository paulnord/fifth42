#include "../fifth42-coordinator-overlay/src/kernel.hpp"
#include <cassert>
#include <iostream>
U64 pow5(U64 x){U64 x2=x*x;return x2*x2*x;}
bool lowpass(S64 a,S64 b,S64 c,U64 cap){return pow5(a)+pow5(b)-pow5(c)+cap<=2*cap;}
bool exactpass(S64 a,S64 b,S64 c,S64 cap){auto r=fifth64(a)+fifth64(b)+(-fifth64(c));auto lim=I192::from_i64(cap);return !(r<(-lim)||lim<r);}
int main(){assert(lowpass(13,16,17,12));assert(exactpass(13,16,17,12));assert(!lowpass(13,16,17,11));assert(!exactpass(13,16,17,11));assert(lowpass(10,2,4,99008));assert(exactpass(10,2,4,99008));
// Huge positive residual aliases to zero mod2^64, so full-width confirmation must reject.
S64 k=8192;assert(lowpass(13*k,16*k,17*k,42));assert(!exactpass(13*k,16*k,17*k,42));
// Negative alias and signed modular edge arithmetic.
assert(lowpass(-13*k,-16*k,-17*k,42));assert(!exactpass(-13*k,-16*k,-17*k,42));
assert(pow5(static_cast<U64>(-1))==~U64{0});
std::cout<<"boundary_controls_and_positive_negative_aliases_passed\n";
}
