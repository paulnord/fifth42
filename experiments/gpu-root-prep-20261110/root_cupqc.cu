// cuPQC-BigInt 0.6.0 division-free root preparation.
// NOT compiled or GPU-validated by Dot; implemented against official API docs.
// No production integration. Protocol is explicitly little-endian, without padding.
#include <cuda_runtime.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <stdexcept>
#include <string>
#include <vector>
#include <bigint.hpp>
#ifndef ROOT_TPI
#define ROOT_TPI 8
#endif
#ifndef ROOT_SM
#define ROOT_SM 860
#endif
static_assert(ROOT_TPI==4 || ROOT_TPI==8 || ROOT_TPI==16 || ROOT_TPI==32,
              "ROOT_TPI must be 4, 8, 16, or 32");
constexpr unsigned WIDTH=2048, LIMBS=64, BLOCK=128;
struct Memory { uint32_t _limbs[LIMBS]; };
struct Input { uint32_t bits; Memory numerator, denominator; };
using Descriptor=decltype(cupqc::BitWidth<WIDTH>() + cupqc::SM<ROOT_SM>() +
                          cupqc::TPI<ROOT_TPI>() + cupqc::Warp());
using BigInt=typename Descriptor::bigint;

__global__ void roots(Input *input, Memory *output, uint32_t count) {
  const uint32_t i=(blockIdx.x*blockDim.x+threadIdx.x)/ROOT_TPI;
  if(i>=count) return; // Whole cooperative group exits together.
  const BigInt n(input[i].numerator._limbs), d(input[i].denominator._limbs);
  const BigInt one(uint32_t{1});
  const BigInt target=n << (5*input[i].bits);
  BigInt r(uint32_t{0});
  // All mul_low operations are exact, not merely low residues: host guard
  // proves the full products fit WIDTH even for a rejected candidate.
  for(int b=static_cast<int>(input[i].bits); b>=0; --b) {
    const BigInt candidate=r | (one << b);
    const BigInt square=candidate.mul_low(candidate);
    const BigInt fourth=square.mul_low(square);
    const BigInt fifth=fourth.mul_low(candidate);
    const BigInt product=fifth.mul_low(d);
    if(product.compare(target)<=0) r=candidate;
  }
  r.store(output[i]._limbs);
}
static void check(cudaError_t e,const char *where) {
  if(e!=cudaSuccess) throw std::runtime_error(std::string(where)+": "+cudaGetErrorString(e));
}
#define CUDA(call) check((call),#call)
static uint32_t read32(FILE *f) {
  unsigned char b[4];
  if(fread(b,1,4,f)!=4) throw std::runtime_error("truncated input");
  return uint32_t(b[0])|(uint32_t(b[1])<<8)|(uint32_t(b[2])<<16)|(uint32_t(b[3])<<24);
}
static void write32(FILE *f,uint32_t x) {
  unsigned char b[4]={static_cast<unsigned char>(x),static_cast<unsigned char>(x>>8),
    static_cast<unsigned char>(x>>16),static_cast<unsigned char>(x>>24)};
  if(fwrite(b,1,4,f)!=4) throw std::runtime_error("output write failed");
}
static unsigned bitlen(const Memory& a) {
  for(int i=LIMBS-1;i>=0;--i) if(a._limbs[i]) {
    uint32_t v=a._limbs[i]; unsigned n=0; while(v) { ++n; v>>=1; }
    return 32*i+n;
  }
  return 0;
}
static int compare(const Memory& a,const Memory& b) {
  for(int i=LIMBS-1;i>=0;--i) if(a._limbs[i]!=b._limbs[i])
    return a._limbs[i]<b._limbs[i]?-1:1;
  return 0;
}
int main(int argc,char **argv) {
  const auto start=std::chrono::steady_clock::now();
  try {
    if(argc<3 || argc>4) throw std::runtime_error("usage: root_cuda INPUT.bin OUTPUT.bin [REPEATS=1]");
    if(std::string(argv[1])==argv[2]) throw std::runtime_error("input and output paths must differ");
    unsigned repeats=1;
    if(argc==4) { char *end=nullptr; long r=strtol(argv[3],&end,10);
      if(!*argv[3] || *end || r<1 || r>10000) throw std::runtime_error("invalid repeats (1..10000)");
      repeats=static_cast<unsigned>(r); }
    FILE *f=fopen(argv[1],"rb"); if(!f) throw std::runtime_error("cannot open input");
    const uint32_t count=read32(f);
    if(!count || count>1000000) throw std::runtime_error("count must be 1..1000000");
    std::vector<Input> input(count);
    for(uint32_t i=0;i<count;++i) {
      Input &a=input[i]; a.bits=read32(f);
      for(unsigned j=0;j<LIMBS;++j) a.numerator._limbs[j]=read32(f);
      for(unsigned j=0;j<LIMBS;++j) a.denominator._limbs[j]=read32(f);
      const unsigned nb=bitlen(a.numerator),db=bitlen(a.denominator);
      // Candidate < 2^(bits+1), including the x=1 boundary. Therefore all
      // products and shifts fit WIDTH without relying on truncation behavior.
      if(!db || compare(a.numerator,a.denominator)>0 || a.bits<1 || a.bits>222 ||
         (nb>db?nb:db)+5*(a.bits+1)>WIDTH)
        throw std::runtime_error("unsupported input/width at record "+std::to_string(i)+"; use CPU fallback");
    }
    if(fgetc(f)!=EOF || ferror(f)) throw std::runtime_error("trailing input bytes or read error");
    if(fclose(f)) throw std::runtime_error("input close error");
    Input *din=nullptr; Memory *dout=nullptr;
    CUDA(cudaSetDevice(0));
    CUDA(cudaMalloc(reinterpret_cast<void**>(&din),sizeof(Input)*count));
    CUDA(cudaMalloc(reinterpret_cast<void**>(&dout),sizeof(*dout)*count));
    CUDA(cudaMemcpy(din,input.data(),sizeof(Input)*count,cudaMemcpyHostToDevice));
    cudaEvent_t begin,end; CUDA(cudaEventCreate(&begin)); CUDA(cudaEventCreate(&end));
    double kernel_ms=0;
    for(unsigned r=0;r<repeats;++r) {
      CUDA(cudaEventRecord(begin));
      roots<<<(count+(BLOCK/ROOT_TPI)-1)/(BLOCK/ROOT_TPI),BLOCK>>>(din,dout,count);
      CUDA(cudaGetLastError()); CUDA(cudaEventRecord(end)); CUDA(cudaEventSynchronize(end));
      float ms=0; CUDA(cudaEventElapsedTime(&ms,begin,end)); kernel_ms+=ms;
      fprintf(stderr,"kernel_repeat=%u kernel_ms=%.6f\n",r,ms);
    }
    std::vector<Memory> output(count);
    CUDA(cudaMemcpy(output.data(),dout,sizeof(*dout)*count,cudaMemcpyDeviceToHost));
    CUDA(cudaEventDestroy(begin)); CUDA(cudaEventDestroy(end));
    CUDA(cudaFree(din)); CUDA(cudaFree(dout));
    FILE *o=fopen(argv[2],"wb"); if(!o) throw std::runtime_error("cannot open output");
    write32(o,count);
    for(const auto &a:output) for(unsigned j=0;j<LIMBS;++j) write32(o,a._limbs[j]);
    if(fclose(o)) throw std::runtime_error("output close error");
    const double wall_ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count();
    fprintf(stderr,"count=%u tpi=%u repeats=%u mean_kernel_ms=%.6f process_wall_ms=%.6f\n",
      count,ROOT_TPI,repeats,kernel_ms/repeats,wall_ms);
    return 0;
  } catch(const std::exception &e) { fprintf(stderr,"ERROR: %s\n",e.what()); return 1; }
}
