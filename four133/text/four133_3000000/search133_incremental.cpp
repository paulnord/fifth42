#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#include <sys/resource.h>
using u64=uint64_t;using u128=__uint128_t;
constexpr int Q=1597,E=133,D=4206930;
u64 power(u64 a,int e,u64 m){u64 r=1;for(;e;e>>=1,a=u64((u128)a*a%m))if(e&1)r=u64((u128)r*a%m);return r;}
u64 subtract(u64 a,u64 b,u64 m){return a>=b?a-b:a+m-b;}
u64 add(u64 a,u64 b,u64 m){u64 s=a+b;return s>=m?s-m:s;}
int modq(int a){a%=Q;return a<0?a+Q:a;}
int label(u64 p,int sign){if(sign<0)p=p?Q-p:0;return p==1?0:p==325?1:p==1312?2:-1;}
int type(int a,int b){if(a<0||b<0)return -1;if(a>b)std::swap(a,b);return a==0?(b==0?0:b==1?1:2):(a==1&&b==2?3:-1);}
struct Entry{u64 value;int base;bool operator<(const Entry&b)const{return value<b.value||(value==b.value&&base<b.base);}};
int main(int argc,char**argv){
 if(argc!=8&&argc!=9){std::cerr<<"Usage: search branch bound previous_bound modulus start_h end_h source_sha [TEST_ONLY_base_sum]\n";return 2;}
 std::string branch=argv[1],sha=argv[7];int B=std::stoi(argv[2]),old=std::stoi(argv[3]),start=std::stoi(argv[5]),end=std::stoi(argv[6]);u64 m=std::stoull(argv[4]);bool pair22=branch=="22",negative=branch=="31neg",test=argc==9;
 if(!pair22&&branch!="31pos"&&!negative)throw std::runtime_error("invalid branch");
 if(B<44||B>4000000||old<0||old>=B||m<=42||m>(u64(1)<<63)||sha.size()!=64)throw std::runtime_error("unsupported configuration");
 if(test&&pair22&&std::stoi(argv[8])!=42)throw std::runtime_error("22 test sum must equal 42");
 int S=pair22?42:negative?D-42:D+42;if(test)S=std::stoi(argv[8]);if(S<2)throw std::runtime_error("invalid positive normalized sum");
 int H=0;if(pair22){while(66LL*(H+1)*(H+1)<42LL*B)H++;}else{H=(2*B)/135;H=std::min(H,(2*B-S)/3);}
 if(start<1||end>H||start>end)throw std::runtime_error("invalid gap interval");
 rlimit lim{1024ULL*1024*1024,1024ULL*1024*1024};if(setrlimit(RLIMIT_AS,&lim))throw std::runtime_error("memory limit failed");
 auto t0=std::chrono::steady_clock::now();std::vector<u64>p(B+1);for(int x=1;x<=B;x++)p[x]=power(x,E,m);
 std::array<int,Q>P,N;for(int r=0;r<Q;r++){u64 x=power(r,E,Q);P[r]=label(x,negative?-1:1);N[r]=label(x?Q-x:0,negative?-1:1);}
 std::cout<<"START version=1 branch="<<branch<<" bound="<<B<<" previous_bound="<<old<<" modulus="<<m<<" normalized_sum="<<S<<" normalized_target="<<(negative?-42:42)<<" max_gap="<<H<<" start="<<start<<" end="<<end<<" test_mode="<<test<<" source_sha="<<sha<<std::endl;
 u64 leftTotal=0,rightTotal=0,rawTotal=0,canonicalTotal=0,distinctTotal=0;
 for(int h=start;h<=end;h++){
  std::array<std::vector<Entry>,4>L,R;u64 nL=0,nR=0,raw=0,canonical=0,distinct=0;
  int leftLow=pair22?1:(S+h+1)/2,leftHigh=pair22?B-h-42:std::min(B-h,S+h-1);
  int rightLow=std::max(pair22?1:(S+h+1)/2,old-h+1),rightHigh=B-h;
  for(int r=0;r<Q;r++){
   int lt=pair22?type(P[(r+h+42)%Q],N[r]):type(P[modq(S+h-r)],P[r]);
   int rt=type(P[r],N[(r+h)%Q]);
   if(lt>=0)for(int x=leftLow+modq(r-modq(leftLow));x<=leftHigh;x+=Q){u64 key=pair22?subtract(p[x+h+42],p[x],m):add(p[S+h-x],p[x],m);L[lt].push_back({key,x});nL++;}
   if(rt>=0)for(int x=rightLow+modq(r-modq(rightLow));x<=rightHigh;x+=Q){u64 key=subtract(p[x+h],p[x],m);key=negative?subtract(key,42,m):add(key,42,m);R[3-rt].push_back({key,x});nR++;}
  }
  for(int z=0;z<4;z++){
   auto&l=L[z];auto&r=R[z];std::sort(l.begin(),l.end());std::sort(r.begin(),r.end());size_t i=0,j=0;
   while(i<l.size()&&j<r.size()){
    if(l[i].value<r[j].value){i++;continue;}if(r[j].value<l[i].value){j++;continue;}
    size_t ie=i+1,je=j+1;while(ie<l.size()&&l[ie].value==l[i].value)ie++;while(je<r.size()&&r[je].value==r[j].value)je++;
    for(size_t x=i;x<ie;x++)for(size_t y=j;y<je;y++){
     raw++;int a,b,c,d;if(pair22){c=l[x].base;a=c+h+42;b=r[y].base;d=b+h;if(a>b)continue;}else{b=l[x].base;a=S+h-b;c=r[y].base;d=c+h;if(b>c)continue;}
     canonical++;bool isDistinct=pair22?a<b:(a<b&&b<c);distinct+=isDistinct;
     if(pair22){c=-c;d=-d;}else if(negative){a=-a;b=-b;c=-c;}else d=-d;
     std::cout<<"CANDIDATE branch="<<branch<<" h="<<h<<" a="<<a<<" b="<<b<<" c="<<c<<" d="<<d<<" distinct="<<isDistinct<<" residue="<<l[x].value<<"\n";
    }i=ie;j=je;
   }
  }
  leftTotal+=nL;rightTotal+=nR;rawTotal+=raw;canonicalTotal+=canonical;distinctTotal+=distinct;rusage ru{};getrusage(RUSAGE_SELF,&ru);
  std::cout<<"CHECKPOINT branch="<<branch<<" h="<<h<<" left="<<nL<<" right="<<nR<<" raw="<<raw<<" canonical="<<canonical<<" distinct="<<distinct<<" wall="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()<<" rss_kib="<<ru.ru_maxrss<<std::endl;
 }
 std::cout<<"CHUNK_DONE branch="<<branch<<" bound="<<B<<" previous_bound="<<old<<" modulus="<<m<<" start="<<start<<" end="<<end<<" left="<<leftTotal<<" right="<<rightTotal<<" raw="<<rawTotal<<" canonical="<<canonicalTotal<<" distinct="<<distinctTotal<<std::endl;
}
