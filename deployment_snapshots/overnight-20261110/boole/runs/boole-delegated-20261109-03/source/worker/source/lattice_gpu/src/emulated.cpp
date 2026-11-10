#include "io.hpp"
int main(int argc,char**argv){try{
    if(argc==2&&std::string(argv[1])=="--arithmetic"){
        const auto cases=read_arithmetic();std::vector<ArithmeticResult> out;for(auto c:cases)out.push_back(arithmetic(c));print_arithmetic("emulated",out);return 0;
    }
    const auto cap=capacity(argc,argv);const auto start=Clock::now();const auto in=read_input();std::vector<Candidate> hits;std::vector<U64> counts(in.tasks.size());
    for(const auto& chunk:in.chunks)for(std::uint64_t i=chunk.first;i<chunk.first+chunk.count;++i){
        ++counts[chunk.task];Candidate h{};
        if(evaluate(in.tasks[chunk.task],chunk.task,i,in.mode,in.cap,h)){
            if(hits.size()==cap)throw std::runtime_error("candidate capacity exceeded; no coverage");
            hits.push_back(h);
        }
    }
    print_result("emulated",in,hits,counts,elapsed(start),0);return 0;
}catch(const std::exception& e){return failure(e);}}
