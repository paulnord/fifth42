#include <cuda_runtime.h>
#include "io.hpp"
inline void check(cudaError_t e,const char* what){if(e!=cudaSuccess)throw std::runtime_error(std::string(what)+": "+cudaGetErrorString(e));}
template<class T>struct Buffer {
    T* p=nullptr;
    explicit Buffer(std::size_t n){check(cudaMalloc(reinterpret_cast<void**>(&p),std::max<std::size_t>(1,n)*sizeof(T)),"cudaMalloc");}
    ~Buffer(){if(p)cudaFree(p);}
    Buffer(const Buffer&)=delete;Buffer& operator=(const Buffer&)=delete;
};
__global__ void enumerate(const Task* tasks,const Chunk* chunks,int mode,std::uint64_t cap,Candidate* out,U64* found,unsigned capacity,U64* counts){
    const auto chunk=chunks[blockIdx.x];const auto task=tasks[chunk.task];U64 visited=0;
    for(std::uint64_t j=threadIdx.x;j<chunk.count;j+=blockDim.x){
        ++visited;Candidate h{};
        if(evaluate(task,chunk.task,chunk.first+j,mode,cap,h)){const auto index=atomicAdd(found,1ULL);if(index<capacity)out[index]=h;}
    }
    atomicAdd(counts+chunk.task,visited);
}
__global__ void arithmetic_kernel(const ArithmeticCase* in,ArithmeticResult* out,unsigned n){const unsigned i=blockIdx.x*blockDim.x+threadIdx.x;if(i<n)out[i]=arithmetic(in[i]);}
int main(int argc,char**argv){try{
    check(cudaSetDevice(0),"select device 0");
    if(argc==2&&std::string(argv[1])=="--arithmetic"){
        const auto cases=read_arithmetic();Buffer<ArithmeticCase> input(cases.size());Buffer<ArithmeticResult> output(cases.size());std::vector<ArithmeticResult> host(cases.size());
        if(!cases.empty()){check(cudaMemcpy(input.p,cases.data(),cases.size()*sizeof(ArithmeticCase),cudaMemcpyHostToDevice),"arithmetic upload");arithmetic_kernel<<<static_cast<unsigned>((cases.size()+127)/128),128>>>(input.p,output.p,static_cast<unsigned>(cases.size()));check(cudaGetLastError(),"arithmetic launch");check(cudaDeviceSynchronize(),"arithmetic sync");check(cudaMemcpy(host.data(),output.p,host.size()*sizeof(ArithmeticResult),cudaMemcpyDeviceToHost),"arithmetic download");}
        print_arithmetic("gpu",host);return 0;
    }
    const auto cap=capacity(argc,argv);const auto start=Clock::now();const auto in=read_input();Buffer<Task> tasks(in.tasks.size());Buffer<Chunk> chunks(in.chunks.size());Buffer<Candidate> hits(cap);Buffer<U64> found(1),counts(in.tasks.size());
    if(!in.tasks.empty())check(cudaMemcpy(tasks.p,in.tasks.data(),in.tasks.size()*sizeof(Task),cudaMemcpyHostToDevice),"task upload");
    if(!in.chunks.empty())check(cudaMemcpy(chunks.p,in.chunks.data(),in.chunks.size()*sizeof(Chunk),cudaMemcpyHostToDevice),"chunk upload");
    check(cudaMemset(found.p,0,sizeof(U64)),"clear found");if(!in.tasks.empty())check(cudaMemset(counts.p,0,in.tasks.size()*sizeof(U64)),"clear counts");
    cudaEvent_t begin,end;check(cudaEventCreate(&begin),"event create");check(cudaEventCreate(&end),"event create");check(cudaEventRecord(begin),"event begin");
    if(!in.chunks.empty()){enumerate<<<static_cast<unsigned>(in.chunks.size()),256>>>(tasks.p,chunks.p,in.mode,in.cap,hits.p,found.p,cap,counts.p);check(cudaGetLastError(),"enumeration launch");}
    check(cudaEventRecord(end),"event end");check(cudaEventSynchronize(end),"event sync");float ms=0;check(cudaEventElapsedTime(&ms,begin,end),"event elapsed");cudaEventDestroy(begin);cudaEventDestroy(end);
    U64 n=0;check(cudaMemcpy(&n,found.p,sizeof(U64),cudaMemcpyDeviceToHost),"count download");if(n>cap)throw std::runtime_error("candidate capacity exceeded; no coverage");
    std::vector<Candidate> host(static_cast<std::size_t>(n));std::vector<U64> visited(in.tasks.size());
    if(n)check(cudaMemcpy(host.data(),hits.p,host.size()*sizeof(Candidate),cudaMemcpyDeviceToHost),"candidate download");
    if(!visited.empty())check(cudaMemcpy(visited.data(),counts.p,visited.size()*sizeof(U64),cudaMemcpyDeviceToHost),"coverage download");
    print_result("gpu",in,host,visited,elapsed(start),ms/1000.0);return 0;
}catch(const std::exception& e){return failure(e);}}
