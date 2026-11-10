#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <string>
#include <vector>
static void ck(cudaError_t e,const char*w){if(e!=cudaSuccess)throw std::runtime_error(std::string(w)+": "+cudaGetErrorString(e));}
#define CUDA(x) ck((x),#x)
static uint32_t read32(FILE*f){unsigned char b[4];if(fread(b,1,4,f)!=4)throw std::runtime_error("truncated input");return uint32_t(b[0])|(uint32_t(b[1])<<8)|(uint32_t(b[2])<<16)|(uint32_t(b[3])<<24);}
static uint64_t read64(FILE*f){uint64_t a=read32(f),b=read32(f);return a|(b<<32);}
static void write32(FILE*f,uint32_t x){unsigned char b[4]={(unsigned char)x,(unsigned char)(x>>8),(unsigned char)(x>>16),(unsigned char)(x>>24)};if(fwrite(b,1,4,f)!=4)throw std::runtime_error("write failed");}
static void guard(const Input&a){
 const uint64_t max=uint64_t(1)<<40;
 if(!a.lo||a.lo>a.hi||a.hi>max||!a.den||a.den>max||a.left>=a.right||a.right>=a.den||a.cap>42||a.bits<1||a.bits>222)throw std::runtime_error("unsupported domain: CPU fallback required");
 // Independent GMP host preflight ensures singular adjusted radicand cannot underflow.
 mpz_t d,r,c,t,u;mpz_inits(d,r,c,t,u,nullptr);mpz_set_ui(d,a.den);mpz_pow_ui(d,d,5);mpz_set_ui(r,a.right);mpz_pow_ui(r,r,5);mpz_sub(t,d,r);mpz_set_ui(c,a.lo);mpz_pow_ui(c,c,5);mpz_mul(t,t,c);mpz_mul_ui(u,d,a.cap);bool ok=mpz_cmp(t,u)>0;mpz_clears(d,r,c,t,u,nullptr);if(!ok)throw std::runtime_error("singular patch");
}
int main(int argc,char**argv){auto start=std::chrono::steady_clock::now();try{
 if(argc<3||argc>4)throw std::runtime_error("usage: fused INPUT OUTPUT [REPEATS]");
 if(std::string(argv[1])==argv[2])throw std::runtime_error("input/output paths must differ");
 unsigned repeats=6;if(argc==4){char*e;long r=strtol(argv[3],&e,10);if(!*argv[3]||*e||r<1||r>100)throw std::runtime_error("repeats1..100");repeats=r;}
 FILE*f=fopen(argv[1],"rb");if(!f)throw std::runtime_error("input open failed");unsigned count=read32(f);if(!count||count>65536)throw std::runtime_error("count1..65536");std::vector<Input> in(count);
 for(auto&a:in){a.lo=read64(f);a.hi=read64(f);a.left=read64(f);a.right=read64(f);a.den=read64(f);a.cap=read64(f);a.bits=read32(f);guard(a);}
 if(fgetc(f)!=EOF||ferror(f))throw std::runtime_error("trailing bytes/read error");fclose(f);
 Input*di;Output*doo;CUDA(cudaSetDevice(0));CUDA(cudaMalloc((void**)&di,sizeof(Input)*count));CUDA(cudaMalloc((void**)&doo,sizeof(Output)*count));
 cudaEvent_t b,e;CUDA(cudaEventCreate(&b));CUDA(cudaEventCreate(&e));CUDA(cudaEventRecord(b));CUDA(cudaMemcpy(di,in.data(),sizeof(Input)*count,cudaMemcpyHostToDevice));CUDA(cudaEventRecord(e));CUDA(cudaEventSynchronize(e));float ms;CUDA(cudaEventElapsedTime(&ms,b,e));fprintf(stderr,"h2d_ms=%.6f bytes=%zu\n",ms,sizeof(Input)*count);
 for(unsigned r=0;r<repeats;++r){CUDA(cudaEventRecord(b));launch(di,doo,count);CUDA(cudaGetLastError());CUDA(cudaEventRecord(e));CUDA(cudaEventSynchronize(e));CUDA(cudaEventElapsedTime(&ms,b,e));fprintf(stderr,"repeat=%u kernel_ms=%.6f\n",r,ms);}
 std::vector<Output> out(count);CUDA(cudaEventRecord(b));CUDA(cudaMemcpy(out.data(),doo,sizeof(Output)*count,cudaMemcpyDeviceToHost));CUDA(cudaEventRecord(e));CUDA(cudaEventSynchronize(e));CUDA(cudaEventElapsedTime(&ms,b,e));fprintf(stderr,"d2h_ms=%.6f bytes=%zu\n",ms,sizeof(Output)*count);
 CUDA(cudaEventDestroy(b));CUDA(cudaEventDestroy(e));CUDA(cudaFree(di));CUDA(cudaFree(doo));FILE*g=fopen(argv[2],"wb");if(!g)throw std::runtime_error("output open failed");write32(g,count);for(const auto&a:out)for(const auto&v:a.value)for(auto x:v._limbs)write32(g,x);if(fclose(g))throw std::runtime_error("output close failed");
 fprintf(stderr,"process_ms=%.6f\n",std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count());return 0;
 }catch(const std::exception&e){fprintf(stderr,"ERROR: %s\n",e.what());return 1;}}
