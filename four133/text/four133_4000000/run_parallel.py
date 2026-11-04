#!/usr/bin/env python3
"""Parallel resumable 3M-to-4M shell search; tests cannot claim coverage."""
import argparse, concurrent.futures, datetime, fcntl, hashlib, json, math, os, re, shutil, subprocess, time
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
    prev=ROOT.parent/'four133_3000000';audit=json.loads((prev/'audit_production_report.json').read_text());progress=json.loads((prev/'runs/progress.json').read_text())
    assert audit['complete'] and audit['bound']==3000000 and audit['previous_bound']==2100000
    assert audit['checked_chunks']==audit['expected_chunks']==180 and audit['checked_checkpoints']==audit['expected_checkpoints']==180538
    assert audit['exact_solutions']==[] and all(v==0 for v in audit['raw_matches'].values())
    assert progress['status']=='completed_awaiting_independent_audit' and not progress['test_mode'] and progress['completed_chunks']==180
    assert digest(prev/'search133_incremental.cpp')==audit['source_sha256'] and digest(prev/'run_incremental.py')==audit['driver_sha256']
    for rec in audit['chunks']:
        path=prev/'runs'/f"m{rec['modulus']}_{rec['branch']}_h{rec['start']:05d}_{rec['end']:05d}.log"
        assert digest(path)==rec['sha256']
    # The preceding stage explicitly preserves the audited <=2.1M union component.
    oldconfig=json.loads((prev/'runs/config.json').read_text());old=ROOT.parent/'four133_extension'
    for name,rec in oldconfig['previous_evidence'].items():
        assert digest(old/name)==rec['report_sha256']
        log='run_2100000_mod2.log' if 'mod2' in name else 'run_2100000.log'
        assert digest(old/log)==rec['log_sha256'] and digest(old/'search133_complementary.cpp')==rec['source_sha256']
    return dict(bound=3000000,prior_audit_sha256=digest(prev/'audit_production_report.json'),prior_progress_sha256=digest(prev/'runs/progress.json'),prior_source_sha256=audit['source_sha256'],prior_driver_sha256=audit['driver_sha256'],prior_chunks_verified=len(audit['chunks']),earlier_2100000_evidence=oldconfig['previous_evidence'])
def build(inherited_fds=()):
    src=ROOT/'search133_incremental.cpp';exe=ROOT/'search133_incremental';meta=ROOT/'build.json';sha=digest(src)
    prior=json.loads(meta.read_text()) if meta.exists() else {}
    if prior.get('source_sha')!=sha or not exe.exists() or prior.get('binary_sha')!=digest(exe):
        tmp=exe.with_name(exe.name+f'.building.{time.time_ns()}.{os.getpid()}');cmd=['g++','-O3','-std=c++17','-Wall','-Wextra','-Wconversion',str(src),'-o',str(tmp)]
        subprocess.run(cmd,check=True,pass_fds=inherited_fds);os.replace(tmp,exe)
        prior=dict(source_sha=sha,binary_sha=digest(exe),compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],command=cmd)
        atomic_json(meta,prior)
    return sha,prior['binary_sha']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-dir',type=Path,default=ROOT/'runs');ap.add_argument('--chunk-size',type=int,default=1024);ap.add_argument('--workers',type=int,default=1);ap.add_argument('--max-new-chunks',type=int);ap.add_argument('--test',action='store_true');args=ap.parse_args()
    assert 1<=args.chunk_size<=4096 and 1<=args.workers<=9
    if args.max_new_chunks is not None:assert args.max_new_chunks>=0
    rundir=args.run_dir.resolve();rundir.mkdir(parents=True,exist_ok=True)
    lock=(rundir/'run.lock').open('a+')
    try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise RuntimeError('Another coordinator owns this run directory.')
    lock.seek(0);lock.truncate();lock.write(f'pid={os.getpid()} started={datetime.datetime.now(datetime.timezone.utc).isoformat()}\n');lock.flush()
    sha,binary_sha=build((lock.fileno(),))
    config=dict(version=2,bound=1000 if args.test else 4000000,previous_bound=500 if args.test else 3000000,moduli=[97] if args.test else MODULI,chunk_size=args.chunk_size,test_mode=args.test,test_sum=1200 if args.test else None,source_sha=sha,binary_sha=binary_sha,driver_sha=digest(__file__),previous_evidence=None if args.test else previous_evidence())
    cp=rundir/'config.json'
    if cp.exists():assert json.loads(cp.read_text())==config,'Existing run configuration differs; refusing to mix coverage.'
    else:atomic_json(cp,config)
    engine=rundir/f'engine_{binary_sha}'
    if not engine.exists():
        tmp=engine.with_suffix('.tmp');shutil.copy2(ROOT/'search133_incremental',tmp);assert digest(tmp)==binary_sha;os.replace(tmp,engine)
    assert digest(engine)==binary_sha
    allspecs=list(specs(config));done=[];started=time.time();new=0;max_active=0;errors=[];stop_reason=None
    def key(spec):return (spec['modulus'],spec['branch'],spec['start'],spec['end'])
    def path_for(spec):return rundir/f"m{spec['modulus']}_{spec['branch']}_h{spec['start']:05d}_{spec['end']:05d}.log"
    order={key(x):i for i,x in enumerate(allspecs)}
    def save(status):
        done.sort(key=lambda x:order[key(x)])
        by_modulus={}
        for m in config['moduli']:
            selected=[x for x in done if x['modulus']==m]
            by_modulus[str(m)]={k:sum(x[k] for x in selected) for k in KEYS}
            by_modulus[str(m)].update(chunks=len(selected),checkpoints=sum(x['checkpoints'] for x in selected),compute_seconds=sum(x['wall_seconds'] for x in selected))
        obj=dict(status=status,test_mode=config['test_mode'],coverage_claim=False,bound=config['bound'],previous_bound=config['previous_bound'],completed_chunks=len(done),expected_chunks=len(allspecs),completed_checkpoints=sum(x['checkpoints'] for x in done),summed_chunk_wall_seconds=sum(x['wall_seconds'] for x in done),peak_search_process_rss_kib=max([x['rss_kib'] for x in done] or [0]),log_bytes=sum(x['bytes'] for x in done),by_modulus=by_modulus,source_sha=sha,binary_sha=binary_sha,driver_sha=config['driver_sha'],workers_requested=args.workers,maximum_active_chunks=max_active,session_elapsed_seconds=time.time()-started,errors=errors,chunks=done)
        atomic_json(rundir/'progress.json',obj);return obj
    oldprogress=json.loads((rundir/'progress.json').read_text()) if (rundir/'progress.json').exists() else {}
    prior_hashes={key(x):x['sha256'] for x in oldprogress.get('chunks',[])}
    assert set(prior_hashes)<=set(order),'Recorded chunk outside configured search.'
    existing={}
    for spec in allspecs:
        k=key(spec);p=path_for(spec)
        if p.exists():
            r=validate_chunk(p,spec,config)
            if k in prior_hashes:assert r['sha256']==prior_hashes[k],'Completed chunk changed.'
            existing[k]=r;done.append(r)
        else:assert k not in prior_hashes,'A recorded completed chunk is missing.'
    old_solutions=[hit for r in done for hit in r['exact_solutions']]
    if old_solutions:save('exact_solution_found');print('EXACT_SOLUTION_FOUND',json.dumps(old_solutions),flush=True);return
    todo=[s for s in allspecs if key(s) not in existing];limit=len(todo) if args.max_new_chunks is None else min(len(todo),args.max_new_chunks)
    def work(spec):
        p=path_for(spec);partial=p.with_suffix('.partial');cmd=[str(engine),spec['branch'],str(config['bound']),str(config['previous_bound']),str(spec['modulus']),str(spec['start']),str(spec['end']),sha]
        if config['test_mode']:cmd.append(str(42 if spec['branch']=='22' else config['test_sum']))
        with partial.open('w') as out:subprocess.run(cmd,stdout=out,check=True,pass_fds=(lock.fileno(),))
        r=validate_chunk(partial,spec,config);os.replace(partial,p);return r
    submitted=0;active={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        while active or (submitted<limit and stop_reason is None):
            if (rundir/'STOP').exists() and stop_reason is None:stop_reason='pause_requested'
            while stop_reason is None and submitted<limit and len(active)<args.workers:
                spec=todo[submitted];submitted+=1;future=pool.submit(work,spec);active[future]=spec;max_active=max(max_active,len(active));print('RUNNING',path_for(spec).name,'active',len(active),flush=True)
            if not active:break
            ready,_=concurrent.futures.wait(active,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in ready:
                spec=active.pop(future)
                try:
                    r=future.result();done.append(r);new+=1
                    print('CHUNK_OK',len(done),'of',len(allspecs),path_for(spec).name,'raw',r['raw'],'wall',r['wall_seconds'],flush=True)
                    if r['exact_solutions']:stop_reason='exact_solution_found';print('EXACT_SOLUTION_FOUND',json.dumps(r['exact_solutions']),flush=True)
                except Exception as exc:
                    errors.append(dict(spec,error=f'{type(exc).__name__}: {exc}'));stop_reason='failed';print('CHUNK_FAILED',path_for(spec).name,str(exc),flush=True)
            if ready:save(stop_reason or 'active')
    status='failed' if errors else 'exact_solution_found' if any(r['exact_solutions'] for r in done) else 'completed_awaiting_independent_audit' if len(done)==len(allspecs) else 'paused'
    result=save(status)
    with (rundir/'executions.jsonl').open('a') as f:f.write(json.dumps(dict(ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),workers=args.workers,max_active=max_active,elapsed_seconds=time.time()-started,new_completed=new,status=status))+'\n')
    print('SESSION_DONE',json.dumps({k:v for k,v in result.items() if k!='chunks'}),flush=True)
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
