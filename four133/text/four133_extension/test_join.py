#!/usr/bin/env python3
"""Independent direct candidate enumerator for forced collisions modulo 97."""
import collections, json, re, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
B=1000;E=133;Q=1597;m=97
pat=collections.Counter([1,1,325,1312]);p=[pow(x,E,m) for x in range(B+1)];q=[pow(x,E,Q) for x in range(B+1)]
subprocess.run(['g++','-O3','-std=c++17','-DSEARCH_MODULUS=97ULL',str(root/'search133_complementary.cpp'),'-o',str(root/'search133_complementary_mod97')],check=True)
log=subprocess.check_output([str(root/'search133_complementary_mod97'),str(B)],text=True)
(root/'test_1000_mod97.log').write_text(log)
expected=[];all_matches=0;H=0
while 66*(H+1)**2<42*B:H+=1
for h in range(1,H+1):
    L=[];R=[]
    for c in range(1,B-h-42+1):
        a=c+h+42;co=collections.Counter([q[a],(-q[c])%Q])
        if co<=pat:L.append((a,c,co,(p[a]-p[c])%m))
    for b in range(1,B-h+1):
        d=b+h;co=collections.Counter([q[b],(-q[d])%Q])
        if co<=pat:R.append((b,d,co,(42+p[d]-p[b])%m))
    for a,c,lc,lv in L:
        for b,d,rc,rv in R:
            if lc+rc==pat and lv==rv:
                all_matches+=1
                if a<b:expected.append((h,a,b,-c,-d,lv))
actual=[tuple(map(int,re.findall(r'=(-?\d+)',s))) for s in log.splitlines() if s.startswith('CANDIDATE ')]
assert sorted(actual)==sorted(expected)
assert int(re.search(r' matches=(\d+)',log.splitlines()[-1])[1])==all_matches
r={'bound':B,'modulus':m,'gap_checkpoints':H,'all_modular_matches':all_matches,'ordered_distinct_matches':len(actual),'full_candidate_multiset_matches_direct_python':True}
(root/'test_1000_mod97.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
