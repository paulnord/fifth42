// Execute the identical shared CUDA algorithm using checked 4096-bit host arithmetic.
#include <gmpxx.h>
#include <fstream>
#include <stdexcept>
#include <iostream>
#include "types.hpp"
#define __device__
#include "fused_algorithm.cuh"
struct Ops{
 using Num=mpz_class;
 void check(const Num&r){if(r<0||mpz_sizeinbase(r.get_mpz_t(),2)>4096)throw std::runtime_error("4096bit overflow");}
 void set(Num&r,uint64_t x){r=x;check(r);} void copy(Num&r,const Num&a){r=a;check(r);}
 void add(Num&r,const Num&a,const Num&b){r=a+b;check(r);}void sub(Num&r,const Num&a,const Num&b){r=a-b;check(r);}
 void mul(Num&r,const Num&a,const Num&b){r=a*b;check(r);}void shl(Num&r,const Num&a,unsigned b){r=a<<b;check(r);}
 int cmp(const Num&a,const Num&b){return a<b?-1:(a>b?1:0);}
 void store(Mem*r,const Num&a){Num x=a;for(unsigned j=0;j<LIMBS;++j){r->_limbs[j]=static_cast<uint32_t>(x.get_ui());x>>=32;}}
};
int main(int argc,char**argv){try{if(argc!=3)throw std::runtime_error("INPUT OUTPUT");std::ifstream in(argv[1],std::ios::binary);std::ofstream out(argv[2],std::ios::binary);auto read=[&](unsigned n){uint64_t x=0;for(unsigned j=0;j<n;++j){int c=in.get();if(c<0)throw std::runtime_error("truncated");x|=uint64_t(c)<<(8*j);}return x;};auto write=[&](uint32_t x){for(int i=0;i<4;++i)out.put((x>>(8*i))&255);};unsigned count=read(4);write(count);for(unsigned i=0;i<count;++i){Input a;a.lo=read(8);a.hi=read(8);a.left=read(8);a.right=read(8);a.den=read(8);a.cap=read(8);a.bits=read(4);Output b;Ops o;run_patch(o,a,b);for(auto&v:b.value)for(auto x:v._limbs)write(x);}return 0;}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
