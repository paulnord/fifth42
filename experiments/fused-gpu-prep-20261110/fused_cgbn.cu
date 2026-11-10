#include <cuda_runtime.h>
#include <gmp.h>
#include "cgbn/cgbn.h"
#include "types.hpp"
#ifndef ROOT_TPI
#define ROOT_TPI 8
#endif
#include "fused_algorithm.cuh"
using Context=cgbn_context_t<ROOT_TPI>;using Env=cgbn_env_t<Context,WIDTH>;
struct Ops{
 using Num=Env::cgbn_t; Env &e;
 __device__ void set(Num&r,uint64_t v){Num a,b;cgbn_set_ui32(e,a,v>>32);cgbn_shift_left(e,b,a,32);cgbn_set_ui32(e,a,(uint32_t)v);cgbn_add(e,r,b,a);}
 __device__ void copy(Num&r,const Num&a){cgbn_set(e,r,a);}
 __device__ void add(Num&r,const Num&a,const Num&b){cgbn_add(e,r,a,b);}
 __device__ void sub(Num&r,const Num&a,const Num&b){cgbn_sub(e,r,a,b);}
 __device__ void mul(Num&r,const Num&a,const Num&b){cgbn_mul(e,r,a,b);}
 __device__ void shl(Num&r,const Num&a,unsigned b){cgbn_shift_left(e,r,a,b);}
 __device__ int cmp(const Num&a,const Num&b){return cgbn_compare(e,a,b);}
 __device__ void store(Mem*r,const Num&a){cgbn_store(e,reinterpret_cast<cgbn_mem_t<WIDTH>*>(r),a);}
};
__global__ void fused(const Input*in,Output*out,unsigned count){unsigned i=(blockIdx.x*blockDim.x+threadIdx.x)/ROOT_TPI;if(i>=count)return;Context c(cgbn_no_checks);Env e(c.env<Env>());Ops o{e};run_patch(o,in[i],out[i]);}
void launch(const Input*i,Output*o,unsigned n){fused<<<(n+BLOCK/ROOT_TPI-1)/(BLOCK/ROOT_TPI),BLOCK>>>(i,o,n);}
#include "common_host.hpp"
