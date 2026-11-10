// Isolated fused preparation backend using cuPQC-BigInt 0.6.0.
// SDK remains an external dependency under NVIDIA's Math SDK license.
#include <cuda_runtime.h>
#include <cstdint>
#include <gmp.h>
#include <bigint.hpp>
#ifndef ROOT_TPI
#define ROOT_TPI 8
#endif
#ifndef ROOT_SM
#define ROOT_SM 860
#endif
static_assert(ROOT_TPI==4 || ROOT_TPI==8 || ROOT_TPI==16 || ROOT_TPI==32,
              "ROOT_TPI must be 4, 8, 16 or 32");
#include "types.hpp"
using Descriptor=decltype(cupqc::BitWidth<4096>() + cupqc::SM<ROOT_SM>() +
                          cupqc::TPI<ROOT_TPI>() + cupqc::Warp());
struct Ops {
  using Num=typename Descriptor::bigint;
  __device__ void set(Num &out,uint64_t v) {
    out=Num(static_cast<uint32_t>(v));
    if(v>>32) out=out+(Num(static_cast<uint32_t>(v>>32))<<32);
  }
  __device__ void copy(Num &out,const Num &a) { out=a; }
  __device__ void add(Num &out,const Num &a,const Num &b) { out=a+b; }
  __device__ void sub(Num &out,const Num &a,const Num &b) { out=a-b; }
  __device__ void mul(Num &out,const Num &a,const Num &b) { out=a.mul_low(b); }
  __device__ void shl(Num &out,const Num &a,unsigned n) { out=a<<n; }
  __device__ int cmp(const Num &a,const Num &b) { return a.compare(b); }
  __device__ void load(Num &out,const Mem *a) { out=Num(a->_limbs); }
  __device__ void store(Mem *out,const Num &a) { a.store(out->_limbs); }
};
#include "fused_algorithm.cuh"
__global__ void fused_kernel(const Input *input,Output *output,uint32_t count) {
  const uint32_t i=(blockIdx.x*blockDim.x+threadIdx.x)/ROOT_TPI;
  if(i>=count) return;
  Ops ops;
  run_patch(ops,input[i],output[i]);
}
static void launch(const Input *din,Output *dout,unsigned count) {
  constexpr unsigned block=128;
  fused_kernel<<<(count+block/ROOT_TPI-1)/(block/ROOT_TPI),block>>>(din,dout,count);
}
#include "common_host.hpp"
