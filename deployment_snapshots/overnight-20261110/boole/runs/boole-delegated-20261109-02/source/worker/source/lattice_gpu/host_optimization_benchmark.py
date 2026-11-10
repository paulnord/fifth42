#!/usr/bin/env python3
"""Bounded scratch CPU/CUDA adapter; requires external ADA guard and leases."""
import argparse
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import statistics
import sys
import time
import uuid

import coordinator_benchmark as helpers
import coordinator_packing
import coordinator_pipeline as pipeline
from engine_session import EngineSession
from adapter_runtime import open_session, verify_workers, normalized_counts, normalized_hits
import exact_host_opt
import overnight_search as night
import scaling_core as core
import wider_patch_experiment as widths

ROOT = Path(__file__).resolve().parent


def preparation(pool, specifications, bound, cap):
    start=time.perf_counter()
    rows=pool.map(exact_host_opt.prepare_certified,specifications,8)
    worker_wall=time.perf_counter()-start
    tasks,tokens=[r[0] for r in rows],[r[1] for r in rows]
    start=time.perf_counter()
    plan,geometry,payload=coordinator_packing.assemble_with_geometry(bound,cap,specifications,(),tasks,tokens)
    return plan,dict(pool_wall_seconds=worker_wall,assembly_geometry_seconds=time.perf_counter()-start,
                     worker_prepare_cpu_seconds=sum(r[2][1] for r in rows),
                     worker_certify_cpu_seconds=sum(r[2][3] for r in rows),
                     payload_bytes=payload,geometry_sha256=geometry,
                     certificate_sha256=plan.certificate_sha256,
                     patches=tuple((t.id,token,t.points) for t,token in zip(tasks,tokens))),tuple(r[2] for r in rows)


def trial(args,mode,repeat,width=None):
    began=time.perf_counter();deadline=time.monotonic()+120
    pool=multiprocessing.get_context('spawn').Pool(args.workers,initializer=exact_host_opt.initialize,
                                                  initargs=(args.source,args.cpus,mode))
    session=None
    try:
        limited=helpers.DeadlinePool(pool,deadline);warmed={}
        while len(warmed)<args.workers:
            warmed.update(limited.map(core.worker_identity,range(args.workers*4),1))
        verify_workers(warmed,args.cpus)
        session=open_session(args.engine,args.backend,deadline,1)
        engine=pipeline.OwnedEngine(session)
        name=f'{mode}-'+(f'w{width}-' if width else '')+f'{repeat}-{uuid.uuid4().hex}'
        startup=time.perf_counter()-began;started=time.perf_counter();cpu_started=time.process_time()
        rows=[];hits=set();signatures=[];points=patches=0
        if width is None:
            window=pipeline.Window(100000000001,200000000000,3751385984,3751387008,bits=222)
            with pipeline.TrialJournal(args.output/name,dict(trial=name,source_identity=args.fingerprint),window) as journal:
                for part in helpers.chunks(window,256):
                    specs=part.specifications();plan,info,durations=preparation(limited,specs,part.hi,part.cap)
                    chunk=pipeline.PreparedChunk(part,plan,info['patches'],info['geometry_sha256'],info['payload_bytes'],{},durations)
                    result=pipeline.execute_chunk(chunk,engine,trial=name,coordinator=0,timeout=max(.001,deadline-time.monotonic()))
                    commit_start=time.perf_counter();journal.commit(result);commit=time.perf_counter()-commit_start
                    signatures.append(dict(window=part.identity(),patches=info['patches'],geometry=info['geometry_sha256'],
                        certificate=plan.certificate_sha256,packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in plan.batches]))
                    hits.update(map(tuple,result['hits']));points+=plan.points;patches+=plan.tasks
                    rows.append(dict(preparation={k:v for k,v in info.items() if k!='patches'},execution=result['stages'],commit_seconds=commit))
            committed=True
        else:
            specs=widths.shared_specs(width)
            plan,info,durations=preparation(limited,specs,widths.HIGH_HI,42)
            exact_start=time.perf_counter();rpc=engine_seconds=kernel_seconds=0.
            for batch in plan.batches:
                response,wall=engine.run(batch.packet,timeout=max(.001,deadline-time.monotonic()))
                pipeline.validate_response_types(response)
                hits.update(core.decode_batch(batch,response,engine.backend));rpc+=wall;engine_seconds+=response['engine_seconds']
                if args.backend=='gpu':kernel_seconds+=response['kernel_seconds']
            execution=time.perf_counter()-exact_start
            points,patches=plan.points,plan.tasks
            signatures=[dict(width=width,patches=info['patches'],geometry=info['geometry_sha256'],
                certificate=plan.certificate_sha256,packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in plan.batches])]
            rows=[dict(preparation={k:v for k,v in info.items() if k!='patches'},execution_seconds=execution,
                       rpc_seconds=rpc,native_engine_seconds=engine_seconds,
                       cuda_kernel_seconds=kernel_seconds if args.backend=='gpu' else None,
                       transfer_seconds=None,packets=len(plan.batches))]
            # Width changes alter grid/chunk semantics. This standalone CPU width
            # comparison deliberately does not claim unchanged durable-commit cadence.
            committed=False
        seconds=time.perf_counter()-started;coordinator_cpu=time.process_time()-cpu_started
        shutdown_start=time.perf_counter();session.close();session=None;pool.close();pool.join()
        return dict(mode=mode,width=width,repeat=repeat,trial=name,status='exact_'+args.backend+'_verified',backend=args.backend,
                    steady_seconds=seconds,startup_seconds=startup,shutdown_seconds=time.perf_counter()-shutdown_start,
                    total_seconds=time.perf_counter()-began,coordinator_cpu_seconds=coordinator_cpu,
                    workers=args.workers,warmed_workers=len(warmed),cpus=args.cpus,
                    points=points,patches=patches,hits=sorted(hits),signatures=signatures,rows=rows,
                    durable_commits_included=committed,cuda_executed=args.backend=='gpu',no_full_box_claim=True)
    finally:
        if session:session.close()
        pool.terminate();pool.join()


def main():
    if sys.flags.optimize:raise SystemExit('Exact checks require ordinary Python')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT.parent/'lattice_prototype')
    parser.add_argument('--backend', choices=('emulated','gpu'), default='emulated')
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--repeats',type=int,default=5)
    parser.add_argument('--width-sweep',action='store_true')
    parser.add_argument('--widths',type=int,nargs='+',choices=widths.WIDTHS,default=list(widths.WIDTHS))
    args=parser.parse_args()
    if not 1<=args.workers<=16 or not 1<=args.repeats<=5:parser.error('Finite worker/repeat limits exceeded')
    args.source,args.engine=args.source.resolve(),args.engine.resolve()
    args.cpus=tuple(sorted(os.sched_getaffinity(0))[:args.workers])
    if len(args.cpus)!=args.workers:parser.error('Insufficient allowed CPUs')
    os.sched_setaffinity(0,set(args.cpus));night.initialize(args.source)
    args.fingerprint=helpers.source_identity(args.source,args.engine)
    args.output.mkdir(parents=True,exist_ok=False)
    cases=list(args.widths) if args.width_sweep else list(exact_host_opt.MODES)
    expected={};hits_expected=None;results=[]
    try:
        for repeat in range(args.repeats):
            order=cases[repeat%len(cases):]+cases[:repeat%len(cases)]
            for case in order:
                result=trial(args,'combined' if args.width_sweep else case,repeat,case if args.width_sweep else None)
                key=case if args.width_sweep else 'identical-patches'
                if key not in expected:expected[key]=result['signatures']
                elif result['signatures']!=expected[key]:raise RuntimeError('Exact task/packet identity changed')
                if hits_expected is None:hits_expected=result['hits']
                elif result['hits']!=hits_expected:raise RuntimeError('Exact hit sets differ')
                results.append(result);night.atomic_json(args.output/f'{repeat}-{case}.json',result)
                print(json.dumps(dict(case=case,repeat=repeat,seconds=result['steady_seconds'],points=result['points'])),flush=True)
        summary={str(case):dict(median_seconds=statistics.median(r['steady_seconds'] for r in results if (r['width'] if args.width_sweep else r['mode'])==case),
                               min_seconds=min(r['steady_seconds'] for r in results if (r['width'] if args.width_sweep else r['mode'])==case),
                               max_seconds=max(r['steady_seconds'] for r in results if (r['width'] if args.width_sweep else r['mode'])==case)) for case in cases}
        night.atomic_json(args.output/'summary.json',dict(status='passed',source_identity=args.fingerprint,
            regime='nested-width-union' if args.width_sweep else 'same-patch-arithmetic',repeats=args.repeats,
            modes=summary,all_exact_identities_equal_within_each_grid=True,all_hit_sets_equal=True,
            coverage_claim='Selected windows only',cuda_executed=args.backend=='gpu',
            durable_commits_included=not args.width_sweep,
            shared_ratio_union=[widths.pair(widths.LEFT),widths.pair(widths.RIGHT)] if args.width_sweep else None))
    except BaseException as error:
        night.atomic_json(args.output/'failure.json',dict(error=f'{type(error).__name__}: {error}',successful_trials=len(results)))
        raise


if __name__=='__main__':main()
