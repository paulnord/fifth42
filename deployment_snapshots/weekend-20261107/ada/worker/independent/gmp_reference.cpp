// Independent packet walk: no project headers, limb arithmetic or evaluator.
#include <gmpxx.h>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

int main() {
  try {
    const auto begin=std::chrono::steady_clock::now();
    std::string magic;int mode;unsigned long cap;unsigned count;
    if(!(std::cin>>magic>>mode>>cap>>count)||magic!="LATTICE_GPU_V1"||mode<0||mode>1||count>4096)
      throw std::runtime_error("header");
    std::vector<unsigned long> visited;std::vector<std::string> hits;
    unsigned long total=0;
    for(unsigned task=0;task<count;++task) {
      unsigned id;long low,high;std::array<long,3> j;std::array<std::array<long,3>,3> u;
      if(!(std::cin>>id>>low>>high>>j[0]>>j[1]>>j[2])||id!=task)throw std::runtime_error("task");
      for(auto& row:u)for(auto& x:row)if(!(std::cin>>x))throw std::runtime_error("transform");
      unsigned long volume=1;
      for(auto bound:j){if(bound<0||bound>10000000)throw std::runtime_error("bound");volume*=2*bound+1;}
      if(volume>10000000||total+volume>50000000)throw std::runtime_error("work limit");
      unsigned long linear=0;
      for(long n2=-j[2];n2<=j[2];++n2)for(long n1=-j[1];n1<=j[1];++n1)for(long n0=-j[0];n0<=j[0];++n0,++linear) {
        std::array<__int128,3> v{};
        for(int col=0;col<3;++col)v[col]=(__int128)n0*u[0][col]+(__int128)n1*u[1][col]+(__int128)n2*u[2][col];
        if(v[0]<low||v[0]>high||v[1]<1||v[1]>v[2]||v[2]>=v[0])continue;
        const long c=v[0],a=v[1],b=v[2];mpz_class ap,bp,cp;
        mpz_ui_pow_ui(ap.get_mpz_t(),a,5);mpz_ui_pow_ui(bp.get_mpz_t(),b,5);mpz_ui_pow_ui(cp.get_mpz_t(),c,5);
        const mpz_class residual=ap+bp-cp;
        const mpz_class limit=mode?mpz_class(5)*c*c:mpz_class(cap);
        if(residual < -limit || residual>limit)continue;
        hits.push_back("{\"task\":"+std::to_string(task)+",\"linear\":"+std::to_string(linear)+
          ",\"a\":"+std::to_string(a)+",\"b\":"+std::to_string(b)+",\"c\":"+std::to_string(c)+"}");
      }
      if(linear!=volume)throw std::runtime_error("walk count");
      visited.push_back(linear);total+=linear;
    }
    std::string extra;if(std::cin>>extra)throw std::runtime_error("extra input");
    const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
    std::cout<<"{\"backend\":\"emulated\",\"box_complete\":true,\"points_visited\":"<<total<<
      ",\"engine_seconds\":"<<seconds<<",\"kernel_seconds\":0,\"counts\":[";
    for(unsigned i=0;i<visited.size();++i){if(i)std::cout<<',';std::cout<<"{\"id\":"<<i<<",\"expected\":"<<visited[i]<<",\"visited\":"<<visited[i]<<'}';}
    std::cout<<"],\"hits\":[";for(unsigned i=0;i<hits.size();++i){if(i)std::cout<<',';std::cout<<hits[i];}
    std::cout<<"]}\n";
  } catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}
}
