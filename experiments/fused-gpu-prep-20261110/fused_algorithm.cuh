#pragma once
// All operations exact unsigned integers. Host proves intermediate bounds.
template<class O> __device__ void power(O&o,typename O::Num&r,const typename O::Num&a,unsigned k) {
  typename O::Num x,x2,x4,x8; o.copy(x,a);
  o.mul(x2,x,x);
  if(k==2){o.copy(r,x2);return;}
  if(k==3){o.mul(r,x2,x);return;}
  o.mul(x4,x2,x2);
  if(k==4){o.copy(r,x4);return;}
  if(k==5){o.mul(r,x4,x);return;}
  o.mul(x8,x4,x4);o.mul(r,x8,x); // all remaining call sites use k=9

}
template<class O> __device__ void fifth_root(O&o,typename O::Num&r,const typename O::Num&N,const typename O::Num&D,unsigned bits){
  typename O::Num target,one,bit,candidate,p,product;
  o.shl(target,N,5*bits);o.set(r,0);o.set(one,1);
  for(int b=bits;b>=0;--b){o.shl(bit,one,b);o.add(candidate,r,bit);power(o,p,candidate,5);o.mul(product,p,D);if(o.cmp(product,target)<=0)o.copy(r,candidate);}
}
template<class O> __device__ void run_patch(O&o,const Input&a,Output&out){
  using N=typename O::Num;
  N P,H,R,S,C,cap,T,s5,r5,p5,c5,qn,vn,an,ad,nq,nqh,nv,na,tmp,tmp2,target,x,y;
  o.set(P,a.left+a.right);o.set(H,a.right-a.left);o.set(R,2*a.right);o.set(S,2*a.den);
  o.set(C,a.lo);o.set(cap,a.cap);o.set(T,1);o.shl(tmp,T,a.bits);o.copy(T,tmp);
  power(o,s5,S,5);power(o,p5,P,5);power(o,r5,R,5);power(o,c5,C,5);
  o.sub(qn,s5,p5);o.sub(vn,s5,r5);
  o.mul(tmp,vn,c5);o.mul(tmp2,cap,s5);o.sub(an,tmp,tmp2);o.mul(ad,s5,c5);
  fifth_root(o,nq,qn,s5,a.bits);o.copy(nqh,nq);power(o,tmp,nq,5);o.mul(tmp2,tmp,s5);o.shl(target,qn,5*a.bits);
  if(o.cmp(tmp2,target)!=0){o.set(tmp,1);o.add(tmp2,nq,tmp);o.copy(nqh,tmp2);}
  fifth_root(o,nv,vn,s5,a.bits);power(o,tmp,nv,5);o.mul(tmp2,tmp,ad);o.shl(target,an,5*a.bits);
  if(o.cmp(tmp2,target)<=0)o.copy(na,nv);else fifth_root(o,na,an,ad,a.bits);
  o.store(&out.value[0],nq);o.store(&out.value[1],nqh);o.store(&out.value[2],nv);o.store(&out.value[3],na);
  N numerator,denominator,t4,P4,s4,xy;
  power(o,x,nq,4);power(o,y,nqh,4);power(o,t4,T,4);power(o,P4,P,4);power(o,s4,S,4);o.mul(xy,x,y);
  // q=(nq+nqh)/(2T)
  o.add(numerator,nq,nqh);o.shl(denominator,T,1);o.store(&out.value[4],numerator);o.store(&out.value[5],denominator);
  // -m=P^4 T^4 (x+y)/(2S^4xy)
  o.add(tmp,x,y);o.mul(tmp2,P4,t4);o.mul(numerator,tmp2,tmp);o.mul(tmp,s4,xy);o.shl(denominator,tmp,1);
  o.store(&out.value[6],numerator);o.store(&out.value[7],denominator);
  o.sub(numerator,nqh,nq);o.shl(denominator,T,1);o.store(&out.value[8],numerator);o.store(&out.value[9],denominator);
  // eps_slope=P^4 T^4 (y-x) H/(2S^5xy)
  o.sub(tmp,y,x);o.mul(tmp2,P4,t4);o.mul(numerator,tmp2,tmp);o.mul(tmp,numerator,H);o.copy(numerator,tmp);
  o.mul(tmp,s5,xy);o.shl(denominator,tmp,1);o.store(&out.value[10],numerator);o.store(&out.value[11],denominator);
  // eps_curve=2R^3 H^2 T^9/(S^5 nv^9)
  power(o,tmp,R,3);power(o,tmp2,H,2);o.mul(numerator,tmp,tmp2);o.shl(tmp,numerator,9*a.bits+1);o.copy(numerator,tmp);
  power(o,tmp,nv,9);o.mul(denominator,s5,tmp);o.store(&out.value[12],numerator);o.store(&out.value[13],denominator);
  // eps_residual=cap*T^4/(5*cmin^5*na^4)
  o.mul(numerator,cap,t4);power(o,tmp,na,4);o.mul(tmp2,c5,tmp);o.set(tmp,5);o.mul(denominator,tmp2,tmp);
  o.store(&out.value[14],numerator);o.store(&out.value[15],denominator);
}
