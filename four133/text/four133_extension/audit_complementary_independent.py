#!/usr/bin/env python3
from itertools import combinations_with_replacement
from collections import defaultdict
from pathlib import Path
import re,json,hashlib
Q=1597; E=133; residues=[pow(x,E,Q) for x in range(Q)]
image=sorted(set(residues))
assert [v for v in combinations_with_replacement(image,4) if sum(v)%Q==42]==[(1,1,325,1312)]
required=(1,1,325,1312)
T={(1,1):0,(1,325):1,(1,1312):2,(325,1312):3}
def typ(a,b):return T.get(tuple(sorted((a,b))),-1)
for a,b,c,d in __import__('itertools').product(image,repeat=4):
 t=typ(a,b);u=typ(c,d)
 assert (t>=0 and u>=0 and t+u==3)==(tuple(sorted((a,b,c,d)))==required)
log=Path(__file__).with_name('run_2100000.log'); rows=log.read_text().splitlines()
def fields(row):return {k:v for k,v in re.findall(r'(\w+)=([^ ]+)',row)}
start=fields(rows[0]);B=int(start['bound']);H=int(start['max_gap'])
check=[fields(r) for r in rows if r.startswith('CHECKPOINT')]
assert [int(r['h']) for r in check]==list(range(1,H+1))
def count(u,period):
 cycles,rem=divmod(u,Q)
 return cycles*sum(period)+sum(period[1:rem+1])
for row in check:
 h=int(row['h'])
 lp=[typ(residues[(c+h+42)%Q],(-residues[c])%Q)>=0 for c in range(Q)]
 rp=[typ(residues[b],(-residues[(b+h)%Q])%Q)>=0 for b in range(Q)]
 assert int(row['left'])==count(B-h-42,lp)
 assert int(row['right'])==count(B-h,rp)
# A deliberately tiny secondary modulus creates many collisions, testing
# complement buckets, all multiplicities, strict ordering and signed residues.
Bsmall=400;M=43;p=[pow(x,E,M) for x in range(Bsmall+1)]
nhit=0;types=set(); expected_cpp=[];raw_cpp=0
for h in range(1,31):
 left=defaultdict(list);right=defaultdict(list)
 for c in range(1,Bsmall-h-41):
  t=typ(residues[(c+h+42)%Q],(-residues[c%Q])%Q)
  if t>=0:left[t,(p[c+h+42]-p[c])%M].append(c)
 for b in range(1,Bsmall-h+1):
  t=typ(residues[b%Q],(-residues[(b+h)%Q])%Q)
  if t>=0:right[3-t,(42+p[b+h]-p[b])%M].append(b)
 got=[]
 if h<=15:raw_cpp+=sum(len(cs)*len(right.get(key,[])) for key,cs in left.items())
 for (t,v),cs in left.items():
  for c in cs:
   for b in right.get((t,v),[]):
    if c+h+42<b:got.append((c+h+42,b,-c,-b-h));types.add(t)
 want=[]
 for c in range(1,Bsmall-h-41):
  a=c+h+42
  for b in range(a+1,Bsmall-h+1):
   d=b+h
   if (p[a]+p[b]-p[c]-p[d])%M!=42%M:continue
   if tuple(sorted((residues[a%Q],residues[b%Q],(-residues[c%Q])%Q,(-residues[d%Q])%Q)))==required:want.append((a,b,-c,-d))
 assert sorted(got)==sorted(want)
 nhit+=len(got)
 if h<=15:expected_cpp.extend(got)
assert types=={0,1,2,3},types
cpp_rows=Path(__file__).with_name('audit_search133_mod43.log').read_text().splitlines()
actual_cpp=[tuple(int(fields(r)[k]) for k in ('a','b','c','d')) for r in cpp_rows if r.startswith('CANDIDATE')]
assert sorted(actual_cpp)==sorted(expected_cpp)
assert int(fields(cpp_rows[-1])['matches'])==raw_cpp
result={'residue_multiset':'unique and confirmed','all_four_pair_types':True,'synthetic_modulus':M,'synthetic_candidates_verified':nhit,'cpp_candidates_verified':len(actual_cpp),'cpp_raw_matches_verified':raw_cpp,'independent_checkpoint_counts':len(check),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
