#!/usr/bin/env python3
"""Bounded scratch CPU/CUDA adapter; requires external ADA guard and leases."""
import argparse
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import time
import uuid

import coordinator_benchmark as benchmark
import coordinator_batching as batching
import coordinator_pipeline as pipeline
from engine_session import EngineSession
from adapter_runtime import open_session, verify_workers, normalized_counts, normalized_hits
import overnight_search as night
import scaling_core as core


def execute_aggregated(plan, chunks, engine, trial, deadline):
    records = [dict(window=chunk.window.identity(), patches=chunk.patches,
                    points=chunk.plan.points, geometry_sha256=chunk.geometry_sha256,
                    certificate_sha256=chunk.plan.certificate_sha256,
                    complete=True, hits=set(), batches=[]) for chunk in chunks]
    timings = dict(rpc_seconds=0., engine_seconds=0., exact_decode_seconds=0., packets=[])
    for native_batch_id, (batch, routes) in enumerate(zip(plan.batches, plan.routes)):
        response, rpc_seconds = engine.run(batch.packet, timeout=max(.001, deadline-time.monotonic()))
        began = time.perf_counter()
        pipeline.validate_response_types(response)
        core.decode_batch(batch, response, engine.backend)
        packet_hash = hashlib.sha256(batch.packet.encode()).hexdigest()
        response_hash = hashlib.sha256(json.dumps(response,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        # Each local native task is routed back to its source checkpoint chunk.
        # Decode each complete subset through the same exact host checker.
        by_chunk = {}
        for local, route in enumerate(routes):
            by_chunk.setdefault(route.chunk_index, []).append(local)
        for chunk_index, locals_ in by_chunk.items():
            remap = {native:local for local,native in enumerate(locals_)}
            subbatch = core.encode_batch([batch.tasks[i] for i in locals_],chunks[chunk_index].window.cap)
            subset = dict(backend=engine.backend,box_complete=True,points_visited=subbatch.points,
                          counts=[dict(id=local,expected=batch.tasks[native].points,visited=batch.tasks[native].points)
                                  for local,native in enumerate(locals_)],
                          hits=[dict(hit,task=remap[hit['task']]) for hit in response['hits'] if hit['task'] in remap])
            record = records[chunk_index]
            record['hits'].update(core.decode_batch(subbatch,subset,engine.backend))
            record['batches'].append(dict(identity=dict(trial=trial,coordinator=0,
                window=chunks[chunk_index].window.identity(),batch=len(record['batches']),
                packet_sha256=packet_hash,native_batch=native_batch_id,native_request_id=response.get('request_id'),
                native_task_ids=locals_),points=subbatch.points,patch_ids=[t.id for t in subbatch.tasks],
                response_sha256=response_hash, backend=engine.backend,
                native_counts=normalized_counts(batch,response,locals_),
                native_hit_records=normalized_hits(batch,response,locals_)))
        timings['exact_decode_seconds'] += time.perf_counter()-began
        timings['rpc_seconds'] += rpc_seconds
        timings['engine_seconds'] += response.get('engine_seconds',0.)
        timings['packets'].append(dict(tasks=len(batch.tasks),points=batch.points,packet_bytes=len(batch.packet.encode()),
                                       rpc_seconds=rpc_seconds,engine_seconds=response.get('engine_seconds'),
                                       kernel_seconds=response.get('kernel_seconds') if engine.backend=='gpu' else None,transfer_seconds=None))
    for record in records:
        record['hits']=sorted(record['hits'])
    return records,timings


def run(args, max_tasks, repeat, output):
    started=time.perf_counter();deadline=time.monotonic()+120
    pool=multiprocessing.get_context('spawn').Pool(args.workers,initializer=night.initialize,
                                                  initargs=(args.source,args.cpus))
    session=None
    try:
        bounded=benchmark.DeadlinePool(pool,deadline)
        warmed={}
        while len(warmed)<args.workers:
            warmed.update(bounded.map(core.worker_identity,range(args.workers*4),1))
        verify_workers(warmed,args.cpus)
        session=open_session(args.engine,args.backend,deadline,1)
        trial=f'batch-{max_tasks}-{repeat}-{uuid.uuid4().hex}'
        startup=time.perf_counter()-started;begin=time.perf_counter()
        chunks=tuple(pipeline.prepare_chunk(bounded,window,'packed') for window in benchmark.chunks(args.window,256))
        preparation=time.perf_counter()-begin
        payload=sum(chunk.payload_bytes for chunk in chunks)
        if payload>128*1024*1024:raise ValueError('Sweep exceeds 128 MiB canonical serialization allowance')
        aggregate_start=time.perf_counter()
        plan=batching.aggregate_batches(chunks,max_tasks=max_tasks)
        aggregate=time.perf_counter()-aggregate_start
        records,timings=execute_aggregated(plan,chunks,pipeline.OwnedEngine(session),trial,deadline)
        commit_start=time.perf_counter()
        with pipeline.TrialJournal(output/trial,dict(trial=trial,source_identity=args.fingerprint),args.window) as journal:
            for record in records:journal.commit(record)
            if journal.state['patches']!=args.window.last-args.window.first:
                raise RuntimeError('Aggregated output did not cover the fixed union')
        commit=time.perf_counter()-commit_start
        end_to_end=time.perf_counter()-begin
        signature=[dict(window=c.window.identity(),patches=c.patches,geometry_sha256=c.geometry_sha256,
                        certificate_sha256=c.plan.certificate_sha256,hits=r['hits'],
                        native_counts=sorted(v for b in r['batches'] for v in b['native_counts']),
                        native_hit_records=sorted(v for b in r['batches'] for v in b['native_hit_records'])) for c,r in zip(chunks,records)]
        shutdown_start=time.perf_counter();session.close();session=None;pool.close();pool.join()
        return dict(max_packet_tasks=max_tasks,repeat=repeat,trial=trial,status='exact_'+args.backend+'_verified',backend=args.backend,
                    source_identity=args.fingerprint,patches=args.window.last-args.window.first,points=plan.points,
                    original_checkpoint_chunk_patches=256,checkpoint_commits=len(chunks),
                    serialized_payload_bytes=payload,startup_seconds=startup,preparation_seconds=preparation,
                    aggregation_seconds=aggregate,commit_seconds=commit,end_to_end_seconds=end_to_end,
                    shutdown_seconds=time.perf_counter()-shutdown_start,total_seconds=time.perf_counter()-started,
                    timings=timings,signatures=signature,gpu_measured=args.backend=='gpu',transfer_seconds=None,
                    no_full_box_claim=True)
    finally:
        if session:session.close()
        pool.terminate();pool.join()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    root=Path(__file__).resolve().parents[1]
    parser.add_argument('--source',type=Path,default=root/'lattice_prototype')
    parser.add_argument('--backend', choices=('emulated','gpu'), default='emulated')
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--repeats',type=int,default=1)
    args=parser.parse_args()
    if not 1<=args.workers<=16 or not 1<=args.repeats<=5:parser.error('Finite worker/repeat limits exceeded')
    args.source=args.source.resolve();args.engine=args.engine.resolve()
    args.cpus=tuple(sorted(os.sched_getaffinity(0))[:args.workers])
    if len(args.cpus)!=args.workers:parser.error('Insufficient CPU allocation')
    os.sched_setaffinity(0,set(args.cpus));night.initialize(args.source)
    args.window=pipeline.Window(100000000001,200000000000,3751385984,3751385984+4096,bits=222)
    args.fingerprint=benchmark.source_identity(args.source,args.engine)
    args.output.mkdir(parents=True,exist_ok=False)
    trials=[];expected=None;sizes=(256,512,1024,2048,4096)
    for repeat in range(args.repeats):
        order=sizes[repeat%len(sizes):]+sizes[:repeat%len(sizes)]
        for size in order:
            result=run(args,size,repeat,args.output)
            if expected is None:expected=result['signatures']
            elif result['signatures']!=expected:raise RuntimeError('Batch-size sweep changed exact coverage or hits')
            night.atomic_json(args.output/f'{repeat}-{size}.json',result)
            trials.append({key:value for key,value in result.items() if key!='signatures'})
            print(json.dumps(dict(max_packet_tasks=size,packets=len(result['timings']['packets']),
                end_to_end_seconds=result['end_to_end_seconds'],rpc_seconds=result['timings']['rpc_seconds'])),flush=True)
    night.atomic_json(args.output/'summary.json',dict(status='passed',window=args.window.identity(),cpus=args.cpus,
        workers=args.workers,repeats=args.repeats,trials=trials,exact_union_certificates_geometry_hits_equal=True,
        cuda_executed=args.backend=='gpu',backend=args.backend,transfer_measurement='Not separately instrumented',no_full_box_claim=True))


if __name__=='__main__':main()
