#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <sys/resource.h>
using u64=uint64_t; using u128=__uint128_t;
constexpr int E=133,Q=1597;
#ifndef SEARCH_MODULUS
#define SEARCH_MODULUS 2305843009213693921ULL
#endif
constexpr u64 M=SEARCH_MODULUS;
u64 power(u64 a,int e,u64 m){u64 r=1;for(;e;e>>=1,a=static_cast<u64>((u128)a*a%m))if(e&1)r=static_cast<u64>((u128)r*a%m);return r;}
u64 sub(u64 a,u64 b){return a>=b?a-b:a+M-b;}
u64 add42(u64 a){return a>=M-42?a-(M-42):a+42;}
int label(u64 r){return r==1?0:r==325?1:r==1312?2:-1;}
int pairtype(int a,int b){if(a<0||b<0)return -1;if(a>b)std::swap(a,b);if(a==0&&b==0)return 0;if(a==0&&b==1)return 1;if(a==0&&b==2)return 2;if(a==1&&b==2)return 3;return -1;}
struct Entry {u64 value;int base;bool operator<(const Entry& b)const{return value<b.value||(value==b.value&&base<b.base);}};
struct Pattern{int residue,type;};
std::array<int,Q> pos,neg;
void labels(){for(int r=0;r<Q;r++){auto p=power(r,E,Q);pos[r]=label(p);neg[r]=label(p?Q-p:0);}}
std::vector<Pattern> patterns(int h,bool left){std::vector<Pattern> p;for(int x=0;x<Q;x++){int t=left?pairtype(pos[(x+h+42)%Q],neg[x]):pairtype(pos[x],neg[(x+h)%Q]);if(t>=0)p.push_back({x,t});}return p;}
int first_positive(int r){return r==0?Q:r;}
void selftest(){labels();for(int h=1;h<=2000;h++){auto l=patterns(h,true),r=patterns(h,false);std::vector<int> got(10001,-1),want(10001,-1);for(bool left:{false,true}){std::fill(got.begin(),got.end(),-1);for(auto p:(left?l:r))for(int x=first_positive(p.residue);x<=10000;x+=Q)got[x]=p.type;for(int x=1;x<=10000;x++)want[x]=left?pairtype(pos[(x+h+42)%Q],neg[x%Q]):pairtype(pos[x%Q],neg[(x+h)%Q]);if(got!=want)throw std::runtime_error("pattern mismatch");}}
for(int a=0;a<300;a++)for(int b=0;b<300;b++){u64 x=power(a,E,M),y=power(b,E,M);if(sub(x,y)!=(u128(x)+M-y)%M||add42(x)!=(u128(x)+42)%M)throw std::runtime_error("arithmetic mismatch");}
std::cout<<"SELFTEST PASS: residue-stride generation versus direct loops for 2,000 gap values; modular subtraction and complement\n";}
int main(int argc,char**argv){if(argc==2&&std::string(argv[1])=="--self-test"){selftest();return 0;}if(argc<2){std::cerr<<"Usage: search bound [start_h=1] [end_h=complete]\n";return 2;}int B=std::atoi(argv[1]);if(B<44||B>2103443){std::cerr<<"This exact-S42 proof only permits 44 <= B <= 2103443\n";return 2;}int H=0;while(66LL*(H+1)*(H+1)<42LL*B)H++;int start=argc>2?std::atoi(argv[2]):1,end=argc>3?std::atoi(argv[3]):H;if(start<1||end>H||start>end)return 2;
rlimit lim{1024ULL*1024*1024,1024ULL*1024*1024};setrlimit(RLIMIT_AS,&lim);
auto begin=std::chrono::steady_clock::now();labels();std::vector<u64> p(B+1);for(int x=1;x<=B;x++)p[x]=power(x,E,M);
std::cout<<"START bound="<<B<<" modulus="<<M<<" exponent="<<E<<" base_sum=42 max_gap="<<H<<" start="<<start<<" end="<<end<<"\n";
u64 totalL=0,totalR=0,hits=0,ordered=0;
for(int h=start;h<=end;h++){
 std::array<std::vector<Entry>,4> L,R;u64 countL=0,countR=0;
 for(auto pat:patterns(h,true))for(int c=first_positive(pat.residue);c+h+42<=B;c+=Q){int a=c+h+42;L[pat.type].push_back({sub(p[a],p[c]),c});countL++;}
 for(auto pat:patterns(h,false))for(int b=first_positive(pat.residue);b+h<=B;b+=Q){int d=b+h;R[3-pat.type].push_back({add42(sub(p[d],p[b])),b});countR++;}
 u64 localhits=0,localordered=0;
 for(int t=0;t<4;t++){
  auto &l=L[t],&r=R[t];std::sort(l.begin(),l.end());std::sort(r.begin(),r.end());size_t i=0,j=0;
  while(i<l.size()&&j<r.size()){
   if(l[i].value<r[j].value){i++;continue;}if(l[i].value>r[j].value){j++;continue;}
   size_t i2=i+1,j2=j+1;while(i2<l.size()&&l[i2].value==l[i].value)i2++;while(j2<r.size()&&r[j2].value==r[j].value)j2++;
   for(size_t x=i;x<i2;x++)for(size_t y=j;y<j2;y++){
    int c=l[x].base,a=c+h+42,b=r[y].base,d=b+h;localhits++;
    if(a<b){localordered++;std::cout<<"CANDIDATE h="<<h<<" a="<<a<<" b="<<b<<" c="<<-c<<" d="<<-d<<" residue="<<l[x].value<<"\n";}
   }i=i2;j=j2;
  }
 }
 totalL+=countL;totalR+=countR;hits+=localhits;ordered+=localordered;rusage usage{};getrusage(RUSAGE_SELF,&usage);
 std::cout<<"CHECKPOINT bound="<<B<<" h="<<h<<" left="<<countL<<" right="<<countR<<" matches="<<localhits<<" ordered="<<localordered<<" wall="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()<<" rss_kib="<<usage.ru_maxrss<<std::endl;
}
std::cout<<(start==1&&end==H?"DONE":"PARTIAL_DONE")<<" bound="<<B<<" max_gap="<<H<<" start="<<start<<" end="<<end<<" left="<<totalL<<" right="<<totalR<<" matches="<<hits<<" ordered="<<ordered<<std::endl;
}
