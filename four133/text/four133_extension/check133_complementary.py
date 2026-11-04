#!/usr/bin/env python3
"""Verify every emitted candidate with arbitrary-precision integers; summarize checkpoint integrity."""
import argparse, hashlib, json, re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('log',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
lines=a.log.read_text().splitlines()
def fields(s):
    return {k:v for k,v in re.findall(r'(\w+)=([^ ]+)',s)}
start=fields(next(x for x in lines if x.startswith('START ')))
checks=[fields(x) for x in lines if x.startswith('CHECKPOINT ')]
done=fields(next(x for x in lines if x.startswith('DONE ')))
B=int(start['bound']);H=int(start['max_gap'])
assert int(start['base_sum'])==42 and B<=2103443
assert [int(c['h']) for c in checks]==list(range(1,H+1))
assert 66*H*H<42*B<=66*(H+1)*(H+1)
assert all(int(c['bound'])==B for c in checks)
for k in ['left','right','matches','ordered']:
    assert sum(int(c[k]) for c in checks)==int(done[k])
candidates=[]
for line in lines:
    if not line.startswith('CANDIDATE '): continue
    f=fields(line);bases=[int(f[k]) for k in ['a','b','c','d']]
    assert len(set(bases))==4 and max(map(abs,bases))<=B and sum(bases)==42
    exact=sum(x**133 for x in bases)
    assert exact%int(start['modulus'])==42
    candidates.append({'bases':bases,'exact_match':exact==42,'residual':str(exact-42)})
assert len(candidates)==int(done['ordered'])
report={'bound':B,'exponent':133,'target':42,'distinct_bases':True,'base_sum':42,
        'max_gap':H,'checkpoints':len(checks),'left_pairs':int(done['left']),
        'right_pairs':int(done['right']),'modular_matches':int(done['matches']),
        'ordered_distinct_candidates':len(candidates),'exact_solutions':[c for c in candidates if c['exact_match']],
        'wall_seconds':float(checks[-1]['wall']),'rss_kib':max(int(c['rss_kib']) for c in checks),
        'log_sha256':hashlib.sha256(a.log.read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256(a.log.with_name('search133_complementary.cpp').read_bytes()).hexdigest(),
        'candidates':candidates}
if a.output:a.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
