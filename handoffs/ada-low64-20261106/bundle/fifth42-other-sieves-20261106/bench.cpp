// Private bounded experiment only. Does not edit any search engine or live run.
#include "../fifth42-coordinator-overlay/src/io.hpp"
#include <array>
#include <set>
#include <tuple>
#include <sstream>
#include <iomanip>
#include <vector>
using Hit=std::tuple<unsigned,U64,S64,S64,S64>;
std::vector<S64> targets; bool interval=false; U64 cap=42;
constexpr int mods[4]={11,25,31,61};
std::array<std::array<U64,61>,4> powers{},mask{};
U64 fifthlow(U64 x){U64 s=x*x;return s*s*x;}
bool lowok(U64 r,U64 bits){U64 m=bits==64?~U64{0}:((U64{1}<<bits)-1);r&=m;if(interval)return r<=cap||r>=((-cap)&m);for(auto t:targets)if(r==(static_cast<U64>(t)&m))return true;return false;}
bool modok(S64 a,S64 b,S64 c,bool shared,bool eleven){U64 possible=~U64{0};for(unsigned k=eleven?0:1;k<4;++k){auto m=mods[k];auto r=(powers[k][a%m]+powers[k][b%m]+m-powers[k][c%m])%m;U64 q=mask[k][r];if(!q)return false;if(shared){possible&=q;if(!possible)return false;}}return true;}
bool factorok(S64 a,S64 b,S64 c){U64 s=a+b,x=c%s;U64 x2=static_cast<unsigned __int128>(x)*x%s;U64 x4=static_cast<unsigned __int128>(x2)*x2%s;U64 x5=static_cast<unsigned __int128>(x4)*x%s;for(auto t:targets)if((x5+(t>=0?static_cast<U64>(t):s-static_cast<U64>(-t)%s))%s==0)return true;return false;}
template<int MODE>bool test(const Task&t,unsigned task,U64 index,Candidate&out){auto rem=index;S64 n[3];for(int i=0;i<3;++i){auto w=2*t.J[i]+1;n[i]=static_cast<S64>(rem%w)-static_cast<S64>(t.J[i]);rem/=w;}S64 v[3]={};for(int col=0;col<3;++col)for(int i=0;i<3;++i)v[col]+=n[i]*t.U[3*i+col];auto c=v[0],a=v[1],b=v[2];if(c<t.cmin||c>t.cmax||a<1||a>b||b>=c)return false;
if constexpr(MODE>=1&&MODE<=3)if(!lowok(fifthlow(a)+fifthlow(b)-fifthlow(c),MODE==1?64:MODE==2?32:16))return false;
if constexpr(MODE>=4&&MODE<=6)if(!modok(a,b,c,MODE>=5,MODE==6))return false;
if constexpr(MODE==7)if(!factorok(a,b,c))return false;
auto r=fifth64(a)+fifth64(b)+(-fifth64(c));bool hit=false;if(interval){auto lim=I192::from_i64(static_cast<S64>(cap));hit=!(r<(-lim)||lim<r);}else for(auto t:targets)if(r==I192::from_i64(t))hit=true;if(hit){out={task,index,a,b,c};return true;}return false;}
using Fn=bool(*)(const Task&,unsigned,U64,Candidate&);const Fn fs[]={test<0>,test<1>,test<2>,test<3>,test<4>,test<5>,test<6>,test<7>};const char* names[]={"baseline","low64","low32","low16","mods_relaxed","mods_same_target","mods_same_target_with11","factor_sum"};
int main(int argc,char**argv){try{if(argc<2)throw std::runtime_error("target csv or interval cap");std::string arg=argv[1];if(arg=="interval"){interval=true;cap=std::stoull(argv[2]);}else{std::istringstream ss(arg);std::string v;while(std::getline(ss,v,','))targets.push_back(std::stoll(v));}int reps=argc>3?std::stoi(argv[3]):9;auto in=read_input();for(unsigned k=0;k<4;++k){int m=mods[k];for(int x=0;x<m;++x){U64 p=1;for(int j=0;j<5;++j)p=p*x%m;powers[k][x]=p;}for(unsigned j=0;j<targets.size();++j){auto t=targets[j];mask[k][(t%m+m)%m]|=U64{1}<<j;}}
unsigned nm=interval?4:8;std::vector<std::set<Hit>> hits(nm);std::array<U64,8> survivors{};U64 shape=0,all=0;
for(unsigned id=0;id<in.tasks.size();++id){auto&t=in.tasks[id];all+=t.points;for(U64 ix=0;ix<t.points;++ix){for(unsigned mode=0;mode<nm;++mode){Candidate h{};if(fs[mode](t,id,ix,h))hits[mode].emplace(id,ix,h.a,h.b,h.c);}auto rem=ix;S64 n[3];for(int i=0;i<3;++i){auto w=2*t.J[i]+1;n[i]=static_cast<S64>(rem%w)-static_cast<S64>(t.J[i]);rem/=w;}S64 v[3]={};for(int col=0;col<3;++col)for(int i=0;i<3;++i)v[col]+=n[i]*t.U[3*i+col];auto c=v[0],a=v[1],b=v[2];if(c<t.cmin||c>t.cmax||a<1||a>b||b>=c)continue;++shape;++survivors[0];auto r=fifthlow(a)+fifthlow(b)-fifthlow(c);for(unsigned mode=1;mode<4;++mode)survivors[mode]+=lowok(r,mode==1?64:mode==2?32:16);if(!interval){survivors[4]+=modok(a,b,c,false,false);survivors[5]+=modok(a,b,c,true,false);survivors[6]+=modok(a,b,c,true,true);survivors[7]+=factorok(a,b,c);}}}for(unsigned m=1;m<nm;++m)if(hits[m]!=hits[0])throw std::runtime_error(std::string("hit mismatch ")+names[m]);
std::array<std::vector<double>,8> times;U64 checksum=0;for(int rep=-1;rep<reps;++rep)for(unsigned off=0;off<nm;++off){unsigned mode=(off+rep+1)%nm;auto start=Clock::now();U64 sum=0;for(unsigned id=0;id<in.tasks.size();++id){auto&t=in.tasks[id];for(U64 i=0;i<t.points;++i){Candidate h{};if(fs[mode](t,id,i,h))sum+=h.linear+1;}}auto sec=elapsed(start);checksum+=sum;if(rep>=0)times[mode].push_back(sec);}
std::cout<<std::setprecision(12)<<"{\"all\":"<<all<<",\"shape\":"<<shape<<",\"equal_hit_sets\":true,\"hit_records\":"<<hits[0].size()<<",\"checksum\":"<<checksum<<",\"variants\":{";for(unsigned m=0;m<nm;++m){if(m)std::cout<<',';auto&t=times[m];std::sort(t.begin(),t.end());std::cout<<quote(names[m])<<":{\"exact_tests\":"<<survivors[m]<<",\"median_seconds\":"<<t[t.size()/2]<<",\"min_seconds\":"<<t.front()<<",\"max_seconds\":"<<t.back()<<'}';}std::cout<<"},\"hits\":[";bool first=true;for(auto&h:hits[0]){auto[id,i,a,b,c]=h;if(!first)std::cout<<',';first=false;std::cout<<'['<<id<<','<<i<<','<<a<<','<<b<<','<<c<<']';}std::cout<<"]}\n";
}catch(std::exception&e){std::cerr<<e.what()<<'\n';return 2;}}
