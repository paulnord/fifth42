#!/usr/bin/env python3
"""Resumable 2.1M-to-3M shell search. Test mode cannot claim production coverage."""
import argparse, hashlib, json, math, os, re, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODULI=[2305843009213693921,2305843009213693951]
D=4206930
KEYS=['left','right','raw','canonical','distinct']
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic_json(p,obj):
    p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,p)
def fields(line):return {k:v for k,v in re.findall(r'(\w+)=([^ ]+)',line)}
def max_gap(branch,B,S):
    if branch=='22':return math.isqrt((42*B-1)//66)
    return min(2*B//135,(2*B-S)//3)
def specs(config):
    for m in config['moduli']:
        for branch in ['22','31pos','31neg']:
            S=42 if branch=='22' else config['test_sum'] if config['test_mode'] else D-42 if branch=='31neg' else D+42
            H=max_gap(branch,config['bound'],S)
            for lo in range(1,H+1,config['chunk_size']):
                yield dict(branch=branch,modulus=m,normalized_sum=S,max_gap=H,start=lo,end=min(H,lo+config['chunk_size']-1))
def validate_chunk(path,spec,config):
    lines=Path(path).read_text().splitlines();assert lines and lines[0].startswith('START ') and lines[-1].startswith('CHUNK_DONE ')
    head=fields(lines[0]);done=fields(lines[-1]);B=config['bound'];old=config['previous_bound'];m=spec['modulus'];branch=spec['branch']
    expected=dict(spec,bound=B,previous_bound=old,normalized_target=-42 if branch=='31neg' else 42,test_mode=int(config['test_mode']),source_sha=config['source_sha'],version=1)
    for k,v in expected.items():assert head.get(k)==str(v),(k,head.get(k),v)
    for k in ['branch','bound','previous_bound','modulus','start','end']:assert done[k]==str(expected[k])
    checks=[fields(x) for x in lines if x.startswith('CHECKPOINT ')];assert [int(x['h']) for x in checks]==list(range(spec['start'],spec['end']+1))
    assert all(c['branch']==branch for c in checks)
    assert all(0<=int(c['distinct'])<=int(c['canonical'])<=int(c['raw']) for c in checks)
    totals={k:sum(int(c[k]) for c in checks) for k in KEYS}
    assert all(int(done[k])==totals[k] for k in KEYS)
    candidates=[];counts={h:[0,0] for h in range(spec['start'],spec['end']+1)}
    for line in lines:
        if not line.startswith('CANDIDATE '):continue
        f=fields(line);h=int(f['h']);assert f['branch']==branch and h in counts
        bases=[int(f[k]) for k in ['a','b','c','d']]
        assert old<max(map(abs,bases))<=B and 0 not in bases
        is_distinct=len(set(bases))==4;assert int(f['distinct'])==is_distinct
        expected_sum=42 if branch=='22' else -spec['normalized_sum'] if branch=='31neg' else spec['normalized_sum']
        assert sum(bases)==expected_sum
        if not config['test_mode']:assert sum(bases)%D==42
        if branch=='22':
            a,b,c,d=bases;c=-c;d=-d;assert 0<c<a<=b<d and d-b==h and a-c==h+42
        else:
            if branch=='31neg':a,b,c,d=[-bases[0],-bases[1],-bases[2],bases[3]]
            else:a,b,c,d=[bases[0],bases[1],bases[2],-bases[3]]
            assert 0<a<=b<=c<d and d-c==h and a+b==spec['normalized_sum']+h
        assert sum(pow(x,133,m) for x in bases)%m==42%m
        residual=sum(x**133 for x in bases)-42
        counts[h][0]+=1;counts[h][1]+=is_distinct
        candidates.append(dict(bases=bases,distinct=is_distinct,exact=residual==0,residual=str(residual),h=h))
    assert len(candidates)==totals['canonical']
    for c in checks:assert counts[int(c['h'])]==[int(c['canonical']),int(c['distinct'])]
    return dict(spec,**totals,checkpoints=len(checks),wall_seconds=float(checks[-1]['wall']),rss_kib=max(int(x['rss_kib']) for x in checks),bytes=Path(path).stat().st_size,sha256=digest(path),exact_solutions=[c for c in candidates if c['exact']],candidates=candidates)
def previous_evidence():
    prev=ROOT.parent/'four133_extension';out={}
    for name in ['report_2100000.json','report_2100000_mod2.json']:
        r=json.loads((prev/name).read_text());log='run_2100000_mod2.log' if 'mod2' in name else 'run_2100000.log'
        assert r['bound']==2100000 and r['modular_matches']==0 and r['exact_solutions']==[]
        assert digest(prev/log)==r['log_sha256'] and digest(prev/'search133_complementary.cpp')==r['source_sha256']
        out[name]=dict(report_sha256=digest(prev/name),log_sha256=r['log_sha256'],source_sha256=r['source_sha256'])
    return out
def build():
    src=ROOT/'search133_incremental.cpp';exe=ROOT/'search133_incremental';meta=ROOT/'build.json';sha=digest(src)
    prior=json.loads(meta.read_text()) if meta.exists() else {}
    if prior.get('source_sha')!=sha or not exe.exists() or prior.get('binary_sha')!=digest(exe):
        tmp=exe.with_suffix('.building');cmd=['g++','-O3','-std=c++17','-Wall','-Wextra','-Wconversion',str(src),'-o',str(tmp)]
        subprocess.run(cmd,check=True);os.replace(tmp,exe)
        prior=dict(source_sha=sha,binary_sha=digest(exe),compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],command=cmd)
        atomic_json(meta,prior)
    return sha,prior['binary_sha']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-dir',type=Path,default=ROOT/'runs');ap.add_argument('--chunk-size',type=int,default=1024);ap.add_argument('--max-new-chunks',type=int);ap.add_argument('--test',action='store_true');args=ap.parse_args()
    assert 1<=args.chunk_size<=4096
    sha,binary_sha=build();rundir=args.run_dir.resolve();rundir.mkdir(parents=True,exist_ok=True)
    config=dict(version=1,bound=1000 if args.test else 3000000,previous_bound=500 if args.test else 2100000,moduli=[97] if args.test else MODULI,chunk_size=args.chunk_size,test_mode=args.test,test_sum=1200 if args.test else None,source_sha=sha,binary_sha=binary_sha,previous_evidence=None if args.test else previous_evidence())
    cp=rundir/'config.json'
    if cp.exists():assert json.loads(cp.read_text())==config,'Existing run configuration differs; refusing to mix coverage.'
    else:atomic_json(cp,config)
    allspecs=list(specs(config));done=[];started=time.time();new=0
    def save(status):
        by_modulus={}
        for m in config['moduli']:
            selected=[x for x in done if x['modulus']==m]
            by_modulus[str(m)]={k:sum(x[k] for x in selected) for k in KEYS}
            by_modulus[str(m)].update(chunks=len(selected),checkpoints=sum(x['checkpoints'] for x in selected),compute_seconds=sum(x['wall_seconds'] for x in selected))
        obj=dict(status=status,test_mode=config['test_mode'],coverage_claim=False,bound=config['bound'],previous_bound=config['previous_bound'],completed_chunks=len(done),expected_chunks=len(allspecs),completed_checkpoints=sum(x['checkpoints'] for x in done),compute_seconds=sum(x['wall_seconds'] for x in done),peak_rss_kib=max([x['rss_kib'] for x in done] or [0]),log_bytes=sum(x['bytes'] for x in done),by_modulus=by_modulus,source_sha=sha,binary_sha=binary_sha,chunks=done)
        atomic_json(rundir/'progress.json',obj)
        return obj
    previous_progress=json.loads((rundir/'progress.json').read_text()) if (rundir/'progress.json').exists() else {}
    prior_hashes={(x['modulus'],x['branch'],x['start'],x['end']):x['sha256'] for x in previous_progress.get('chunks',[])}
    def spec_key(spec):return (spec['modulus'],spec['branch'],spec['start'],spec['end'])
    def chunk_path(spec):return rundir/f"m{spec['modulus']}_{spec['branch']}_h{spec['start']:05d}_{spec['end']:05d}.log"
    expected_keys={spec_key(x) for x in allspecs}
    assert set(prior_hashes)<=expected_keys,'Recorded chunk lies outside the configured search.'
    existing={}
    # Validate ALL completed work before scheduling or writing a progress snapshot.
    # This preserves noncontiguous completed chunks and their hashes across pauses.
    for spec in allspecs:
        key=spec_key(spec);path=chunk_path(spec)
        if path.exists():
            record=validate_chunk(path,spec,config)
            if key in prior_hashes:assert record['sha256']==prior_hashes[key],'Completed chunk changed.'
            existing[key]=record;done.append(record)
        else:assert key not in prior_hashes,'A recorded completed chunk is missing.'
    old_solutions=[hit for record in done for hit in record['exact_solutions']]
    if old_solutions:
        save('exact_solution_found');print('EXACT_SOLUTION_FOUND',json.dumps(old_solutions),flush=True);return
    for spec in allspecs:
        key=spec_key(spec);path=chunk_path(spec);name=path.name
        if key in existing:continue
        if args.max_new_chunks is not None and new>=args.max_new_chunks:save('paused');print('PAUSED',len(done),'of',len(allspecs),flush=True);return
        partial=path.with_suffix('.partial');cmd=[str(ROOT/'search133_incremental'),spec['branch'],str(config['bound']),str(config['previous_bound']),str(spec['modulus']),str(spec['start']),str(spec['end']),sha]
        if config['test_mode']:cmd.append(str(42 if spec['branch']=='22' else config['test_sum']))
        print('RUNNING',name,flush=True)
        try:
            with partial.open('w') as f:subprocess.run(cmd,stdout=f,check=True)
            record=validate_chunk(partial,spec,config);os.replace(partial,path)
        except Exception:
            save('failed');raise
        done.append(record);done.sort(key=lambda x:(config['moduli'].index(x['modulus']),['22','31pos','31neg'].index(x['branch']),x['start']));new+=1;save('active')
        print('CHUNK_OK',len(done),'of',len(allspecs),'raw',record['raw'],'canonical',record['canonical'],'wall',record['wall_seconds'],flush=True)
        if record['exact_solutions']:
            save('exact_solution_found');print('EXACT_SOLUTION_FOUND',json.dumps(record['exact_solutions']),flush=True);return
    result=save('completed_awaiting_independent_audit');print('ALL_CHUNKS_COMPLETE',json.dumps({k:v for k,v in result.items() if k!='chunks'}),flush=True)
if __name__=='__main__':main()
