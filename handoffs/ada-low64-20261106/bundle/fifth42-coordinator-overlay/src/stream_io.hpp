#pragma once
#include "io.hpp"
#include <sstream>
#include <csignal>
#include <sys/prctl.h>
#include <unistd.h>

constexpr std::size_t MAX_FRAME_BYTES=16*1024*1024;

inline void protect_parent() {
    const auto parent=getppid();
    if(parent<=1||prctl(PR_SET_PDEATHSIG,SIGKILL)!=0||getppid()!=parent)
        throw std::runtime_error("engine parent-lifetime guard failed");
}

inline bool read_frame(U64& request,std::string& payload,U64& previous) {
    std::string line;
    if(!std::getline(std::cin,line))return false;
    if(line=="QUIT")return false;
    std::istringstream header(line);
    std::string command,extra;U64 bytes=0;
    if(!(header>>command>>request>>bytes)||command!="RUN"||(header>>extra)
       ||request<=previous||bytes>MAX_FRAME_BYTES)
        throw std::runtime_error("invalid request frame");
    previous=request;payload.resize(static_cast<std::size_t>(bytes));
    if(bytes&&!std::cin.read(&payload[0],static_cast<std::streamsize>(bytes)))
        throw std::runtime_error("incomplete request frame");
    return true;
}

inline Input parse_frame(const std::string& payload) {
    std::istringstream stream(payload);
    auto* original=std::cin.rdbuf(stream.rdbuf());
    try {
        auto input=read_input();std::cin.rdbuf(original);std::cin.clear();return input;
    } catch(...) {std::cin.rdbuf(original);std::cin.clear();throw;}
}

template<class Function> inline void frame_output(U64 request,Function function) {
    std::ostringstream stream;auto* original=std::cout.rdbuf(stream.rdbuf());
    try {function();std::cout.rdbuf(original);}
    catch(...) {std::cout.rdbuf(original);throw;}
    auto text=stream.str();while(!text.empty()&&(text.back()=='\n'||text.back()=='\r'))text.pop_back();
    if(text.empty()||text.front()!='{'||text.back()!='}')throw std::runtime_error("invalid engine response");
    std::cout<<"{\"request_id\":"<<request<<','<<text.substr(1)<<'\n'<<std::flush;
}

inline unsigned parse_unsigned(const std::string& value,unsigned maximum) {
    std::size_t used=0;const auto n=std::stoull(value,&used);
    if(used!=value.size()||n<1||n>maximum)throw std::runtime_error("option outside supported range");
    return static_cast<unsigned>(n);
}
