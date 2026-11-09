"""Isolate GPU request aggregation while preserving exact tasks and candidates."""
import hashlib,json,os,statistics,subprocess,time
from pathlib import Path
import buffered_pipeline as b
import adapter_runtime as adapter
import coordinator_pipeline as pipeline
import runtime_initialize,scaling_core as core,width_coverage as coverage
from run_validation import helper
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
class Serial:
    def map(self,fn,args,chunksize):return list(map(fn,args))
def main(existing_guard=None):
    guard=existing_guard or helper();handles=[];engine=None
    if existing_guard is None:
        resources=guard.resources();assert not guard.hardware_blockers();handles,leased=guard.acquire_leases(resources,False)
    try:
        os.sched_setaffinity(0,set(range(16)));runtime_initialize.initialize(W/'source/lattice_prototype')
        engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+180);results=[]
        for region,first,factor in [('ada',4398974336,2),('cabbage',2300778112,4)]:
            chunks=[coverage.prepare_chunk(Serial(),pipeline.Window(100000000001,200000000000,first+i*256,first+(i+1)*256,8,222,42,'adaptive'),factor) for i in range(4)]
            tasks=tuple(task for chunk in chunks for batch in chunk.plan.batches for task in batch.tasks)
            expected_hits=None;expected_counts=None;cases={}
            for group in (1,2,4):
                packets=[]
                for index in range(0,4,group):
                    items=tuple(t for chunk in chunks[index:index+group] for batch in chunk.plan.batches for t in batch.tasks)
                    packets.append(core.encode_batch(items,42))
                counts=[];hits=set()
                for packet in packets:
                    raw,_=engine.run(packet.packet,timeout=20);pipeline.validate_response_types(raw);hits.update(core.decode_batch(packet,raw,'gpu'));counts+=adapter.normalized_counts(packet,raw)
                    ref=json.loads(subprocess.run([str(W/'bin/gmp_reference')],input=packet.packet,text=True,capture_output=True,check=True,timeout=20).stdout)
                    assert adapter.normalized_counts(packet,raw)==adapter.normalized_counts(packet,ref) and adapter.normalized_hits(packet,raw)==adapter.normalized_hits(packet,ref)
                if expected_counts is None:expected_counts=counts;expected_hits=hits
                assert counts==expected_counts and hits==expected_hits
                cases[group]=packets
            samples={group:[] for group in cases}
            for repeat in range(15):
                order=[1,2,4] if repeat%2==0 else [4,2,1]
                for group in order:
                    begin=time.monotonic()
                    for packet in cases[group]:raw,_=engine.run(packet.packet,timeout=20);core.decode_batch(packet,raw,'gpu')
                    samples[group].append(time.monotonic()-begin)
            medians={str(group):statistics.median(values) for group,values in samples.items()}
            results.append(dict(region=region,logical_cells=1024,groups=medians,request_throughput_ratio={group:medians['1']/value for group,value in medians.items()},same_tasks_counts_candidates=True,gmp_all_packets=True,hits=sorted(expected_hits),scope='Cached native requests only; no preparation, durable journal or restart changes.'))
        report=dict(status='passed',results=results,production_protocol_changed=False,production_coverage=False)
        (ROOT/'gpu-aggregation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    finally:
        if engine:engine.close()
        for handle in handles:handle.close()
if __name__=='__main__':main()
