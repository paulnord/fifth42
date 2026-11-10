// Isolated batched candidate reduction. GPU values never certify a lattice.
#include <cuda_runtime.h>
#include <cmath>
#include <cstdint>
#include <climits>
#include <chrono>
#include <new>

struct DD { double h,l; };
struct Result { int64_t u[9]; int32_t status,steps; };
__device__ DD norm(double a,double b) { double s=a+b; return {s,b-(s-a)}; }
__device__ DD add(DD a,DD b) {
 double s=a.h+b.h,v=s-a.h;
 double e=((a.h-(s-v))+(b.h-v))+a.l+b.l; return norm(s,e);
}
__device__ DD neg(DD a) { return {-a.h,-a.l}; }
__device__ DD sub(DD a,DD b) { return add(a,neg(b)); }
__device__ DD mul(DD a,DD b) {
 double p=a.h*b.h;double e=fma(a.h,b.h,-p)+a.h*b.l+a.l*b.h;
 DD z=norm(p,e);return add(z,{a.l*b.l,0});
}
__device__ DD divd(DD a,DD b) {
 double q1=a.h/b.h;DD r=sub(a,mul(b,{q1,0}));
 double q2=r.h/b.h;r=sub(r,mul(b,{q2,0}));
 double q3=r.h/b.h;return add(add({q1,0},{q2,0}),{q3,0});
}
__device__ bool finite(DD a) { return isfinite(a.h)&&isfinite(a.l); }
__device__ int cmp(DD a,DD b) {
 DD d=sub(a,b);return d.h>0?1:(d.h<0?-1:(d.l>0?1:(d.l<0?-1:0)));
}
__device__ DD dot(const DD*a,const DD*b) { return add(add(mul(a[0],b[0]),mul(a[1],b[1])),mul(a[2],b[2])); }
__device__ bool gs(DD b[9],DD mu[9],DD d[3]) {
 DD star[9];
 for(int i=0;i<9;i++)mu[i]={0,0};
 for(int i=0;i<3;i++) {
  for(int c=0;c<3;c++)star[3*i+c]=b[3*i+c];
  for(int j=0;j<i;j++) {
   if(cmp(d[j],{0,0})<=0||!finite(d[j]))return false;
   mu[3*i+j]=divd(dot(b+3*i,star+3*j),d[j]);
   if(!finite(mu[3*i+j]))return false;
   for(int c=0;c<3;c++)star[3*i+c]=sub(star[3*i+c],mul(mu[3*i+j],star[3*j+c]));
  }
  d[i]=dot(star+3*i,star+3*i);
  if(cmp(d[i],{0,0})<=0||!finite(d[i]))return false;
 }
 return true;
}
__device__ bool row_integer(int64_t*dst,const int64_t*src,int64_t q) {
 constexpr int64_t limit=(int64_t(1)<<60)-1;
 int64_t temp[3];
 for(int i=0;i<3;i++) {
  uint64_t a=q<0?-uint64_t(q):uint64_t(q),b=src[i]<0?-uint64_t(src[i]):uint64_t(src[i]);
  if(b && a>uint64_t(limit)/b)return false;
  int64_t product=q*src[i];
  if((product>0&&dst[i]<-limit+product)||(product<0&&dst[i]>limit+product))return false;
  temp[i]=dst[i]-product;
  if(temp[i]<-limit||temp[i]>limit)return false;
 }
 for(int i=0;i<3;i++)dst[i]=temp[i];return true;
}
__global__ void candidates(const DD*input,Result*output,int count,int maxsteps) {
 int index=blockIdx.x*blockDim.x+threadIdx.x;if(index>=count)return;
 DD b[9],mu[9],d[3];Result r{};
 for(int i=0;i<9;i++){b[i]=input[9*index+i];r.u[i]=(i/3==i%3);if(!finite(b[i]))r.status=4;}
 int k=1;
 while(k<3 && r.status==0) {
  if(++r.steps>maxsteps){r.status=1;break;}
  for(int j=k-1;j>=0;j--) {
   if(!gs(b,mu,d)){r.status=3;break;}
   double value=mu[3*k+j].h+mu[3*k+j].l;
   if(!isfinite(value)||fabs(value)>=1125899906842624.0){r.status=2;break;}
   int64_t q=static_cast<int64_t>(floor(value+0.5));
   if(q) {
    if(!row_integer(r.u+3*k,r.u+3*j,q)){r.status=2;break;}
    for(int c=0;c<3;c++)b[3*k+c]=sub(b[3*k+c],mul({double(q),0},b[3*j+c]));
   }
  }
  if(r.status)break;
  if(!gs(b,mu,d)){r.status=3;break;}
  DD rhs=mul(sub({0.75,0},mul(mu[3*k+k-1],mu[3*k+k-1])),d[k-1]);
  if(cmp(d[k],rhs)>=0)k++;
  else {
   for(int c=0;c<3;c++){DD v=b[3*k+c];b[3*k+c]=b[3*(k-1)+c];b[3*(k-1)+c]=v;int64_t u=r.u[3*k+c];r.u[3*k+c]=r.u[3*(k-1)+c];r.u[3*(k-1)+c]=u;}
   k=k>1?k-1:1;
  }
 }
 output[index]=r;
}
struct Context { DD*input=nullptr;Result*output=nullptr;int capacity,maxsteps;cudaEvent_t begin,end; };
extern "C" void* gpu_lll_create(int capacity,int maxsteps,int*error) {
 *error=0;if(capacity<1||capacity>65536||maxsteps<1||maxsteps>4096){*error=int(cudaErrorInvalidValue);return nullptr;}
 Context*c=new(std::nothrow) Context;if(!c){*error=int(cudaErrorMemoryAllocation);return nullptr;}c->capacity=capacity;c->maxsteps=maxsteps;
 cudaError_t e=cudaSetDevice(0);
 if(e==cudaSuccess)e=cudaMalloc(reinterpret_cast<void**>(&c->input),sizeof(DD)*9*capacity);
 if(e==cudaSuccess)e=cudaMalloc(reinterpret_cast<void**>(&c->output),sizeof(Result)*capacity);
 if(e==cudaSuccess)e=cudaEventCreate(&c->begin);
 if(e==cudaSuccess)e=cudaEventCreate(&c->end);
 if(e!=cudaSuccess){*error=int(e);if(c->input)cudaFree(c->input);if(c->output)cudaFree(c->output);delete c;return nullptr;}
 return c;
}
extern "C" int gpu_lll_run(void*handle,const double*input,int count,Result*output,double*kernel_ms,double*wall_ms) {
 Context*c=static_cast<Context*>(handle);if(!c||count<1||count>c->capacity)return int(cudaErrorInvalidValue);
 auto start=std::chrono::steady_clock::now();cudaError_t e=cudaMemcpy(c->input,input,sizeof(DD)*9*count,cudaMemcpyHostToDevice);
 if(e==cudaSuccess)e=cudaEventRecord(c->begin);
 if(e==cudaSuccess){candidates<<<(count+127)/128,128>>>(c->input,c->output,count,c->maxsteps);e=cudaGetLastError();}
 if(e==cudaSuccess)e=cudaEventRecord(c->end);
 if(e==cudaSuccess)e=cudaEventSynchronize(c->end);
 float ms=0;if(e==cudaSuccess)e=cudaEventElapsedTime(&ms,c->begin,c->end);
 if(e==cudaSuccess)e=cudaMemcpy(output,c->output,sizeof(Result)*count,cudaMemcpyDeviceToHost);
 *kernel_ms=ms;*wall_ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count();return int(e);
}
extern "C" void gpu_lll_destroy(void*handle) {
 Context*c=static_cast<Context*>(handle);if(c){cudaEventDestroy(c->begin);cudaEventDestroy(c->end);cudaFree(c->input);cudaFree(c->output);delete c;}
}
extern "C" const char* gpu_lll_error(int code) { return cudaGetErrorString(static_cast<cudaError_t>(code)); }
