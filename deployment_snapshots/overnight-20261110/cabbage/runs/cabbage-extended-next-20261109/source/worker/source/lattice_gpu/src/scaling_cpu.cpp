#include "stream_io.hpp"
#include <atomic>
#include <mutex>
#include <thread>

int main(int argc,char**argv) {
    try {
        protect_parent();
        unsigned threads=1,capacity=65536;
        for(int i=1;i<argc;i+=2) {
            if(i+1>=argc)throw std::runtime_error("missing option value");
            const std::string key=argv[i];
            if(key=="--threads")threads=parse_unsigned(argv[i+1],16);
            else if(key=="--capacity")capacity=parse_unsigned(argv[i+1],1000000);
            else throw std::runtime_error("unknown option");
        }
        std::cout<<"{\"ready\":true,\"backend\":\"emulated\",\"persistent\":true,\"threads\":"<<threads<<"}\n"<<std::flush;
        U64 previous=0,request=0;std::string payload;
        while(read_frame(request,payload,previous)) {
            try {
                const auto start=Clock::now();const auto in=parse_frame(payload);
                std::vector<std::atomic<U64>> counts(in.tasks.size());for(auto& x:counts)x.store(0);
                std::atomic<std::size_t> next{0};std::atomic<U64> found{0};
                std::vector<Candidate> hits;std::mutex mutex;
                const auto worker=[&]() {
                    std::vector<Candidate> local;
                    for(;;) {
                        const auto index=next.fetch_add(1);if(index>=in.chunks.size())break;
                        const auto chunk=in.chunks[index];U64 visited=0;
                        for(std::uint64_t j=0;j<chunk.count;++j) {
                            ++visited;Candidate hit{};
                            if(evaluate(in.tasks[chunk.task],chunk.task,chunk.first+j,in.mode,in.cap,hit)) {
                                if(found.fetch_add(1)<capacity)local.push_back(hit);
                            }
                        }
                        counts[chunk.task].fetch_add(visited);
                    }
                    std::lock_guard<std::mutex> lock(mutex);hits.insert(hits.end(),local.begin(),local.end());
                };
                std::vector<std::thread> pool;
                const auto active=std::min<std::size_t>(threads,std::max<std::size_t>(1,in.chunks.size()));
                for(std::size_t i=0;i<active;++i)pool.emplace_back(worker);
                for(auto& thread:pool)thread.join();
                if(found.load()>capacity)throw std::runtime_error("candidate capacity exceeded; no coverage");
                std::vector<U64> visited;visited.reserve(counts.size());for(auto& x:counts)visited.push_back(x.load());
                const auto seconds=elapsed(start);
                frame_output(request,[&](){print_result("emulated",in,hits,visited,seconds,0);});
            } catch(const std::exception& error) {frame_output(request,[&](){failure(error);});}
        }
        return 0;
    } catch(const std::exception& error) {std::cerr<<error.what()<<'\n';return 2;}
}
