"""Independent direct enumeration of collision-rich branch and shell tests."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,subprocess
root=Path(__file__).parent
source=root/'search133_incremental.cpp'; sha=hashlib.sha256(source.read_bytes()).hexdigest()
binary=root/'audit_incremental_ubsan'; M=43; Q=1597

def run(branch,B,old,S,start,end,name):
    args=[str(binary),branch,str(B),str(old),str(M),str(start),str(end),sha]
    if branch!='22':args.append(str(S))
    out=subprocess.check_output(args,text=True)
    (root/(name+'.log')).write_text(out)
    rows={int(x[1]):dict(zip(['left','right','raw','canonical','distinct'],map(int,x[2:]))) for x in re.findall(r'^CHECKPOINT branch=(\w+) h=(\d+) left=(\d+) right=(\d+) raw=(\d+) canonical=(\d+) distinct=(\d+)',out,re.M)}
    # regex tuple above has branch at0,h at1
    got=[]
    for branch0,h,a,b,c,d,distinct,residue in re.findall(r'^CANDIDATE branch=(\w+) h=(\d+) a=(-?\d+) b=(-?\d+) c=(-?\d+) d=(-?\d+) distinct=(\d+) residue=(\d+)$',out,re.M):
        vals=tuple(map(int,(a,b,c,d))); got.append((int(h),vals,int(distinct)))
        assert (sum(pow(x,133,M) for x in vals)-42)%M==0
        assert max(map(abs,vals))>old
    assert set(rows)==set(range(start,end+1))
    return rows,Counter(got)

def direct(branch,B,old,S,start,end):
    T=-42 if branch=='31neg' else 42
    target=sorted([pow(T//42,133,Q)]*2+[325*(T//42)%Q,1312*(T//42)%Q])
    targetcount=Counter(target)
    def allowed(sig):return not(Counter(sig)-targetcount)
    p=[pow(i,133,M)for i in range(B+1)]
    q=[pow(i,133,Q)for i in range(B+1)]
    result={};tuples=[]
    for h in range(start,end+1):
        low=1 if branch=='22' else (S+h+1)//2
        high=B-h-42 if branch=='22' else B-h
        L=[];R=[]
        for x in range(low,high+1):
            if branch=='22':sig=(q[x+h+42],(-q[x])%Q);key=(p[x+h+42]-p[x])%M
            else:sig=(q[S+h-x],q[x]);key=(p[S+h-x]+p[x])%M
            if allowed(sig):L.append((x,sig,key))
        for x in range(max(1 if branch=='22' else(S+h+1)//2,old-h+1),B-h+1):
            sig=(q[x],(-q[x+h])%Q);key=(p[x+h]-p[x]+T)%M
            if allowed(sig):R.append((x,sig,key))
        raw=canonical=distinct=0
        for x,ls,lk in L:
            for y,rs,rk in R:
                if sorted(ls+rs)!=target or lk!=rk:continue
                raw+=1
                if branch=='22':
                    a=x+h+42;b=y;c=x;d=y+h
                    if a>b:continue
                    vals=(a,b,-c,-d)
                else:
                    a=S+h-x;b=x;c=y;d=y+h
                    if b>c:continue
                    vals=(-a,-b,-c,d) if T<0 else(a,b,c,-d)
                canonical+=1;is_distinct=int(len(set(vals))==4);distinct+=is_distinct
                tuples.append((h,vals,is_distinct))
        result[h]=dict(left=len(L),right=len(R),raw=raw,canonical=canonical,distinct=distinct)
    return result,Counter(tuples)

reports=[]
for branch,S,H,B,old in [('22',42,15,400,280),('31pos',500,5,400,280),('31neg',500,5,400,280),('22',42,25,1000,500),('31pos',1200,14,1000,500),('31neg',1200,14,1000,500)]:
    fullrows,full=run(branch,B,0,S,1,H,'audit_'+branch+'_'+str(B)+'_full')
    shellrows,shell=run(branch,B,old,S,1,H,'audit_'+branch+'_'+str(B)+'_shell')
    expectedrows,expected=direct(branch,B,old,S,1,H)
    assert shellrows==expectedrows,(branch,'count mismatch',shellrows,expectedrows)
    assert shell==expected,(branch,'tuple mismatch',shell-expected,expected-shell)
    assert shell==Counter({k:v for k,v in full.items() if max(map(abs,k[1]))>old}),(branch,'shell omission')
    cut=H//2
    r1,t1=run(branch,B,old,S,1,cut,'audit_'+branch+'_'+str(B)+'_split1')
    r2,t2=run(branch,B,old,S,cut+1,H,'audit_'+branch+'_'+str(B)+'_split2')
    assert {**r1,**r2}==shellrows and t1+t2==shell,(branch,'split resume mismatch')
    reports.append(dict(branch=branch,bound=B,previous_bound=old,normalized_sum=S,raw_matches=sum(x['raw']for x in shellrows.values()),canonical_matches=sum(shell.values()),distinct_matches=sum(v for(k,_,d),v in shell.items()if d),gap_count=H))
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha,'source changed during tests'
report=dict(source_sha256=sha,modulus=M,checks=['direct per-gap counts','all Cartesian collision tuples','shell equals full filtered by maximum','split/resume concatenation','undefined-behavior and libstdc++ assertions'],branches=reports)
(root/'audit_incremental_small.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
