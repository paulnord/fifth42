#define main experiment_main
#include "../fifth42-other-sieves-20261106/bench.cpp"
#undef main
#include <cassert>
int main(){
 U64 checks=0,triples=0,aliases=0; interval=true;
 for(U64 C:{U64(0),U64(1),U64(42),U64(2951)}){
  cap=C;
  for(int bits:{16,32,64}){
   U64 M=bits==64?~U64(0):(U64(1)<<bits)-1;
   for(S64 r=-static_cast<S64>(C);r<=static_cast<S64>(C);++r){assert(lowok(static_cast<U64>(r),bits));++checks;}
   for(U64 u:{U64(0),C,C+1,M-C-1,M-C,M}){
    u&=M;bool want=(u<=C||u>=((U64(0)-C)&M));assert(lowok(u,bits)==want);++checks;
   }
  }
 }
 cap=42;
 for(S64 t=-44;t<=44;++t){bool want=t>=-42&&t<=42;assert(lowok(static_cast<U64>(t),64)==want);++checks;}
 U64 a,b,c,lo,mid,hi;int exact;
 while(std::cin>>a>>b>>c>>lo>>mid>>hi>>exact){
  auto got=fifth64(a)+fifth64(b)+(-fifth64(c));assert(got.lo==lo&&got.hi.lo==mid&&got.hi.hi==hi);
  U64 l=fifthlow(a)+fifthlow(b)-fifthlow(c);assert(l==lo);
  if(exact)assert(lowok(l,64));else if(lowok(l,64))++aliases;
  Task t{};t.cmin=1;t.cmax=200000000000LL;t.J[0]=1;t.points=3;t.U[0]=c;t.U[1]=a;t.U[2]=b;Candidate h0{},h1{};
  assert(test<0>(t,0,2,h0)==bool(exact));assert(test<1>(t,0,2,h1)==bool(exact));++triples;
 }
 interval=false;targets={-42,42};for(S64 t=-43;t<=43;++t){assert(lowok(static_cast<U64>(t),64)==(t==-42||t==42));++checks;}
 targets={12,384,2951,-960};
 for(auto v:std::vector<std::array<S64,3>>{{13,16,17},{26,32,34},{42,71,72},{2,2,4}}){
  Task t{};t.cmin=1;t.cmax=200000000000LL;t.J[0]=1;t.points=3;t.U[0]=v[2];t.U[1]=v[0];t.U[2]=v[1];Candidate h{};
  assert(test<0>(t,0,2,h));assert(test<1>(t,0,2,h));++checks;
 }
 std::cout<<"{\"boundary_checks\":"<<checks<<",\"bigint_triples\":"<<triples<<",\"actual_aliases\":"<<aliases<<",\"all_passed\":true,\"cap_zero_preserves_but_does_not_filter\":"<<(cap=0,interval=true,lowok(123456,64)?"true":"false")<<"}\n";
}
