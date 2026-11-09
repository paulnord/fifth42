#pragma once
#include "source/lattice_gpu/src/kernel.hpp"

HD inline U64 power5_low(U64 x) { const auto y=x*x;return y*y*x; }
HD inline bool near_low(U64 residual,U64 cap) {return residual+cap<=2*cap;}
HD inline bool canonical(const Task&t,S64 c,S64 a,S64 b) {
    return c>=t.cmin&&c<=t.cmax&&a>=1&&a<=b&&b<c;
}
HD inline bool full_hit(const Task&t,unsigned task,U64 index,S64 c,S64 a,S64 b,int mode,U64 cap,Candidate&out) {
    if(!canonical(t,c,a,b))return false;
    const auto r=fifth64(a)+fifth64(b)+(-fifth64(c));
    const auto limit=mode?five_square(c):I192::from_i64(static_cast<S64>(cap));
    if(r<(-limit)||limit<r)return false;
    out={task,index,a,b,c};return true;
}
HD inline bool low_hit(const Task&t,unsigned task,U64 index,S64 c,S64 a,S64 b,int mode,U64 cap,Candidate&out) {
    if(!canonical(t,c,a,b))return false;
    if(!mode&&!near_low(power5_low(static_cast<U64>(a))+power5_low(static_cast<U64>(b))-power5_low(static_cast<U64>(c)),cap))return false;
    return full_hit(t,task,index,c,a,b,mode,cap,out);
}
struct Differences {
    U64 d[6];
    HD void initialize(S64 c,S64 a,S64 b,S64 uc,S64 ua,S64 ub,U64 stride) {
        U64 v[6];
        for(unsigned i=0;i<6;++i) {
            const U64 k=static_cast<U64>(i)*stride;
            v[i]=power5_low(static_cast<U64>(a)+k*static_cast<U64>(ua))
                +power5_low(static_cast<U64>(b)+k*static_cast<U64>(ub))
                -power5_low(static_cast<U64>(c)+k*static_cast<U64>(uc));
        }
        for(unsigned order=0;order<6;++order) {
            d[order]=v[0];for(unsigned j=0;j<5-order;++j)v[j]=v[j+1]-v[j];
        }
    }
    HD void advance() {for(unsigned i=0;i<5;++i)d[i]+=d[i+1];}
};
HD inline int residue(S64 x) {const int r=static_cast<int>(x%251);return r<0?r+251:r;}
HD inline int pow_mod(int x) {const int y=x*x%251;return y*y%251*x%251;}
HD inline bool modular_near(S64 c,S64 a,S64 b,U64 cap) {
    if(cap>=125)return true;
    int r=(pow_mod(residue(a))+pow_mod(residue(b))-pow_mod(residue(c)))%251;
    if(r<0)r+=251;
    return static_cast<U64>(r)<=cap||static_cast<U64>(251-r)<=cap;
}

HD inline S64 coordinate(const Task&t,const S64 base[3],unsigned axis,S64 n,unsigned col) {
    // The unchanged packet guard bounds the sum of absolute terms by INT64_MAX.
    return base[col]+n*t.U[3*axis+col];
}
HD inline bool constraint(const Task&t,const S64 base[3],unsigned axis,S64 n,unsigned which) {
    const auto c=coordinate(t,base,axis,n,0),a=coordinate(t,base,axis,n,1),b=coordinate(t,base,axis,n,2);
    switch(which){case 0:return c>=t.cmin;case 1:return c<=t.cmax;case 2:return a>=1;case 3:return a<=b;default:return b<c;}
}
HD inline bool clip(const Task&t,const S64 base[3],unsigned axis,S64&lo,S64&hi) {
    for(unsigned which=0;which<5;++which) {
        const bool l=constraint(t,base,axis,lo,which),h=constraint(t,base,axis,hi,which);
        if(l&&h)continue;
        if(!l&&!h)return false;
        S64 left=lo,right=hi;
        while(left<right) {
            const S64 mid=left+(right-left)/2;
            if(constraint(t,base,axis,mid,which)==l)left=mid+1;else right=mid;
        }
        if(l)hi=left-1;else lo=left;
    }
    return lo<=hi;
}
