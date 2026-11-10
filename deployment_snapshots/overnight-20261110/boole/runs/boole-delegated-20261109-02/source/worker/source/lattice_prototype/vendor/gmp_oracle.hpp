#pragma once
#include "exact.hpp"
#include <gmpxx.h>
inline mpz_class arbitrary(I192 n) {
    const std::uint64_t words[]{n.lo,n.hi.lo,n.hi.hi};
    mpz_class out;
    mpz_import(out.get_mpz_t(),3,-1,sizeof(words[0]),0,0,words);
    if(n.hi.hi>>63)out-=(mpz_class{1}<<192);
    return out;
}
inline I192 from_arbitrary(const mpz_class& n) {
    mpz_class u;
    mpz_fdiv_r_2exp(u.get_mpz_t(),n.get_mpz_t(),192);
    std::uint64_t words[3]{};std::size_t count=0;
    mpz_export(words,&count,-1,sizeof(words[0]),0,0,u.get_mpz_t());
    return {words[0],Upper128{words[1],words[2]}};
}
inline mpz_class arbitrary_fifth(int n) {
    mpz_class x{n};mpz_pow_ui(x.get_mpz_t(),x.get_mpz_t(),5);return x;
}
