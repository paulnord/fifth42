// Isolated single-core target-aware screening experiment; source kernel untouched.
#include "../fifth42-coordinator-overlay/src/io.hpp"
#include <numeric>
#include <array>
#include <set>
#include <tuple>
#include <sstream>
#include <iomanip>

using Hit=std::tuple<unsigned,U64,S64,S64,S64>;
std::vector<S64> targets;
std::array<std::array<unsigned char,61>,3> powers{},wanted{};
constexpr int mods[3]={25,31,61};
std::vector<unsigned> wheel;
S64 max_target=0;
bool primitive_only=false;
U64 absu(S64 n){return static_cast<U64>(n<0?-n:n);}
U64 gcd3(const S64* n){return std::gcd(std::gcd(absu(n[0]),absu(n[1])),absu(n[2]));}
bool allowed(U64 g){
 if(primitive_only)return g==1;
 if(g==1)return true;
 if(g==0){for(auto t:targets)if(t==0)return true;return false;}
 U64 v=1;
 for(unsigned i=0;i<5;++i){if(v>static_cast<U64>(max_target)/g){for(auto t:targets)if(t==0)return true;return false;}v*=g;}
 for(auto t:targets)if(t%static_cast<S64>(v)==0)return true;
 return false;
}
bool wheel_ok(const S64* n){for(auto p:wheel)if(n[0]%p==0&&n[1]%p==0&&n[2]%p==0)return false;return true;}
bool mod_ok(S64 a,S64 b,S64 c){
 for(unsigned k=0;k<3;++k){auto m=mods[k];auto r=(powers[k][a%m]+powers[k][b%m]+m-powers[k][c%m])%m;if(!wanted[k][r])return false;}
 return true;
}
struct Stats{U64 all=0,nonprimitive=0,shape=0,shape_nonprimitive=0,mods=0,mods_nonprimitive=0,exact=0,hits=0;};

template<int MODE> bool test(const Task& t,unsigned task,U64 index,Candidate& out){
 auto remainder=index;S64 n[3];
 for(int i=0;i<3;++i){auto width=2*t.J[i]+1;n[i]=static_cast<S64>(remainder%width)-static_cast<S64>(t.J[i]);remainder/=width;}
 if constexpr(MODE==1)if(!allowed(gcd3(n)))return false;
 if constexpr(MODE==3)if(!wheel_ok(n))return false;
 S64 v[3]={0,0,0};
 for(int col=0;col<3;++col)for(int i=0;i<3;++i)v[col]+=n[i]*t.U[3*i+col];
 const auto c=v[0],a=v[1],b=v[2];
 if(c<t.cmin||c>t.cmax||a<1||a>b||b>=c)return false;
 if constexpr(MODE==2||MODE==7)if(!allowed(gcd3(n)))return false;
 if constexpr(MODE==4)if(!wheel_ok(n))return false;
 if constexpr(MODE==5||MODE==6||MODE==7)if(!mod_ok(a,b,c))return false;
 if constexpr(MODE==6)if(!allowed(gcd3(n)))return false;
 const auto r=fifth64(a)+fifth64(b)+(-fifth64(c));
 for(auto target:targets)if(r==I192::from_i64(target)){out={task,index,a,b,c};return true;}
 return false;
}
using Fn=bool(*)(const Task&,unsigned,U64,Candidate&);
const Fn functions[]={test<0>,test<1>,test<2>,test<3>,test<4>,test<5>,test<6>,test<7>};
const char* names[]={"baseline_target","early_gcd","shape_gcd","early_wheel2357","shape_wheel2357","mod_only","mod_then_gcd","gcd_then_mod"};

int main(int argc,char**argv){try{
 if(argc<2)throw std::runtime_error("target csv required");
 std::istringstream ts(argv[1]);std::string val;while(std::getline(ts,val,',')){auto t=std::stoll(val);targets.push_back(t);max_target=std::max(max_target,static_cast<S64>(absu(t)));}
 primitive_only=std::all_of(targets.begin(),targets.end(),[](S64 t){return t==42||t==-42;});
 int repeats=argc>2?std::stoi(argv[2]):7;
 auto in=read_input();
 for(unsigned k=0;k<3;++k){int m=mods[k];for(int x=0;x<m;++x){int p=1;for(int j=0;j<5;++j)p=p*x%m;powers[k][x]=static_cast<unsigned char>(p);}for(auto t:targets)wanted[k][(t%m+m)%m]=1;}
 for(unsigned p:{2,3,5,7}){bool valid=true;S64 p5=p*p*p*p*p;for(auto t:targets)if(t%p5==0)valid=false;if(valid)wheel.push_back(p);}
 Stats s;std::set<Hit> expected;
 for(unsigned id=0;id<in.tasks.size();++id){auto&t=in.tasks[id];for(U64 index=0;index<t.points;++index){
 ++s.all;auto rem=index;S64 n[3];for(int i=0;i<3;++i){auto w=2*t.J[i]+1;n[i]=static_cast<S64>(rem%w)-static_cast<S64>(t.J[i]);rem/=w;}
 auto g=gcd3(n);s.nonprimitive+=(g!=1);S64 v[3]={};for(int c=0;c<3;++c)for(int i=0;i<3;++i)v[c]+=n[i]*t.U[3*i+c];
 if(std::gcd(std::gcd(absu(v[0]),absu(v[1])),absu(v[2]))!=g)throw std::runtime_error("gcd mapping failure");
 auto c=v[0],a=v[1],b=v[2];if(c<t.cmin||c>t.cmax||a<1||a>b||b>=c)continue;
 ++s.shape;s.shape_nonprimitive+=(g!=1);if(mod_ok(a,b,c)){++s.mods;s.mods_nonprimitive+=(g!=1);}
 Candidate hit{};if(test<0>(t,id,index,hit))expected.emplace(id,index,hit.a,hit.b,hit.c);
 }}
 s.hits=expected.size();
 for(unsigned mode=1;mode<8;++mode){std::set<Hit> got;for(unsigned id=0;id<in.tasks.size();++id){auto&t=in.tasks[id];for(U64 i=0;i<t.points;++i){Candidate h{};if(functions[mode](t,id,i,h))got.emplace(id,i,h.a,h.b,h.c);}}if(got!=expected)throw std::runtime_error(std::string("hit mismatch: ")+names[mode]);}
 // Warm-up and rotated-order samples. Each sample traverses the unchanged box.
 std::array<std::vector<double>,8> times;U64 checksum=0;
 for(int rep=-1;rep<repeats;++rep)for(unsigned offset=0;offset<8;++offset){unsigned mode=(offset+static_cast<unsigned>(rep+1))%8;auto start=Clock::now();U64 local=0;for(unsigned id=0;id<in.tasks.size();++id){auto&t=in.tasks[id];for(U64 i=0;i<t.points;++i){Candidate h{};if(functions[mode](t,id,i,h))local+=h.linear+1;}}auto seconds=elapsed(start);checksum+=local;if(rep>=0)times[mode].push_back(seconds);}
 std::cout<<std::setprecision(12)<<"{\"all\":"<<s.all<<",\"nonprimitive\":"<<s.nonprimitive<<",\"shape\":"<<s.shape<<",\"shape_nonprimitive\":"<<s.shape_nonprimitive<<",\"mods\":"<<s.mods<<",\"mods_nonprimitive\":"<<s.mods_nonprimitive<<",\"hit_records\":"<<s.hits<<",\"all_variant_hit_sets_equal\":true,\"all_gcd_mappings_equal\":true,\"checksum\":"<<checksum<<",\"timings\":{";
 for(unsigned i=0;i<8;++i){if(i)std::cout<<',';std::sort(times[i].begin(),times[i].end());std::cout<<quote(names[i])<<":{\"median_seconds\":"<<times[i][times[i].size()/2]<<",\"min_seconds\":"<<times[i].front()<<",\"max_seconds\":"<<times[i].back()<<",\"samples\":[";for(unsigned k=0;k<times[i].size();++k){if(k)std::cout<<',';std::cout<<times[i][k];}std::cout<<"]}";}
 std::cout<<"},\"hits\":[";bool first=true;for(auto& h:expected){auto [id,i,a,b,c]=h;if(!first)std::cout<<',';first=false;std::cout<<'['<<id<<','<<i<<','<<a<<','<<b<<','<<c<<']';}std::cout<<"]}\n";
 }catch(std::exception&e){std::cerr<<e.what()<<'\n';return 2;}}
