#include <cuda_runtime.h>
#include "stream_io.hpp"

inline void check(cudaError_t error,const char* operation) {
    if(error!=cudaSuccess)throw std::runtime_error(std::string(operation)+": "+cudaGetErrorString(error));
}
template<class T> struct Reusable {
    T* p=nullptr;std::size_t capacity=0;
    void reserve(std::size_t count) {
        count=std::max<std::size_t>(1,count);if(count<=capacity)return;
        T* replacement=nullptr;check(cudaMalloc(reinterpret_cast<void**>(&replacement),count*sizeof(T)),"buffer allocation");
        if(p)cudaFree(p);p=replacement;capacity=count;
    }
    ~Reusable(){if(p)cudaFree(p);}
};
__global__ void enumerate_stream(const Task* tasks,const Chunk* chunks,int mode,std::uint64_t cap,
                                Candidate* hits,U64* found,unsigned capacity,U64* counts) {
    const auto chunk=chunks[blockIdx.x];const auto task=tasks[chunk.task];U64 visited=0;
    for(std::uint64_t j=threadIdx.x;j<chunk.count;j+=blockDim.x) {
        ++visited;Candidate hit{};
        if(evaluate(task,chunk.task,chunk.first+j,mode,cap,hit)) {
            const auto position=atomicAdd(found,1ULL);if(position<capacity)hits[position]=hit;
        }
    }
    atomicAdd(counts+chunk.task,visited);
}

int main(int argc,char**argv) {
    try {
        protect_parent();
        const auto capacity=::capacity(argc,argv);
        check(cudaSetDevice(0),"select GPU");check(cudaFree(nullptr),"initialize GPU context");
        Reusable<Task> tasks;Reusable<Chunk> chunks;Reusable<Candidate> hits;Reusable<U64> found,counts;
        hits.reserve(capacity);found.reserve(1);
        cudaEvent_t begin,end;check(cudaEventCreate(&begin),"create event");check(cudaEventCreate(&end),"create event");
        std::cout<<"{\"ready\":true,\"backend\":\"gpu\",\"persistent\":true,\"reusable_buffers\":true}\n"<<std::flush;
        U64 previous=0,request=0;std::string payload;
        while(read_frame(request,payload,previous)) {
            try {
                const auto start=Clock::now();const auto in=parse_frame(payload);
                tasks.reserve(in.tasks.size());chunks.reserve(in.chunks.size());counts.reserve(in.tasks.size());
                if(!in.tasks.empty())check(cudaMemcpy(tasks.p,in.tasks.data(),in.tasks.size()*sizeof(Task),cudaMemcpyHostToDevice),"task upload");
                if(!in.chunks.empty())check(cudaMemcpy(chunks.p,in.chunks.data(),in.chunks.size()*sizeof(Chunk),cudaMemcpyHostToDevice),"chunk upload");
                check(cudaMemset(found.p,0,sizeof(U64)),"reset candidate count");
                if(!in.tasks.empty())check(cudaMemset(counts.p,0,in.tasks.size()*sizeof(U64)),"reset coverage counts");
                check(cudaEventRecord(begin),"begin event");
                if(!in.chunks.empty()) {
                    enumerate_stream<<<static_cast<unsigned>(in.chunks.size()),256>>>(tasks.p,chunks.p,in.mode,in.cap,hits.p,found.p,capacity,counts.p);
                    check(cudaGetLastError(),"enumeration launch");
                }
                check(cudaEventRecord(end),"end event");check(cudaEventSynchronize(end),"enumeration completion");
                float milliseconds=0;check(cudaEventElapsedTime(&milliseconds,begin,end),"kernel duration");
                U64 size=0;check(cudaMemcpy(&size,found.p,sizeof(U64),cudaMemcpyDeviceToHost),"candidate count download");
                if(size>capacity)throw std::runtime_error("candidate capacity exceeded; no coverage");
                std::vector<Candidate> output(static_cast<std::size_t>(size));std::vector<U64> visited(in.tasks.size());
                if(size)check(cudaMemcpy(output.data(),hits.p,output.size()*sizeof(Candidate),cudaMemcpyDeviceToHost),"candidate download");
                if(!visited.empty())check(cudaMemcpy(visited.data(),counts.p,visited.size()*sizeof(U64),cudaMemcpyDeviceToHost),"coverage download");
                const auto seconds=elapsed(start);
                frame_output(request,[&](){print_result("gpu",in,output,visited,seconds,milliseconds/1000.0);});
            } catch(const std::exception& error) {frame_output(request,[&](){failure(error);});}
        }
        cudaEventDestroy(begin);cudaEventDestroy(end);return 0;
    } catch(const std::exception& error) {std::cerr<<error.what()<<'\n';return 2;}
}
