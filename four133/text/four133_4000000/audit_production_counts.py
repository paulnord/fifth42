"""Independent residue-progression counts and production-log coverage audit.
Does not import production search or its driver/checker.
"""
import argparse, collections, functools, gzip, hashlib, json, math, re, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
B=4000000; OLD=3000000; Q=1597; D=4206930
MODULI=[2305843009213693921,2305843009213693951]
SOURCE_SHA='30365331b8f9e0cde8471b843c3ca38b695417d8dfc8c4c9df25cd0fee968f24'
DRIVER_SHA='d58e092f6e0ecb599c4282f68dba02d70bdf18047033cf67b50e632537ce15ff'
S_VALUES={'22':42,'31pos':D+42,'31neg':D-42}
H_VALUES={'22':math.isqrt((42*B-1)//66),'31pos':2*B//135,'31neg':2*B//135}
P=[pow(r,133,Q) for r in range(Q)]
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fields(line):return dict(re.findall(r'(\w+)=([^ ]+)',line))

def expected_counts():
    allowed={1:{(1,1),(1,325),(1,1312),(325,1312)},-1:{(1596,1596),(1272,1596),(285,1596),(285,1272)}}
    @functools.lru_cache(None)
    def right_residues(sign,hm):
        return [r for r in range(Q) if tuple(sorted((P[r],P[(-r-hm)%Q]))) in allowed[sign]]
    @functools.lru_cache(None)
    def left_residues(branch,hm):
        S=S_VALUES[branch];sign=-1 if branch=='31neg' else 1
        if branch=='22':return [r for r in range(Q) if tuple(sorted((P[(r+hm+42)%Q],P[-r%Q]))) in allowed[sign]]
        return [r for r in range(Q) if tuple(sorted((P[(S+hm-r)%Q],P[r]))) in allowed[sign]]
    def count(low,high,residues):
        if low>high:return 0
        return sum((high-r)//Q-(low-1-r)//Q for r in residues)
    result={}
    for branch,H in H_VALUES.items():
        S=S_VALUES[branch];sign=-1 if branch=='31neg' else 1;rows=[]
        for h in range(1,H+1):
            low=1 if branch=='22' else (S+h+1)//2
            high=B-h-42 if branch=='22' else min(B-h,S+h-1)
            rlow=max(1 if branch=='22' else (S+h+1)//2,OLD-h+1)
            rows.append([count(low,high,left_residues(branch,h%Q)),count(rlow,B-h,right_residues(sign,h%Q))])
        result[branch]=rows
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-dir',type=Path,default=ROOT/'runs');parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--require-complete',action='store_true');args=parser.parse_args()
    cache=ROOT/'audit_expected_counts.json.gz';start=time.monotonic()
    if cache.exists():
        with gzip.open(cache,'rt')as f:expected=json.load(f)
    else:
        expected=expected_counts()
        with gzip.open(cache,'wt')as f:json.dump(expected,f,separators=(',',':'))
    assert {k:len(v)for k,v in expected.items()}==H_VALUES
    count_summary={b:dict(checkpoints=len(v),left=sum(x[0]for x in v),right=sum(x[1]for x in v))for b,v in expected.items()}
    if args.prepare_only:
        print(json.dumps(dict(expected=count_summary,seconds=time.monotonic()-start),indent=2));return
    run=args.run_dir;config=json.loads((run/'config.json').read_text())
    assert not config['test_mode'] and config['bound']==B and config['previous_bound']==OLD and config['moduli']==MODULI
    assert config['source_sha']==SOURCE_SHA==digest(ROOT/'search133_incremental.cpp')
    assert digest(ROOT/'run_parallel.py')==DRIVER_SHA
    assert config['driver_sha']==DRIVER_SHA
    assert config['binary_sha']==digest(ROOT/'search133_incremental')
    assert config['binary_sha']==digest(run/('engine_'+config['binary_sha']))
    previous=ROOT.parent/'four133_3000000'
    assert config['previous_evidence']['prior_audit_sha256']==digest(previous/'audit_production_report.json')
    assert config['previous_evidence']['prior_progress_sha256']==digest(previous/'runs/progress.json')
    expected_ranges=[]
    for m in MODULI:
        for branch,H in H_VALUES.items():
            for lo in range(1,H+1,config['chunk_size']):expected_ranges.append((m,branch,lo,min(H,lo+config['chunk_size']-1)))
    seen=set();completed=[];exact=[];allcandidates=[];raw_counts=collections.Counter();canonical_counts=collections.Counter();distinct_counts=collections.Counter()
    for m,branch,lo,hi in expected_ranges:
        path=run/f'm{m}_{branch}_h{lo:05d}_{hi:05d}.log'
        if not path.exists():continue
        lines=path.read_text().splitlines();assert lines[0].startswith('START ')and lines[-1].startswith('CHUNK_DONE ')
        head=fields(lines[0]);end=fields(lines[-1]);S=S_VALUES[branch];T=-42 if branch=='31neg' else 42
        required=dict(version=1,branch=branch,bound=B,previous_bound=OLD,modulus=m,normalized_sum=S,normalized_target=T,max_gap=H_VALUES[branch],start=lo,end=hi,test_mode=0,source_sha=SOURCE_SHA)
        assert all(head.get(k)==str(v)for k,v in required.items()),(path,head)
        checkpoints=[fields(line)for line in lines if line.startswith('CHECKPOINT ')]
        assert [int(x['h'])for x in checkpoints]==list(range(lo,hi+1))
        totals=collections.Counter();emitted=collections.Counter();emitted_distinct=collections.Counter()
        for line in lines[1:-1]:
            assert line.startswith(('CHECKPOINT ','CANDIDATE ')),line
            if not line.startswith('CANDIDATE '):continue
            row=fields(line);h=int(row['h']);v=tuple(int(row[k])for k in 'abcd')
            assert row['branch']==branch and lo<=h<=hi and OLD<max(map(abs,v))<=B and 0 not in v
            assert sum(v)==(-S if T<0 else S) and sum(v)%D==42
            assert sum(pow(x,133,Q)for x in v)%Q==42 and sum(pow(x,133,m)for x in v)%m==42
            distinct=len(set(v))==4;assert int(row['distinct'])==distinct
            if branch=='22':
                a,b,c,d=v;c=-c;d=-d
                assert 0<c<a<=b<d and a-c==h+42 and d-b==h
            else:
                a,b,c,d=((-v[0],-v[1],-v[2],v[3]) if T<0 else(v[0],v[1],v[2],-v[3]))
                assert 0<a<=b<=c<d and d-c==h and a+b==S+h
            residual=sum(x**133 for x in v)-42
            item=dict(branch=branch,modulus=m,h=h,bases=v,distinct=distinct,residual=str(residual));allcandidates.append(item)
            if residual==0:exact.append(item)
            emitted[h]+=1;emitted_distinct[h]+=distinct
        for row in checkpoints:
            h=int(row['h']);key=(m,branch,h);assert key not in seen;seen.add(key)
            assert row['branch']==branch
            left,right=expected[branch][h-1]
            assert [int(row['left']),int(row['right'])]==[left,right],(key,row,left,right)
            assert int(row['canonical'])==emitted[h] and int(row['distinct'])==emitted_distinct[h]
            assert 0<=int(row['distinct'])<=int(row['canonical'])<=int(row['raw'])
            for k in ['left','right','raw','canonical','distinct']:totals[k]+=int(row[k])
        assert all(end[k]==str(required[k])for k in ['branch','bound','previous_bound','modulus','start','end'])
        assert all(int(end[k])==v for k,v in totals.items())
        raw_counts[m]+=totals['raw'];canonical_counts[m]+=totals['canonical'];distinct_counts[m]+=totals['distinct']
        completed.append(dict(modulus=m,branch=branch,start=lo,end=hi,sha256=digest(path),**totals))
    complete=len(completed)==len(expected_ranges)
    if args.require_complete:assert complete,(len(completed),len(expected_ranges))
    report=dict(complete=complete,source_sha256=SOURCE_SHA,driver_sha256=DRIVER_SHA,bound=B,previous_bound=OLD,expected_chunks=len(expected_ranges),checked_chunks=len(completed),expected_checkpoints=2*sum(H_VALUES.values()),checked_checkpoints=len(seen),independent_counts_per_modulus=count_summary,raw_matches=dict(raw_counts),canonical_matches=dict(canonical_counts),distinct_matches=dict(distinct_counts),exact_solutions=exact,candidates=allcandidates,chunks=completed,seconds=time.monotonic()-start)
    (ROOT/'audit_production_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in['chunks','candidates']},indent=2))
if __name__=='__main__':main()
