#include "native_fast.hpp"
#include <iostream>
int main(){
    S64 c,a,b,uc,ua,ub;U64 stride,steps,cap;
    while(std::cin>>c>>a>>b>>uc>>ua>>ub>>stride>>steps>>cap){
        if(steps>1000)return 2;
        Differences d{};d.initialize(c,a,b,uc,ua,ub,stride);
        for(U64 k=0;k<steps;++k){std::cout<<d.d[0]<<' '<<near_low(d.d[0],cap)<<'\n';d.advance();}
    }
}
