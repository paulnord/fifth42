"""Independent mathematical count reconciliation; does not import search/checker code."""
import hashlib,json,math,re,sys
from pathlib import Path
root=Path(__file__).parent; B=2100000; q=1597
log_path=root/(sys.argv[1] if len(sys.argv)>1 else 'run_2100000.log')
log=log_path.read_text()
start=re.search(r'^START bound=(\d+) modulus=(\d+) exponent=133 base_sum=42 max_gap=(\d+) start=1 end=(\d+)$',log,re.M)
assert start and int(start[1])==B
modulus=int(start[2])
assert modulus in [2305843009213693921,2305843009213693951]
rx=re.compile(r'^CHECKPOINT bound=(\d+) h=(\d+) left=(\d+) right=(\d+) matches=(\d+) ordered=(\d+) wall=([\d.]+) rss_kib=(\d+)$',re.M)
rows=[m.groups() for m in rx.finditer(log)]
H=math.isqrt((42*B-1)//66)
assert len(rows)==H and [int(x[1]) for x in rows]==list(range(1,H+1))
res=[pow(x,133,q) for x in range(q)]
allowed={(1,1),(1,325),(1,1312),(325,1312)}
def count(r,limit):
    # count positive integers <=limit in congruence class r mod q
    return (limit-r)//q+1-(r==0) if limit>=r else 0
Lsum=Rsum=0
for row in rows:
    b,h,nL,nR,matches,ordered=map(int,row[:6]);assert b==B and matches==ordered==0
    L=R=0
    for r in range(q):
        if tuple(sorted((res[(r+h+42)%q],res[-r%q]))) in allowed:
            L+=count(r,B-h-42)
        if tuple(sorted((res[r],res[-(r+h)%q]))) in allowed:
            R+=count(r,B-h)
    assert (L,R)==(nL,nR),(h,L,nL,R,nR)
    Lsum+=L;Rsum+=R
summary=dict(bound=B,modulus=modulus,max_gap=H,checked_checkpoints=len(rows),independent_left_count=Lsum,independent_right_count=Rsum,raw_modular_matches=sum(int(x[4])for x in rows),candidate_lines=len(re.findall(r'^CANDIDATE ',log,re.M)),source_sha256=hashlib.sha256((root/'search133_complementary.cpp').read_bytes()).hexdigest(),log_sha256=hashlib.sha256(log.encode()).hexdigest())
assert re.search(rf'^DONE bound={B} max_gap={H} start=1 end={H} left={Lsum} right={Rsum} matches=0 ordered=0$',log,re.M)
(root/('audit_independent_counts_mod2.json' if 'mod2' in log_path.name else 'audit_independent_counts.json')).write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
