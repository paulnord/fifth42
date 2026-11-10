// TEST_ONLY: two streams within one request. No cross-request pipelining.
#include <cuda_runtime.h>
#include "stream_io.hpp"
inline void check(cudaError_t e,const char* op){if(e!=cudaSuccess)throw std::runtime_error(std::string(op)+": "+cudaGetErrorString(e));}
template<class T> struct Buffer {
 T *d=nullptr,*h=nullptr;std::size_t capacity=0;
 void reserve(std::size_t n){n=std::max<std::size_t>(1,n);if(n<=capacity)return;
  T *nd=nullptr,*nh=nullptr;check(cudaMalloc(reinterpret_cast<void**>(&nd),n*sizeof(T)),"device allocation");
  auto e=cudaMallocHost(reinterpret_cast<void**>(&nh),n*sizeof(T));if(e!=cudaSuccess){cudaFree(nd);check(e,"pinned allocation");}
  if(d)cudaFree(d);if(h)cudaFreeHost(h);d=nd;h=nh;capacity=n;
 }
 ~Buffer(){if(d)cudaFree(d);if(h)cudaFreeHost(h);}
 Buffer()=default;Buffer(const Buffer&)=delete;Buffer& operator=(const Buffer&)=delete;
};
__global__ void enumerate_overlap(const Task* tasks,const Chunk* chunks,unsigned offset,int mode,U64 cap,
 Candidate* hits,U64* found,unsigned capacity,U64* counts){
 const auto chunk=chunks[blockIdx.x];const auto task=tasks[chunk.task];U64 visited=0;
 for(U64 j=threadIdx.x;j<chunk.count;j+=blockDim.x){++visited;Candidate hit{};
  if(evaluate(task,chunk.task+offset,chunk.first+j,mode,cap,hit)){
   const auto p=atomicAdd(found,1ULL);if(p<capacity)hits[p]=hit;
  }}atomicAdd(counts+chunk.task,visited);
}
struct Lane {
 cudaStream_t stream=nullptr;cudaEvent_t begin=nullptr,end=nullptr;
 Buffer<Task> tasks;Buffer<Chunk> chunks;Buffer<Candidate> hits;Buffer<U64> found,counts;
 unsigned offset=0;std::size_t nt=0,nc=0;float ms=0;
 Lane(){check(cudaStreamCreateWithFlags(&stream,cudaStreamNonBlocking),"create stream");check(cudaEventCreate(&begin),"create begin");check(cudaEventCreate(&end),"create end");}
 ~Lane(){if(stream)cudaStreamSynchronize(stream);if(begin)cudaEventDestroy(begin);if(end)cudaEventDestroy(end);if(stream)cudaStreamDestroy(stream);}
 void prepare(const Input& in,unsigned first,unsigned last,unsigned capacity){
  offset=first;nt=last-first;nc=0;for(const auto& c:in.chunks)if(c.task>=first&&c.task<last)++nc;
  tasks.reserve(nt);chunks.reserve(nc);hits.reserve(capacity);found.reserve(1);counts.reserve(nt);
  std::copy(in.tasks.begin()+first,in.tasks.begin()+last,tasks.h);std::size_t k=0;
  for(auto c:in.chunks)if(c.task>=first&&c.task<last){c.task-=first;chunks.h[k++]=c;}
 }
 void submit(const Input& in,unsigned capacity){
  if(nt)check(cudaMemcpyAsync(tasks.d,tasks.h,nt*sizeof(Task),cudaMemcpyHostToDevice,stream),"task upload");
  if(nc)check(cudaMemcpyAsync(chunks.d,chunks.h,nc*sizeof(Chunk),cudaMemcpyHostToDevice,stream),"chunk upload");
  check(cudaMemsetAsync(found.d,0,sizeof(U64),stream),"reset hits");
  if(nt)check(cudaMemsetAsync(counts.d,0,nt*sizeof(U64),stream),"reset counts");
  check(cudaEventRecord(begin,stream),"begin event");
  if(nc){enumerate_overlap<<<static_cast<unsigned>(nc),256,0,stream>>>(tasks.d,chunks.d,offset,in.mode,in.cap,hits.d,found.d,capacity,counts.d);check(cudaGetLastError(),"launch");}
  check(cudaEventRecord(end,stream),"end event");
  check(cudaMemcpyAsync(found.h,found.d,sizeof(U64),cudaMemcpyDeviceToHost,stream),"found download");
  if(nt)check(cudaMemcpyAsync(counts.h,counts.d,nt*sizeof(U64),cudaMemcpyDeviceToHost,stream),"counts download");
 }
 void finish(unsigned capacity){check(cudaStreamSynchronize(stream),"stream completion");check(cudaEventElapsedTime(&ms,begin,end),"kernel timing");
  if(found.h[0]>capacity)throw std::runtime_error("candidate capacity exceeded; no coverage");
  if(found.h[0]){check(cudaMemcpyAsync(hits.h,hits.d,found.h[0]*sizeof(Candidate),cudaMemcpyDeviceToHost,stream),"hit download");check(cudaStreamSynchronize(stream),"hit completion");}
 }
};
int main(int argc,char**argv){try{
 protect_parent();const auto capacity=::capacity(argc,argv);check(cudaSetDevice(0),"select GPU");check(cudaFree(nullptr),"context");
 Lane lanes[2];std::cout<<"{\"ready\":true,\"backend\":\"gpu\",\"persistent\":true,\"reusable_buffers\":true,\"test_only_two_streams\":true}\n"<<std::flush;
 U64 previous=0,request=0;std::string payload;
 while(read_frame(request,payload,previous)){try{
  const auto start=Clock::now();const auto in=parse_frame(payload);const unsigned split=static_cast<unsigned>((in.tasks.size()+1)/2);
  lanes[0].prepare(in,0,split,capacity);lanes[1].prepare(in,split,static_cast<unsigned>(in.tasks.size()),capacity);
  for(auto& l:lanes)l.submit(in,capacity);for(auto& l:lanes)l.finish(capacity);
  if(lanes[0].found.h[0]+lanes[1].found.h[0]>capacity)throw std::runtime_error("combined candidate capacity exceeded; no coverage");
  std::vector<Candidate> hits;std::vector<U64> counts(in.tasks.size());float ms=0;
  for(auto& l:lanes){hits.insert(hits.end(),l.hits.h,l.hits.h+l.found.h[0]);std::copy(l.counts.h,l.counts.h+l.nt,counts.begin()+l.offset);ms+=l.ms;}
  frame_output(request,[&](){print_result("gpu",in,hits,counts,elapsed(start),ms/1000.0);});
 }catch(const std::exception& e){for(auto& l:lanes)cudaStreamSynchronize(l.stream);frame_output(request,[&](){failure(e);});}}
 return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}}
