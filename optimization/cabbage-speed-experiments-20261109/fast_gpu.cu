#include <cuda_runtime.h>
#include "source/lattice_gpu/src/stream_io.hpp"
#include "native_fast.hpp"
#include <sstream>
#ifndef EXPERIMENT
#define EXPERIMENT 0
#endif
struct RowChunk {unsigned task,axis;U64 first,count;};
inline void check(cudaError_t e,const char*s){if(e!=cudaSuccess)throw std::runtime_error(std::string(s)+": "+cudaGetErrorString(e));}
template<class T>struct Buffer {
    T*p=nullptr;std::size_t capacity=0;
    void reserve(std::size_t n){n=std::max<std::size_t>(n,1);if(n<=capacity)return;T*q=nullptr;check(cudaMalloc(reinterpret_cast<void**>(&q),n*sizeof(T)),"allocate");if(p)cudaFree(p);p=q;capacity=n;}
    ~Buffer(){if(p)cudaFree(p);}
};
__device__ inline void emit(Candidate h,Candidate*hits,U64*found,unsigned capacity){const auto i=atomicAdd(found,1ULL);if(i<capacity)hits[i]=h;}
__global__ void flat(const Task*tasks,const Chunk*chunks,int mode,U64 cap,Candidate*hits,U64*found,unsigned capacity,U64*counts,U64*examined) {
    const auto ch=chunks[blockIdx.x];const auto t=tasks[ch.task];U64 seen=0;
    for(U64 j=threadIdx.x;j<ch.count;j+=blockDim.x) {
        ++seen;const auto index=ch.first+j;Candidate hit{};bool yes;
        if(EXPERIMENT==0)yes=evaluate(t,ch.task,index,mode,cap,hit);
        else {
            auto rem=index;S64 n[3];for(int i=0;i<3;++i){const auto w=2*t.J[i]+1;n[i]=static_cast<S64>(rem%w)-static_cast<S64>(t.J[i]);rem/=w;}
            S64 v[3]={0,0,0};for(int col=0;col<3;++col)for(int i=0;i<3;++i)v[col]+=n[i]*t.U[3*i+col];
            yes=low_hit(t,ch.task,index,v[0],v[1],v[2],mode,cap,hit);
        }
        if(yes)emit(hit,hits,found,capacity);
    }
    atomicAdd(counts+ch.task,seen);atomicAdd(examined+ch.task,seen);
}
__global__ void rows(const Task*tasks,const RowChunk*chunks,int mode,U64 cap,Candidate*hits,U64*found,unsigned capacity,U64*counts,U64*examined) {
    const auto ch=chunks[blockIdx.x];const auto t=tasks[ch.task];const unsigned axis=ch.axis;
    const unsigned o0=(axis+1)%3,o1=(axis+2)%3,lane=threadIdx.x%32,warp=threadIdx.x/32;
    const U64 widths[3]={2*t.J[0]+1,2*t.J[1]+1,2*t.J[2]+1};
    const U64 factors[3]={1,widths[0],widths[0]*widths[1]};U64 accounted=0,seen=0;
    for(U64 row=ch.first+warp;row<ch.first+ch.count;row+=blockDim.x/32) {
        S64 n[3]={0,0,0};n[o0]=static_cast<S64>(row%widths[o0])-static_cast<S64>(t.J[o0]);
        n[o1]=static_cast<S64>(row/widths[o0])-static_cast<S64>(t.J[o1]);
        S64 base[3];for(int col=0;col<3;++col)base[col]=n[o0]*t.U[3*o0+col]+n[o1]*t.U[3*o1+col];
        S64 lo=-static_cast<S64>(t.J[axis]),hi=static_cast<S64>(t.J[axis]);
        if(lane==0)accounted+=widths[axis];
        if(!clip(t,base,axis,lo,hi))continue;
        const bool wheel=(EXPERIMENT==3||EXPERIMENT==5)&&!mode&&cap<125;
        const bool recurrence=(EXPERIMENT==4||EXPERIMENT==5)&&!mode;
        const unsigned slots=wheel?8:1;
        for(unsigned slot=0;slot<slots;++slot) {
            S64 first;const U64 stride=wheel?251:32;
            if(wheel) {
                const unsigned r=lane+32*slot;if(r>=251)continue;
                // Use a real point in the bounded row to avoid signed overflow
                // in residue representatives outside the certified coefficient box.
                const int lr=residue(lo);first=lo+(static_cast<int>(r)-lr+251)%251;
            }else first=lo+lane;
            if(first>hi)continue;
            S64 c=coordinate(t,base,axis,first,0),a=coordinate(t,base,axis,first,1),b=coordinate(t,base,axis,first,2);
            if(wheel&&!modular_near(c,a,b,cap))continue;
            Differences differences{};
            const U64 length=static_cast<U64>(hi-first)/stride+1;
            // Long-row version is explicit: measure its setup cost as well as
            // its benefit. An automatic crossover can be selected afterwards.
            if(recurrence)differences.initialize(c,a,b,t.U[3*axis],t.U[3*axis+1],t.U[3*axis+2],stride);
            for(U64 k=0;k<length;++k) {
                ++seen;const S64 value=first+static_cast<S64>(k*stride);
                c=coordinate(t,base,axis,value,0);a=coordinate(t,base,axis,value,1);b=coordinate(t,base,axis,value,2);
                const U64 index=(static_cast<U64>(value+static_cast<S64>(t.J[axis]))*factors[axis])
                    +static_cast<U64>(n[o0]+static_cast<S64>(t.J[o0]))*factors[o0]
                    +static_cast<U64>(n[o1]+static_cast<S64>(t.J[o1]))*factors[o1];
                Candidate hit{};bool yes=false;
                if(recurrence) {
                    if(near_low(differences.d[0],cap))yes=full_hit(t,ch.task,index,c,a,b,mode,cap,hit);
                    differences.advance();
                }else yes=low_hit(t,ch.task,index,c,a,b,mode,cap,hit);
                if(yes)emit(hit,hits,found,capacity);
            }
        }
    }
    atomicAdd(counts+ch.task,accounted);atomicAdd(examined+ch.task,seen);
}
int main(int argc,char**argv) {
 try {
    protect_parent();const auto capacity=::capacity(argc,argv);check(cudaSetDevice(0),"device");check(cudaFree(nullptr),"context");
    Buffer<Task>tasks;Buffer<Chunk>chunks;Buffer<RowChunk>rowchunks;Buffer<Candidate>hits;Buffer<U64>found,counts,examined;
    hits.reserve(capacity);found.reserve(1);examined.reserve(1);cudaEvent_t begin,end;check(cudaEventCreate(&begin),"event");check(cudaEventCreate(&end),"event");
    std::cout<<"{\"ready\":true,\"backend\":\"gpu\",\"persistent\":true,\"experiment\":"<<EXPERIMENT<<"}\n"<<std::flush;
    U64 previous=0,request=0;std::string payload;
    while(read_frame(request,payload,previous))try {
        const auto start=Clock::now();const auto in=parse_frame(payload);tasks.reserve(in.tasks.size());counts.reserve(in.tasks.size());examined.reserve(in.tasks.size());
        if(!in.tasks.empty())check(cudaMemcpy(tasks.p,in.tasks.data(),in.tasks.size()*sizeof(Task),cudaMemcpyHostToDevice),"upload");
        check(cudaMemset(found.p,0,sizeof(U64)),"reset");
        if(!in.tasks.empty())check(cudaMemset(examined.p,0,in.tasks.size()*sizeof(U64)),"reset");
        if(!in.tasks.empty())check(cudaMemset(counts.p,0,in.tasks.size()*sizeof(U64)),"reset");
        std::vector<RowChunk>rc;
        if(EXPERIMENT>=2) {
            for(unsigned i=0;i<in.tasks.size();++i){const auto&t=in.tasks[i];unsigned axis=0;for(unsigned j=1;j<3;++j)if(t.J[j]>t.J[axis])axis=j;
                const auto total=t.points/(2*t.J[axis]+1);for(U64 first=0;first<total;first+=256)rc.push_back({i,axis,first,std::min<U64>(256,total-first)});}
            rowchunks.reserve(rc.size());if(!rc.empty())check(cudaMemcpy(rowchunks.p,rc.data(),rc.size()*sizeof(RowChunk),cudaMemcpyHostToDevice),"rows upload");
        }else {chunks.reserve(in.chunks.size());if(!in.chunks.empty())check(cudaMemcpy(chunks.p,in.chunks.data(),in.chunks.size()*sizeof(Chunk),cudaMemcpyHostToDevice),"chunks upload");}
        check(cudaEventRecord(begin),"begin");
        if(EXPERIMENT>=2){if(!rc.empty())rows<<<static_cast<unsigned>(rc.size()),256>>>(tasks.p,rowchunks.p,in.mode,in.cap,hits.p,found.p,capacity,counts.p,examined.p);}
        else if(!in.chunks.empty())flat<<<static_cast<unsigned>(in.chunks.size()),256>>>(tasks.p,chunks.p,in.mode,in.cap,hits.p,found.p,capacity,counts.p,examined.p);
        check(cudaGetLastError(),"launch");check(cudaEventRecord(end),"end");check(cudaEventSynchronize(end),"sync");float ms=0;check(cudaEventElapsedTime(&ms,begin,end),"elapsed");
        U64 size=0;check(cudaMemcpy(&size,found.p,sizeof(U64),cudaMemcpyDeviceToHost),"found");
        if(size>capacity)throw std::runtime_error("candidate capacity");
        std::vector<Candidate>out(size);std::vector<U64>visited(in.tasks.size()),evaluated(in.tasks.size());
        if(size)check(cudaMemcpy(out.data(),hits.p,size*sizeof(Candidate),cudaMemcpyDeviceToHost),"hits");
        if(!visited.empty())check(cudaMemcpy(visited.data(),counts.p,visited.size()*sizeof(U64),cudaMemcpyDeviceToHost),"counts");
        if(!evaluated.empty())check(cudaMemcpy(evaluated.data(),examined.p,evaluated.size()*sizeof(U64),cudaMemcpyDeviceToHost),"evaluated counts");
        U64 seen=0;for(unsigned i=0;i<visited.size();++i){if(visited[i]!=in.tasks[i].points||evaluated[i]>visited[i])throw std::runtime_error("incomplete accounting");seen+=evaluated[i];}
        const auto seconds=elapsed(start);
        frame_output(request,[&](){
            std::cout<<"{\"backend\":\"gpu\",\"box_complete\":true,\"schema\":2,\"points_accounted\":"<<in.points
                <<",\"points_visited\":"<<seen<<",\"points_explicitly_evaluated\":"<<seen<<",\"points_exactly_excluded\":"<<in.points-seen
                <<",\"engine_seconds\":"<<seconds<<",\"kernel_seconds\":"<<ms/1000.<<",\"counts\":[";
            for(unsigned i=0;i<visited.size();++i){if(i)std::cout<<',';std::cout<<"{\"id\":"<<i<<",\"expected\":"<<in.tasks[i].points
                <<",\"accounted\":"<<visited[i]<<",\"visited\":"<<evaluated[i]<<",\"exactly_excluded\":"<<visited[i]-evaluated[i]<<'}';}
            std::cout<<"],\"hits\":[";for(unsigned i=0;i<out.size();++i){if(i)std::cout<<',';const auto&v=out[i];std::cout<<"{\"task\":"<<v.task<<",\"linear\":"<<v.linear<<",\"a\":"<<v.a<<",\"b\":"<<v.b<<",\"c\":"<<v.c<<'}';}
            std::cout<<"],\"coverage_accounting\":\"enumerated_or_exactly_excluded\"}";});
    }catch(const std::exception&e){frame_output(request,[&](){failure(e);});}
    cudaEventDestroy(begin);cudaEventDestroy(end);return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
