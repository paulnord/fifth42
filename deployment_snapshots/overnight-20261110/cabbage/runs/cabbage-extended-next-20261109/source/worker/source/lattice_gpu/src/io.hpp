#pragma once
#include "kernel.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

struct Input { int mode; std::uint64_t cap,points=0; std::vector<Task> tasks; std::vector<Chunk> chunks; };
inline std::string quote(const std::string& s) {
    std::string r="\"";for(char c:s){if(c=='\\'||c=='\"')r+='\\';if(c=='\n')r+="\\n";else if(c=='\r')r+="\\r";else if(c=='\t')r+="\\t";else r+=c;}return r+'\"';
}
inline void no_trailing(){std::string extra;if(std::cin>>extra)throw std::runtime_error("trailing input");}
inline Input read_input() {
    Input in{};std::string magic;unsigned n;
    if(!(std::cin>>magic>>in.mode>>in.cap>>n)||magic!="LATTICE_GPU_V1"||in.mode<0||in.mode>1||in.cap>static_cast<std::uint64_t>(INT64_MAX)||n>MAX_TASKS||(in.mode&&in.cap))throw std::runtime_error("invalid packet header");
    for(unsigned i=0;i<n;++i){
        Task t{};unsigned id;
        if(!(std::cin>>id>>t.cmin>>t.cmax>>t.J[0]>>t.J[1]>>t.J[2])||id!=i)throw std::runtime_error("invalid task header");
        for(auto& u:t.U)if(!(std::cin>>u)||u==INT64_MIN)throw std::runtime_error("invalid transform");
        if(t.cmin<1||t.cmax<t.cmin||static_cast<std::uint64_t>(t.cmax)>LATTICE_MAX_BASE)throw std::runtime_error("invalid base range");
        unsigned __int128 points=1;
        for(auto j:t.J){if(j>MAX_PATCH_POINTS)throw std::runtime_error("invalid coefficient bound");points*=2*j+1;}
        if(points>MAX_PATCH_POINTS)throw std::runtime_error("patch point budget exceeded");
        t.points=static_cast<std::uint64_t>(points);
        for(int col=0;col<3;++col){unsigned __int128 maximum=0;for(int k=0;k<3;++k){const auto u=t.U[3*k+col];maximum+=static_cast<unsigned __int128>(t.J[k])*static_cast<std::uint64_t>(u<0?-u:u);}if(maximum>INT64_MAX)throw std::runtime_error("transform may overflow");}
        in.points+=t.points;if(in.points>MAX_PACKET_POINTS)throw std::runtime_error("packet point budget exceeded");
        in.tasks.push_back(t);
        for(std::uint64_t first=0;first<t.points;first+=65536)in.chunks.push_back({i,first,std::min<std::uint64_t>(65536,t.points-first)});
    }
    no_trailing();return in;
}
inline std::vector<ArithmeticCase> read_arithmetic() {
    std::string magic;unsigned n;if(!(std::cin>>magic>>n)||magic!="ARITH_V1"||n>4096)throw std::runtime_error("invalid arithmetic header");
    std::vector<ArithmeticCase> cases(n);
    for(auto& c:cases)if(!(std::cin>>c.a>>c.b)||c.a< -static_cast<S64>(LATTICE_MAX_BASE)||c.b< -static_cast<S64>(LATTICE_MAX_BASE)||c.a>static_cast<S64>(LATTICE_MAX_BASE)||c.b>static_cast<S64>(LATTICE_MAX_BASE))throw std::runtime_error("arithmetic base range");
    no_trailing();return cases;
}
inline void print_value(I192 x){std::cout<<'['<<x.lo<<','<<x.hi.lo<<','<<x.hi.hi<<']';}
inline void print_arithmetic(const char* backend,const std::vector<ArithmeticResult>& rows) {
    std::cout<<"{\"backend\":"<<quote(backend)<<",\"arithmetic\":[";
    for(std::size_t i=0;i<rows.size();++i){if(i)std::cout<<',';const auto& r=rows[i];std::cout<<"{\"p\":";print_value(r.p);std::cout<<",\"q\":";print_value(r.q);std::cout<<",\"sum\":";print_value(r.sum);std::cout<<",\"negative\":";print_value(r.negative);std::cout<<",\"square5\":";print_value(r.square5);std::cout<<",\"lt\":"<<r.lt<<",\"eq\":"<<r.eq<<'}';}
    std::cout<<"]}\n";
}
inline unsigned capacity(int argc,char**argv) {
    if(argc==1)return 65536;
    if(argc!=3||std::string(argv[1])!="--capacity")throw std::runtime_error("usage: engine [--capacity N] or --arithmetic");
    std::size_t used=0;const auto n=std::stoull(argv[2],&used);
    if(used!=std::string(argv[2]).size()||n<1||n>1000000)throw std::runtime_error("invalid capacity");
    return static_cast<unsigned>(n);
}
inline void print_result(const char* backend,const Input& in,const std::vector<Candidate>& hits,const std::vector<U64>& counts,double engine_seconds,double kernel_seconds) {
    if(counts.size()!=in.tasks.size())throw std::runtime_error("missing task counts");
    U64 total=0;for(std::size_t i=0;i<counts.size();++i){if(counts[i]!=in.tasks[i].points)throw std::runtime_error("incomplete task");total+=counts[i];}
    if(total!=in.points)throw std::runtime_error("incomplete packet");
    std::cout<<"{\"backend\":"<<quote(backend)<<",\"box_complete\":true,\"points_visited\":"<<total<<",\"engine_seconds\":"<<engine_seconds<<",\"kernel_seconds\":"<<kernel_seconds<<",\"counts\":[";
    for(std::size_t i=0;i<counts.size();++i){if(i)std::cout<<',';std::cout<<"{\"id\":"<<i<<",\"expected\":"<<in.tasks[i].points<<",\"visited\":"<<counts[i]<<'}';}
    std::cout<<"],\"hits\":[";
    for(std::size_t i=0;i<hits.size();++i){if(i)std::cout<<',';const auto& h=hits[i];std::cout<<"{\"task\":"<<h.task<<",\"linear\":"<<h.linear<<",\"a\":"<<h.a<<",\"b\":"<<h.b<<",\"c\":"<<h.c<<'}';}
    std::cout<<"]}\n";
}
using Clock=std::chrono::steady_clock;
inline double elapsed(Clock::time_point t){return std::chrono::duration<double>(Clock::now()-t).count();}
inline int failure(const std::exception& e){std::cout<<"{\"box_complete\":false,\"error\":"<<quote(e.what())<<"}\n";return 2;}
