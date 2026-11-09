#!/usr/bin/env python3
"""Checkpointed, streaming certified search with an absolute morning deadline."""
import argparse
from dataclasses import asdict
from datetime import datetime,timezone
import hashlib
import json
from math import gcd
import multiprocessing
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback

ROOT=Path(__file__).resolve().parent
MAX_BASE=200_000_000_000
CHUNK_TASKS=256
WORKERS=16

class RequestedStop(Exception):pass

def atomic_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('w') as stream:
        json.dump(data,stream,sort_keys=True,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    temporary.replace(path)
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def grid_count(lo,width):
    if type(lo)!=int or lo<1 or type(width)!=int or width<1:raise ValueError('Invalid shell grid')
    return (9*lo+10*width-1)//(10*width)

def shell_specs(lo,hi,width,bits,first,last,cap=42):
    count=grid_count(lo,width)
    if not (1<=lo<=hi<=min(2*lo-1,MAX_BASE) and 0<=first<=last<=count):raise ValueError('Invalid streaming shell interval')
    def pair(n,d):
        factor=gcd(n,d);return n//factor,d//factor
    return [(i,lo,hi,pair(9*i,10*count),pair(9*(i+1),10*count),cap,bits) for i in range(first,last)]

def initialize(source,cpus=()):
    import scaling_core as core
    core.initialize(source,cpus)
    # Only this isolated streaming run extends the full-domain coordinator cap.
    # Native packets retain every original per-task, packet, transform and base guard.
    core.MAX_BOUND=MAX_BASE

def cpu_sphere(spec):
    """Exact bounded fallback for a patch that cannot fit the native box engine."""
    import scaling_core as core
    l=core.lattice();ident,lo,hi,left,right,cap,bits=spec
    patch=l.make_patch(lo,hi,l.Q(*left),l.Q(*right),cap,bits)
    stats=l.Stats();began=time.perf_counter()
    budget=l.Budget(max_nodes=10_000_000,max_patches=1,max_seconds=300,start=began)
    try:
        hits=l.patch_search(patch,lambda r,c:abs(r)<=cap,stats,budget,backend='fpylll')
        budget.check(stats)
    except l.BudgetExceeded as error:
        return dict(id=ident,hits=[],stats=asdict(stats),seconds=time.perf_counter()-began,
            complete=False,method='original-exact-sphere',spec=spec,error=str(error))
    return dict(id=ident,hits=sorted(hits),stats=asdict(stats),seconds=time.perf_counter()-began,
        complete=True,method='original-exact-sphere',spec=spec)

def native_safe(task):
    import scaling_core as core
    return (task.points<=core.MAX_PATCH_POINTS and
        all(abs(x)<=core.MAX_I64 for row in task.U for x in row) and
        all(sum(task.J[i]*abs(task.U[i][col]) for i in range(3))<=core.MAX_I64 for col in range(3)))

def encode_record(previous,record):
    payload=dict(record,previous_sha256=previous)
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    payload['sha256']=hashlib.sha256(raw).hexdigest()
    return (json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode(),payload['sha256']

def verify_journal(path,checkpoint):
    path=Path(path);previous='0'*64;sequence=0;offset=0
    if not path.exists():
        if checkpoint['journal_offset']:raise RuntimeError('Checkpoint journal is missing')
        return
    with path.open('rb') as stream:
        while offset<checkpoint['journal_offset']:
            raw=stream.readline()
            if not raw.endswith(b'\n'):raise RuntimeError('Truncated committed coverage record')
            data=json.loads(raw);digest=data.pop('sha256')
            if data['previous_sha256']!=previous or data['sequence']!=sequence+1:raise RuntimeError('Coverage chain order mismatch')
            if hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=digest:
                raise RuntimeError('Coverage chain hash mismatch')
            previous=digest;sequence+=1;offset=stream.tell()
        if offset!=checkpoint['journal_offset'] or previous!=checkpoint['journal_sha256'] or sequence!=checkpoint['chunks']:
            raise RuntimeError('Checkpoint does not identify the committed journal prefix')
    # A crash after append but before checkpoint leaves an uncommitted suffix.
    # Preserve it for inspection; replay its grid interval on resume.
    if path.stat().st_size>offset:
        with path.open('rb') as stream:
            stream.seek(offset);tail=stream.read()
        orphan=path.with_name('uncommitted-'+str(time.time_ns())+'.jsonl');orphan.write_bytes(tail)
        with path.open('r+b') as stream:stream.truncate(offset);stream.flush();os.fsync(stream.fileno())

def validate_checkpoint(state,config):
    if (state['width'],state['backend'],state['cap'],state['source_identity'])!=(config['width'],config['backend'],42,config['source_identity']):
        raise RuntimeError('Resume configuration or source identity changed')
    lo=state['shell_lo'];index=state['next_patch']
    origin=config.get('start_bound',1)
    ratio=lo//origin if type(lo)==int and lo>=origin else 0
    if not ratio or lo%origin or ratio&(ratio-1):raise RuntimeError('Checkpoint shell progression changed')
    if origin==1 and state['completed_bound']!=lo-1:raise RuntimeError('Checkpoint shell coverage is not a contiguous prefix')
    if origin!=1 and state['completed_bound'] is not None:raise RuntimeError('Selected high-range patches cannot confer full-box coverage')
    if type(index)!=int or not 0<=index<=grid_count(lo,state['width']):raise RuntimeError('Invalid checkpoint patch cursor')

def extend_arithmetic_range(run,config):
    """Change one scratch range guard, rebuild, and test 192-bit arithmetic."""
    import random
    work=run/'workspace';path=work/'src/kernel.hpp'
    text=path.read_text();old='LATTICE_MAX_BASE=100000000000ULL'
    if text.count(old)!=1:raise RuntimeError('Original native base guard changed')
    if not 3*MAX_BASE**5<2**191:raise RuntimeError('Extended signed 192-bit range proof failed')
    path.write_text(text.replace(old,f'LATTICE_MAX_BASE={MAX_BASE}ULL'))
    environment=dict(os.environ,ASAN_OPTIONS='detect_leaks=0',CUDA_VISIBLE_DEVICES='0')
    commands=[]
    for name,command in (('range-build',['make','-j1','all']),('stream-build',['make','-f','scaling.mk','-j1','scaling'])):
        with (run/(name+'.stdout.log')).open('w') as output,(run/(name+'.stderr.log')).open('w') as error:
            p=subprocess.run(command,cwd=work,env=environment,stdout=output,stderr=error,timeout=90)
        commands.append(dict(command=command,exit_code=p.returncode))
        if p.returncode:raise RuntimeError('Extended range build failed: '+name)
    values=[0,1,-1,2**32-1,2**32,2**32+1,100_000_000_000,-100_000_000_000,
        100_000_000_001,-100_000_000_001,MAX_BASE,-MAX_BASE]
    rng=random.Random(205942);pairs=[(x,y) for x in values for y in values]+[(rng.randint(-MAX_BASE,MAX_BASE),rng.randint(-MAX_BASE,MAX_BASE)) for _ in range(128)]
    packet='ARITH_V1 '+str(len(pairs))+'\n'+'\n'.join(f'{x} {y}' for x,y in pairs)+'\n'
    mask=(1<<192)-1
    for binary in ('emulated','emulated-sanitized','cuda'):
        p=subprocess.run([str(work/'bin'/binary),'--arithmetic'],input=packet,text=True,capture_output=True,timeout=30,env=environment)
        if p.returncode:raise RuntimeError('Extended arithmetic execution failed: '+binary+' '+p.stderr[:300])
        result=json.loads(p.stdout)
        if len(result['arithmetic'])!=len(pairs):raise RuntimeError('Missing extended arithmetic cases')
        for (x,y),row in zip(pairs,result['arithmetic']):
            px,py=x**5,y**5
            for key,value in (('p',px),('q',py),('sum',px+py),('negative',-px-py),('square5',5*x*x)):
                actual=sum(int(word)<<(64*i) for i,word in enumerate(row[key]))
                if actual!=(value&mask):raise RuntimeError('Extended arithmetic differs from Python integers')
            if row['lt']!=(px<py) or row['eq']!=(px==py):raise RuntimeError('Extended signed comparison failed')
    record=dict(status='passed',max_base=MAX_BASE,exact_range_proof='3*max_base^5 < 2^191',
        arithmetic_cases_per_backend=len(pairs),backends=['emulated','emulated-sanitized','cuda'],commands=commands,
        kernel_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        binary_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (work/'bin').iterdir() if p.is_file()},
        source_change='One base-range guard in an isolated scratch copy; original source preserved')
    atomic_json(run/'extended-range-validation.json',record);config['extended_range_validation']=record

def worker(config):
    import scaling_core as core
    import packing_opt
    from engine_session import EngineSession
    run=Path(config['run']);source=ROOT/'lattice_prototype';selected=config['physical_cpus'][:WORKERS]
    initialize(source);os.sched_setaffinity(0,set(selected))
    deadline=config['deadline_monotonic'];width=config['width'];backend=config['backend']
    context=multiprocessing.get_context('spawn');pool=cpu=session=None
    checkpoint=run/'checkpoint.json';journal=run/'coverage.jsonl'
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else dict(status='starting',width=width,
        backend=backend,cap=42,source_identity=config['source_identity'],shell_lo=config['start_bound'],
        next_patch=config['initial_patch'],completed_bound=0 if config['start_bound']==1 else None,
        region_start_bound=config['start_bound'],region_initial_patch=config['initial_patch'],guarded_patches=0,
        chunks=0,patches=0,native_points=0,cpu_sphere_patches=0,journal_offset=0,journal_sha256='0'*64,
        hits=[],independent_oracle_verified_through=0,started_utc=datetime.now(timezone.utc).isoformat())
    validate_checkpoint(state,config);verify_journal(journal,state)
    def save():
        state['updated_utc']=datetime.now(timezone.utc).isoformat();atomic_json(checkpoint,state)
    def remaining(cap=120):
        if (run/'STOP').exists():raise RequestedStop('STOP file requested')
        left=min(deadline-time.monotonic(),config['stop_epoch']-time.time())-15
        if left<=0:raise RequestedStop('Morning deadline reached')
        return min(cap,left)
    def execute(engine,plan):
        hits=set(plan.direct_hits);records=[]
        for batch in plan.batches:
            data,seconds=engine.run(batch.packet,timeout=remaining())
            hits|=core.decode_batch(batch,data,engine.backend)
            records.append(dict(tasks=len(batch.tasks),points=batch.points,visited=data['points_visited'],seconds=seconds,
                packet_sha256=hashlib.sha256(batch.packet.encode()).hexdigest(),
                response_sha256=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
        return hits,records
    def commit(record,next_patch,shell_complete=False):
        record.update(sequence=state['chunks']+1,shell_lo=state['shell_lo'],width=width,bits=record.get('bits',48))
        raw,digest=encode_record(state['journal_sha256'],record)
        with journal.open('ab') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno());offset=stream.tell()
        state['chunks']+=1;state['journal_offset']=offset;state['journal_sha256']=digest
        state['patches']+=record.get('patches',0);state['native_points']+=record.get('native_points',0)
        state['cpu_sphere_patches']+=len(record.get('sphere_fallback',[]))
        state['guarded_patches']+=len(record.get('guarded_patches',[]))
        state['hits']=sorted({tuple(h) for h in state['hits']}|{tuple(h) for h in record['hits']})
        state['next_patch']=next_patch
        if shell_complete:
            if config['start_bound']==1 and not state['guarded_patches']:state['completed_bound']=record['shell_hi']
            state['shell_lo']*=2;state['next_patch']=0
            print(json.dumps(dict(event='shell_complete',bound=state['completed_bound'],patches=state['patches'],
                chunks=state['chunks'],hits=len(state['hits']))),flush=True)
        save()
    try:
        remaining();pool=context.Pool(WORKERS,initializer=initialize,initargs=(source,selected))
        cpu=EngineSession([str(ROOT/'bin/scaling_cpu'),'--threads',str(WORKERS)],'emulated',deadline)
        session=cpu if backend=='cpu' else EngineSession([str(ROOT/'bin/scaling_gpu')],'gpu',deadline)
        # Fresh nonempty controls exercise this runner and its original sphere fallback.
        for bound,cap in ((34,384),(100,2951)):
            remaining();oracle=json.loads(subprocess.check_output([str(ROOT/'bin/scaling_oracle'),str(bound),str(cap)],text=True,timeout=remaining()))
            expected={tuple(h) for h in oracle['hits']}
            if not expected or oracle.get('complete') is not True:raise RuntimeError('Nonempty control oracle failed')
            specs,direct=core.specs(bound,cap,width);tasks=pool.map(core.prepare_task,specs,4);tokens=pool.map(core.certify_task,tasks,4)
            plan=packing_opt.assemble(bound,cap,specs,direct,tasks,tokens)
            for engine in {cpu,session}:
                hits,_=execute(engine,plan)
                if hits!=expected:raise RuntimeError('Overnight nonempty engine control mismatch')
            sphere=set(plan.direct_hits)
            for row in pool.map(cpu_sphere,specs,1):sphere|={tuple(h) for h in row['hits']}
            if sphere!=expected:raise RuntimeError('Overnight sphere fallback control mismatch')
        state.update(status='running',controls_passed=True);save();last_notice=0.
        while state['shell_lo']<=config['max_bound']:
            remaining();lo=state['shell_lo'];hi=min(2*lo-1,config['max_bound']);first=state['next_patch']
            if lo!=1 and first==0 and (run/'PAUSE').exists():raise RequestedStop('PAUSE requested at shell boundary')
            if shutil.disk_usage(run).free<2*1024**3 or (journal.exists() and journal.stat().st_size>4*1024**3):
                raise RequestedStop('Artifact space guard reached')
            start=time.perf_counter()
            if core.lattice().Q(42,lo**5)>core.lattice().Q(9049,50000):
                hits=core.lattice().direct_positive(lo,hi,lambda c:42,lambda r,c:abs(r)<=42)
                commit(dict(shell_hi=hi,first=0,last=0,hits=sorted(hits),method='exact-small-shell',seconds=time.perf_counter()-start),0,True)
                continue
            count=grid_count(lo,width);last=min(first+CHUNK_TASKS,count)
            bits=max(48,5*hi.bit_length()+32) if config['start_bound']>1 else max(48,2*hi.bit_length()+16)
            specs=shell_specs(lo,hi,width,bits,first,last);tasks=pool.map(core.prepare_task,specs,8)
            native=[(s,t) for s,t in zip(specs,tasks) if native_safe(t)]
            fallback=[s for s,t in zip(specs,tasks) if not native_safe(t)]
            tokens=pool.map(core.certify_task,[t for _,t in native],8) if native else []
            task_tokens={t.id:token for (_,t),token in zip(native,tokens)}
            hits=set();records=[];pending=[];points=0
            def flush():
                nonlocal pending,points
                if not pending:return
                ss=[s for s,t in pending];tt=[t for s,t in pending]
                plan=packing_opt.assemble(hi,42,ss,[],tt,[task_tokens[t.id] for t in tt])
                found,raw=execute(session,plan);hits.update(found);records.extend(raw)
                if state['chunks']%128==0 and session is not cpu:
                    check,_=execute(cpu,plan)
                    if check!=found:raise RuntimeError('Periodic CPU/CUDA exact crosscheck mismatch')
                pending=[];points=0
            for spec,task in native:
                if pending and (len(pending)==core.MAX_TASKS or points+task.points>core.MAX_POINTS):flush()
                pending.append((spec,task));points+=task.points
            flush()
            sphere=pool.map(cpu_sphere,fallback,1) if fallback else []
            gaps=[]
            for spec,data in zip(fallback,sphere):
                if data['id']!=spec[0] or tuple(data['spec'])!=spec:raise RuntimeError('Sphere fallback patch identity mismatch')
                if not data['complete']:
                    if config['start_bound']==1:raise RuntimeError('Full-prefix sphere fallback did not complete')
                    gaps.append(dict(id=spec[0],error=data['error']));continue
                for h in data['hits']:
                    a,b,c,r=h
                    if not 1<=a<=b<c or not lo<=c<=hi or a**5+b**5-c**5!=r or abs(r)>42:
                        raise RuntimeError('Sphere fallback exact hit mismatch')
                hits|={tuple(h) for h in data['hits']}
            geometry=hashlib.sha256()
            for task in tasks:geometry.update(packing_opt.task_payload(task));geometry.update(b'\n')
            record=dict(shell_hi=hi,grid_count=count,first=first,last=last,bits=bits,patches=len(specs)-len(gaps),
                geometry_sha256=geometry.hexdigest(),native_points=sum(t.points for _,t in native),native=records,
                sphere_fallback=[dict(id=row['id'],stats=row['stats'],seconds=row['seconds']) for row in sphere],
                guarded_patches=gaps,
                hits=sorted(hits),seconds=time.perf_counter()-start,method='certified-native-box-plus-original-sphere',
                cpu_cuda_audited=(session is not cpu and state['chunks']%128==0))
            if config['start_bound']==1 and last==count and hi>=32000 and state['independent_oracle_verified_through']<32000:
                expected=json.loads((run/'oracle-B32000.json').read_text())
                all_hits={tuple(h) for h in state['hits']}|hits
                if {h for h in all_hits if h[2]<=32000}!={tuple(h) for h in expected['hits']}:
                    raise RuntimeError('Streaming prefix differs from independent 32000 oracle')
                state['independent_oracle_verified_through']=32000
            commit(record,last,last==count)
            if time.monotonic()-last_notice>30:
                last_notice=time.monotonic();print(json.dumps(dict(event='checkpoint',completed_bound=state['completed_bound'],
                    shell_lo=state['shell_lo'],next_patch=state['next_patch'],grid_count=count,patches=state['patches'],
                    cpu_sphere_patches=state['cpu_sphere_patches'],hits=len(state['hits']))),flush=True)
        state.update(status='completed_limit',stop_reason='Configured maximum bound completed');save();return 0
    except RequestedStop as error:
        state.update(status='stopped',stop_reason=str(error));save();return 0
    except BaseException as error:
        state.update(status='stopped_at_guard' if type(error).__name__ in ('BudgetExceeded','TimeoutError') else 'failed',
            stop_reason=f'{type(error).__name__}: {error}',traceback=traceback.format_exc());save();traceback.print_exc();return 2
    finally:
        if session is not None and session is not cpu:session.close()
        if cpu is not None:cpu.close()
        if pool is not None:pool.terminate();pool.join()

def coordinator(args):
    import scaling
    import benchmark as helpers
    guard=helpers.resources()
    selection_path=Path(args.selection_report).resolve();report=json.loads(selection_path.read_text())
    if report['status']!='passed' or report['results']['status']!='passed':raise RuntimeError('Passing width comparison is required')
    selection=report['results']['selection'];work=selection_path.parent/'workspace'
    for name,digest in report['source_sha256'].items():
        if helpers.sha(work/name)!=digest:raise RuntimeError('Measured source identity changed: '+name)
    for name,digest in report['binary_sha256'].items():
        if helpers.sha(work/'bin'/name)!=digest:raise RuntimeError('Measured engine binary changed: '+name)
    expected=json.loads((helpers.CPU_ROOT/'published-sha256.json').read_text())
    if guard.package_hashes()!=expected:raise RuntimeError('Pinned lattice package changed')
    stop=datetime.fromisoformat(args.until)
    if stop.tzinfo is None:raise ValueError('The stop time requires an explicit UTC offset')
    stop_epoch=stop.timestamp();seconds=stop_epoch-time.time()
    if not 0<seconds<=24*3600:raise ValueError('Stop time must be within the next 24 hours')
    config=dict(width=selection['width'],backend=args.backend or selection['backend'],physical_cpus=scaling.physical_cpus(),
        stop_epoch=stop_epoch,stop_local=stop.isoformat(),max_bound=args.max_bound,
        start_bound=args.start_bound,initial_patch=grid_count(args.start_bound,selection['width'])//3 if args.start_bound>1 else 0,
        original_full_domain_cap=32000,native_max_base=MAX_BASE,chunk_tasks=CHUNK_TASKS,
        original_packet_guards_retained=True,oversized_patch_method='original-exact-sphere with 10M node and 300s guards',
        selection_report=str(selection_path),selection_report_sha256=helpers.sha(selection_path),
        source_identity=hashlib.sha256(json.dumps(dict(source=report['source_sha256'],binaries=report['binary_sha256'],
            runner=helpers.sha(Path(__file__))),sort_keys=True).encode()).hexdigest(),
        domain='1 <= a <= b < c, abs(a^5+b^5-c^5) <= 42',workers=WORKERS)
    if len(config['physical_cpus'])<WORKERS:raise RuntimeError('16 physical CPU cores are required')
    if args.check_only:print(json.dumps(dict(status='ready',**config),indent=2));return 0
    blockers=helpers.hardware_blockers() if config['backend']=='cuda' else []
    if blockers:raise RuntimeError('; '.join(blockers))
    handles,leased=helpers.acquire_leases(guard,True);process=None
    def interrupted(signum,frame):raise RequestedStop('Service stop requested')
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    try:
        if config['backend']=='cuda':helpers.idle_gpu()
        folder=ROOT/'overnight-runs';folder.mkdir(exist_ok=True)
        if args.resume:
            run=Path(args.resume).resolve();prior=json.loads((run/'config.json').read_text())
            if prior['source_identity']!=config['source_identity']:raise RuntimeError('Resume source differs from frozen run')
            if prior['max_bound']!=config['max_bound']:raise RuntimeError('Resume maximum differs from frozen run')
        else:
            run=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),dir=folder))
            shutil.copytree(work,run/'workspace');shutil.copyfile(__file__,run/'workspace/overnight_search.py')
            shutil.copyfile(selection_path.parent/'oracles/B32000-cap42.json',run/'oracle-B32000.json')
            if args.max_bound>100_000_000_000:
                extend_arithmetic_range(run,config)
        config.update(run=str(run),deadline_monotonic=time.monotonic()+max(0,stop_epoch-time.time()))
        atomic_json(run/'config.json',config);atomic_json(ROOT/'overnight-current.json',dict(run=str(run),config=config))
        print('RUN_DIRECTORY '+str(run),flush=True)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
            MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',BLIS_NUM_THREADS='1',CUDA_VISIBLE_DEVICES='0')
        with (run/'worker.stdout.log').open('a') as output,(run/'worker.stderr.log').open('a') as error:
            process=subprocess.Popen([str(scaling.PINNED_PYTHON),str(run/'workspace/overnight_search.py'),'--worker',str(run/'config.json')],
                cwd=run/'workspace',env=env,stdout=output,stderr=error,start_new_session=True,preexec_fn=guard.parent_death_signal)
            while process.poll() is None:
                if time.time()>=stop_epoch-10 or time.monotonic()>=config['deadline_monotonic']-10:
                    raise RequestedStop('Morning deadline reached')
                if (run/'STOP').exists():raise RequestedStop('STOP file requested')
                busy=guard.blockers([p for p in guard.lock_paths() if p not in leased],True)
                busy=[reason for reason in busy if reason!='CPU load exceeds idle threshold']
                if busy:raise RequestedStop('Yielding to production: '+', '.join(busy))
                time.sleep(.5)
        return process.returncode
    except RequestedStop as error:
        if 'run' in locals():
            (run/'STOP').touch();atomic_json(run/'service-stop.json',dict(reason=str(error),utc=datetime.now(timezone.utc).isoformat()))
        return 0
    finally:
        if process is not None and process.poll() is None:
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=3)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
        if 'run' in locals():
            checkpoint=run/'checkpoint.json'
            if checkpoint.exists() and process is not None and process.returncode:
                state=json.loads(checkpoint.read_text())
                if state.get('status') in ('running','starting'):
                    state.update(status='interrupted',stop_reason='Worker stopped; last committed cursor is resumable')
                    atomic_json(checkpoint,state)
            atomic_json(run/'preservation.json',dict(lattice_source_preserved=guard.package_hashes()==expected,
                source_snapshot_sha256=report['source_sha256'],binary_snapshot_sha256=report['binary_sha256'],
                finished_utc=datetime.now(timezone.utc).isoformat(),worker_exit_code=None if process is None else process.returncode))
        for handle in handles:handle.close()

def main():
    if sys.flags.optimize:raise SystemExit('Exact checks require ordinary Python')
    if len(sys.argv)==3 and sys.argv[1]=='--worker':return worker(json.loads(Path(sys.argv[2]).read_text()))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selection-report',required=True);parser.add_argument('--until',required=True)
    parser.add_argument('--max-bound',type=int,default=MAX_BASE);parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--start-bound',type=int,default=100_000_000_001,
        help='high-range selected search starts one third into the uniform ratio grid; use 1 for full-prefix validation')
    parser.add_argument('--backend',choices=('cpu','cuda'),help='override the measured selection for runner validation')
    parser.add_argument('--resume')
    args=parser.parse_args()
    if not 1<=args.start_bound<=args.max_bound<=MAX_BASE:parser.error('Invalid search interval')
    try:return coordinator(args)
    except (ValueError,RuntimeError,TimeoutError) as error:print(str(error),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
