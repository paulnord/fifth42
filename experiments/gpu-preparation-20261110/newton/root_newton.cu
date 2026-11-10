// Isolated CGBN Newton root prototype. No production integration.
// GPU candidates must still receive independent exact CPU certification.
#include <gmp.h>
#include <cuda_runtime.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <chrono>
#include <stdexcept>
#include <string>
#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#include "cgbn/cgbn.h"
#ifndef ROOT_TPI
#define ROOT_TPI 8
#endif
#ifndef ROOT_FLOAT_SEED
#define ROOT_FLOAT_SEED 1
#endif
static_assert(ROOT_TPI==4 || ROOT_TPI==8 || ROOT_TPI==16 || ROOT_TPI==32);
constexpr unsigned BLOCK=128;
struct FullInput { uint32_t bits; std::array<uint32_t,64> n,d; };
template<unsigned W> struct Input { uint32_t bits; cgbn_mem_t<W> n,d; };
struct Stats { uint32_t iterations, fallback, error; };

template<unsigned W, class E>
__device__ __forceinline__ void fifth(E &e,typename E::cgbn_t &out,const typename E::cgbn_t &a) {
  typename E::cgbn_t square,fourth;
  cgbn_mul(e,square,a,a);cgbn_mul(e,fourth,square,square);cgbn_mul(e,out,fourth,a);
}

template<unsigned W>
__global__ void roots(cgbn_error_report_t *report,Input<W>*input,
                      cgbn_mem_t<W>*output,Stats*stats,uint32_t count) {
  const uint32_t i=(blockIdx.x*blockDim.x+threadIdx.x)/ROOT_TPI;
  if(i>=count)return;
  using C=cgbn_context_t<ROOT_TPI>;using E=cgbn_env_t<C,W>;
  C context(cgbn_report_monitor,report,i);E e(context.template env<E>());
  typename E::cgbn_t n,d,scaled,target,r,one,square,fourth,q,next,sum,power,up;
  cgbn_load(e,n,&input[i].n);cgbn_load(e,d,&input[i].d);
  cgbn_shift_left(e,scaled,n,5*input[i].bits);
  cgbn_div(e,target,scaled,d);
  cgbn_set_ui32(e,one,1);
  uint32_t steps=0,fallback=0,error=0;
  const uint32_t bits=W-cgbn_clz(e,target);
  if(bits==0)cgbn_set_ui32(e,r,0);
  else {
    const uint32_t upper_bit=(bits+4)/5;
    cgbn_shift_left(e,r,one,upper_bit);
#if ROOT_FLOAT_SEED
    // Approximation supplies a candidate only. Exact power comparison below
    // proves it is an upper bound; otherwise use the integer upper bound.
    const uint32_t take=bits<24?bits:24;
    const uint32_t shift=bits-take;
    const uint32_t top=cgbn_extract_bits_ui32(e,target,shift,take);
    const float approx=__powf(ldexpf(static_cast<float>(top),shift%5),0.2f);
    const uint32_t prefix=static_cast<uint32_t>(ceilf(ldexpf(approx,20)))+16;
    const int exponent=static_cast<int>(shift/5)-20;
    if(exponent>=0){cgbn_set_ui32(e,next,prefix);cgbn_shift_left(e,next,next,exponent);}
    else {const uint32_t right=-exponent;cgbn_set_ui32(e,next,(prefix+((1u<<right)-1))>>right);}
    // Check the certified coefficient range BEFORE any power, so the width
    // proof remains valid even for a completely inaccurate floating seed.
    if(cgbn_compare(e,next,r)<=0 && cgbn_compare_ui32(e,next,0)>0) {
      fifth<W>(e,power,next);
      // next^5 >= target proves this is a descending-Newton upper seed.
      if(cgbn_compare(e,power,target)>=0)cgbn_set(e,r,next);
      else fallback=1;
    } else fallback=1;
#endif
    bool finished=false;
    for(uint32_t k=0;k<64;++k) {
      cgbn_mul(e,square,r,r);cgbn_mul(e,fourth,square,square);
      cgbn_div(e,q,target,fourth);
      cgbn_mul_ui32(e,sum,r,4);cgbn_add(e,sum,sum,q);cgbn_div_ui32(e,next,sum,5);
      ++steps;
      if(cgbn_compare(e,next,r)>=0){finished=true;break;}
      cgbn_set(e,r,next);
    }
    if(!finished)error=1;
  }
  // Independent device consistency gate. CPU verifies the original rational
  // inequalities as well; neither this check nor a float seed replaces it.
  fifth<W>(e,power,r);
  if(cgbn_compare(e,power,target)>0)error=2;
  cgbn_add_ui32(e,up,r,1);fifth<W>(e,power,up);
  if(cgbn_compare(e,power,target)<=0)error=3;
  cgbn_store(e,&output[i],r);
  if(threadIdx.x%ROOT_TPI==0)stats[i]={steps,fallback,error};
}
static void check(cudaError_t code,const char*what){if(code!=cudaSuccess)throw std::runtime_error(std::string(what)+": "+cudaGetErrorString(code));}
#define CUDA(x) check((x),#x)
static uint32_t read32(FILE*f){unsigned char b[4];if(fread(b,1,4,f)!=4)throw std::runtime_error("truncated input");return uint32_t(b[0])|(uint32_t(b[1])<<8)|(uint32_t(b[2])<<16)|(uint32_t(b[3])<<24);}
static void write32(FILE*f,uint32_t x){unsigned char b[4]={static_cast<unsigned char>(x),static_cast<unsigned char>(x>>8),static_cast<unsigned char>(x>>16),static_cast<unsigned char>(x>>24)};if(fwrite(b,1,4,f)!=4)throw std::runtime_error("write failed");}
static unsigned bitlen(const std::array<uint32_t,64>&x){for(int i=63;i>=0;--i)if(x[i])return i*32+32-__builtin_clz(x[i]);return 0;}
static int compare(const std::array<uint32_t,64>&a,const std::array<uint32_t,64>&b){for(int i=63;i>=0;--i)if(a[i]!=b[i])return a[i]<b[i]?-1:1;return 0;}
template<unsigned W> struct Bucket {
  std::vector<Input<W>> host;
  std::vector<uint32_t> indices;
  Input<W>*din=nullptr;cgbn_mem_t<W>*dout=nullptr;Stats*dstats=nullptr;size_t capacity=0;
  void clear(){host.clear();indices.clear();}
  void append(const FullInput&x,uint32_t i){Input<W> a{};a.bits=x.bits;std::copy_n(x.n.data(),W/32,a.n._limbs);std::copy_n(x.d.data(),W/32,a.d._limbs);host.push_back(a);indices.push_back(i);}
  void reserve(){if(host.size()<=capacity)return;release();capacity=host.size();CUDA(cudaMalloc(reinterpret_cast<void**>(&din),capacity*sizeof(*din)));CUDA(cudaMalloc(reinterpret_cast<void**>(&dout),capacity*sizeof(*dout)));CUDA(cudaMalloc(reinterpret_cast<void**>(&dstats),capacity*sizeof(*dstats)));}
  void release(){if(din)cudaFree(din);if(dout)cudaFree(dout);if(dstats)cudaFree(dstats);din=nullptr;dout=nullptr;dstats=nullptr;capacity=0;}
  ~Bucket(){release();}
};
class Session {
  Bucket<512>b512;Bucket<1024>b1024;Bucket<2048>b2048;
  cgbn_error_report_t*report=nullptr;cudaEvent_t begin,end;
 public:
  Session(){CUDA(cudaSetDevice(0));CUDA(cgbn_error_report_alloc(&report));CUDA(cudaEventCreate(&begin));CUDA(cudaEventCreate(&end));}
  ~Session(){cudaEventDestroy(begin);cudaEventDestroy(end);cgbn_error_report_free(report);}
  template<unsigned W>float launch(Bucket<W>&b){if(b.host.empty())return 0;CUDA(cudaEventRecord(begin));roots<W><<<(b.host.size()+BLOCK/ROOT_TPI-1)/(BLOCK/ROOT_TPI),BLOCK>>>(report,b.din,b.dout,b.dstats,b.host.size());CUDA(cudaGetLastError());CUDA(cudaEventRecord(end));CUDA(cudaEventSynchronize(end));if(cgbn_error_report_check(report))throw std::runtime_error(cgbn_error_string(report));float ms=0;CUDA(cudaEventElapsedTime(&ms,begin,end));return ms;}
  template<unsigned W>void upload(Bucket<W>&b){if(b.host.empty())return;b.reserve();CUDA(cudaMemcpy(b.din,b.host.data(),b.host.size()*sizeof(*b.din),cudaMemcpyHostToDevice));}
  template<unsigned W>void download(Bucket<W>&b,std::vector<std::array<uint32_t,64>>&output,std::vector<Stats>&stats){if(b.host.empty())return;std::vector<cgbn_mem_t<W>>values(b.host.size());std::vector<Stats>local(b.host.size());CUDA(cudaMemcpy(values.data(),b.dout,values.size()*sizeof(*b.dout),cudaMemcpyDeviceToHost));CUDA(cudaMemcpy(local.data(),b.dstats,local.size()*sizeof(*b.dstats),cudaMemcpyDeviceToHost));for(size_t j=0;j<local.size();++j){if(local[j].error)throw std::runtime_error("Newton/device certificate failure at record "+std::to_string(b.indices[j])+" code "+std::to_string(local[j].error));std::copy_n(values[j]._limbs,W/32,output[b.indices[j]].data());stats[b.indices[j]]=local[j];}}
  std::string run(const std::string&infile,const std::string&outfile,unsigned repeats){
    using Clock=std::chrono::steady_clock;const auto start=Clock::now();
    if(infile==outfile)throw std::runtime_error("input and output must differ");
    FILE*f=fopen(infile.c_str(),"rb");if(!f)throw std::runtime_error("cannot open input");
    b512.clear();b1024.clear();b2048.clear();const uint32_t count=read32(f);if(count==0||count>1000000)throw std::runtime_error("count must be 1..1000000");
    static_assert(sizeof(FullInput)==516);const uint32_t endian=1;if(*reinterpret_cast<const unsigned char*>(&endian)!=1)throw std::runtime_error("unsupported host byte order");std::vector<FullInput> input(count);if(fread(input.data(),sizeof(FullInput),count,f)!=count)throw std::runtime_error("truncated input");
    for(uint32_t i=0;i<count;++i){const FullInput&x=input[i];const unsigned nb=bitlen(x.n),db=bitlen(x.d);if(db==0||compare(x.n,x.d)>0||x.bits<1||x.bits>222)throw std::runtime_error("unsupported domain at record "+std::to_string(i)+"; CPU fallback required");const unsigned proof=std::max(nb,db)+5*(x.bits+1);if(proof>2048)throw std::runtime_error("unsupported width at record "+std::to_string(i)+"; CPU fallback required");if(proof<=512)b512.append(x,i);else if(proof<=1024)b1024.append(x,i);else b2048.append(x,i);}
    if(fgetc(f)!=EOF||ferror(f))throw std::runtime_error("trailing bytes or read failure");fclose(f);
    const auto parsed=Clock::now();upload(b512);upload(b1024);upload(b2048);const auto uploaded=Clock::now();
    std::vector<float>times;
    for(unsigned j=0;j<repeats;++j){const float ms=launch(b512)+launch(b1024)+launch(b2048);times.push_back(ms);fprintf(stderr,"kernel_repeat=%u kernel_ms=%.6f\n",j,ms);}
    const auto computed=Clock::now();std::vector<std::array<uint32_t,64>>output(count);std::vector<Stats>stats(count);download(b512,output,stats);download(b1024,output,stats);download(b2048,output,stats);const auto downloaded=Clock::now();
    uint64_t iterations=0,fallbacks=0;unsigned max_steps=0;for(auto s:stats){iterations+=s.iterations;fallbacks+=s.fallback;max_steps=std::max(max_steps,s.iterations);}
    FILE*o=fopen(outfile.c_str(),"wb");if(!o)throw std::runtime_error("cannot open output");write32(o,count);static_assert(sizeof(output[0])==256);if(fwrite(output.data(),256,count,o)!=count)throw std::runtime_error("output write failed");if(fclose(o))throw std::runtime_error("output close failed");
    auto ms=[](auto a,auto z){return std::chrono::duration<double,std::milli>(z-a).count();};std::ostringstream out;out<<"{\"status\":\"ok\",\"count\":"<<count<<",\"tpi\":"<<ROOT_TPI<<",\"float_seed\":"<<ROOT_FLOAT_SEED<<",\"width_counts\":{\"512\":"<<b512.host.size()<<",\"1024\":"<<b1024.host.size()<<",\"2048\":"<<b2048.host.size()<<"},\"mean_newton_iterations\":"<<double(iterations)/count<<",\"max_newton_iterations\":"<<max_steps<<",\"seed_fallbacks\":"<<fallbacks<<",\"parse_ms\":"<<ms(start,parsed)<<",\"upload_allocate_ms\":"<<ms(parsed,uploaded)<<",\"download_ms\":"<<ms(computed,downloaded)<<",\"request_ms\":"<<ms(start,Clock::now())<<",\"kernel_ms\":[";for(size_t j=0;j<times.size();++j){if(j)out<<',';out<<times[j];}out<<"]}";return out.str();
  }
};
int main(int argc,char**argv){try{
  const bool server=argc==2&&std::string(argv[1])=="--server";
  if(!server&&(argc<3||argc>4))throw std::runtime_error("usage: root_newton INPUT OUTPUT [REPEATS] or --server");
  Session session;
  if(server){std::cout<<"{\"ready\":true,\"widths\":[512,1024,2048],\"tpi\":"<<ROOT_TPI<<",\"float_seed\":"<<ROOT_FLOAT_SEED<<"}"<<std::endl;std::string line;while(std::getline(std::cin,line)){if(line=="QUIT")break;std::istringstream in(line);std::string cmd,input,output,extra;unsigned repeats=0;if(!(in>>cmd>>input>>output>>repeats)||cmd!="RUN"||(in>>extra)||repeats<1||repeats>10000)throw std::runtime_error("invalid server command");std::cout<<session.run(input,output,repeats)<<std::endl;}}
  else {unsigned repeats=1;if(argc==4){char*end=nullptr;unsigned long n=strtoul(argv[3],&end,10);if(!*argv[3]||*end||n<1||n>10000)throw std::runtime_error("invalid repeat count");repeats=n;}std::cout<<session.run(argv[1],argv[2],repeats)<<std::endl;}
  return 0;
}catch(const std::exception&e){fprintf(stderr,"ERROR: %s\n",e.what());return 1;}}
