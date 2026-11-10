"""Bounded persistent GPU comparison and stop checks, under ordinary held leases."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import signal
import statistics
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

import packed_worker
import policy

ROOT=Path(__file__).resolve().parent


def trial_config(case):
    base=policy.load_config(ROOT/'config.json')
    end=min(base['stop_epoch'],time.time()+(12 if case=='deadline' else 50))
    geometry='baseline' if case.startswith('baseline-') else 'adaptive'
    output=ROOT/'validation'/case
    output.mkdir(parents=True,exist_ok=False)
    return dict(base,run_id=base['run_id']+'-test-'+case,geometry_policy=geometry,
                test_chunk_limit=None if case in ('signal','deadline') else 32,
                output=str(output/'run'),stop_epoch=end,
                stop_local=datetime.fromtimestamp(end,ZoneInfo('America/Chicago')).isoformat())


def audit(folder,base):
    status=json.loads((folder/'status.json').read_bytes())
    checkpoint=json.loads((folder/'checkpoint.json').read_bytes())
    previous='0'*64;cursor=base['initial_patch'];chunks=points=audits=0;hits=set()
    with (folder/'coverage.jsonl').open('rb') as stream:
        for raw in stream:
            record=json.loads(raw);digest=record.pop('sha256')
            policy.require(record['previous_sha256']==previous and record['sequence']==chunks+1,
                           'Trial receipt chain order mismatch')
            policy.require(hashlib.sha256(policy.stable(record).encode()).hexdigest()==digest,
                           'Trial receipt hash mismatch')
            policy.require(record['window']['first']==cursor,'Trial coverage gap or duplicate')
            policy.require([p[0] for p in record['patches']]==list(range(cursor,record['window']['last'])),
                           'Trial per-patch manifest mismatch')
            policy.require([row for batch in record['batches'] for row in batch['native_counts']]==
                           [[p[0],p[2],p[2]] for p in record['patches']],
                           'Trial native counts incomplete')
            hits.update(map(tuple,record['hits']));points+=record['points'];chunks+=1
            audits+=record['independent_gmp_audited'];cursor=record['window']['last'];previous=digest
        policy.require(stream.tell()==checkpoint['journal_offset'],'Trial uncommitted suffix')
    policy.require((chunks,points,cursor,previous,sorted(hits))==
                   (checkpoint['chunks'],checkpoint['points'],checkpoint['next_patch'],
                    checkpoint['journal_sha256'],checkpoint['hits']),'Trial checkpoint mismatch')
    policy.require(status['error'] is None and status['next_patch']==cursor,'Trial status failure')
    return dict(status=status,checkpoint=checkpoint,hits=sorted(hits),audits=audits)


def execute(case):
    folder=ROOT/'validation'/case
    began=time.monotonic()
    result=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'--case',case],
                          capture_output=True,text=True,timeout=60)
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'stdout.txt').write_text(result.stdout)
    (folder/'stderr.txt').write_text(result.stderr)
    policy.require(result.returncode==0,'GPU validation case failed: '+case+' '+result.stderr[-1500:])
    return time.monotonic()-began


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=[*(p+'-'+str(i) for p in ('baseline','adaptive') for i in range(3)),
                                        'signal','deadline'])
    args=parser.parse_args()
    if args.case:
        return packed_worker.run(trial_config(args.case))
    base=policy.load_config(ROOT/'config.json')
    results=[];expected_hits=None
    for repeat,order in enumerate((('baseline','adaptive'),('adaptive','baseline'),('baseline','adaptive'))):
        for geometry in order:
            case=geometry+'-'+str(repeat);wall=execute(case)
            checked=audit(ROOT/'validation'/case/'run',base);status=checked['status']
            policy.require(status['status']=='completed_test' and status['chunks']==32,
                           'Finite comparison did not finish 32 chunks')
            policy.require(checked['audits']==1,'Periodic independent audit missing')
            if expected_hits is None:expected_hits=checked['hits']
            policy.require(checked['hits']==expected_hits,'Baseline/adaptive accepted exact hit sets differ')
            row=dict(geometry_policy=geometry,repeat=repeat,patches=status['patches'],
                     search_seconds=status['search_seconds'],patches_per_second=status['patches_per_second'],
                     process_wall_seconds=wall,points=checked['checkpoint']['points'],
                     exact_hits=checked['hits'],independent_audits=checked['audits'])
            results.append(row);print(json.dumps(row),flush=True)
    folder=ROOT/'validation'/'signal'
    process=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--case','signal'],
                             stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    try:
        until=time.monotonic()+15
        checkpoint=folder/'run/checkpoint.json'
        while not checkpoint.exists() and process.poll() is None and time.monotonic()<until:
            time.sleep(.05)
        policy.require(checkpoint.exists(),'Signal test never committed a checkpoint')
        process.send_signal(signal.SIGTERM)
        _,errors=process.communicate(timeout=10)
        policy.require(process.returncode==0,'Signal stop failed: '+errors[-1500:])
    finally:
        if process.poll() is None:process.kill();process.wait(timeout=5)
    stopped=audit(folder/'run',base)
    policy.require(stopped['status']['status']=='stopped' and
                   stopped['status']['reason']=='Stop requested','Signal stop was not clean')
    execute('deadline')
    deadline=audit(ROOT/'validation/deadline/run',base)
    policy.require(deadline['status']['status']=='stopped' and
                   'Absolute deadline' in deadline['status']['reason'],'Absolute deadline stop failed')
    medians={p:statistics.median(r['patches_per_second'] for r in results if r['geometry_policy']==p)
             for p in ('baseline','adaptive')}
    ratio=medians['adaptive']/medians['baseline']
    policy.require(ratio>1.1,'Measured persistent GPU gain is insufficient for adoption')
    report=dict(status='passed',trials=results,median_patches_per_second=medians,speedup=ratio,
                supported_nonempty_controls_every_trial=True,exact_hit_sets_equal=True,
                signal_stop_passed=True,absolute_deadline_stop_passed=True,
                production_coverage=False,workers=16,
                limitations=['Short matched tests at the verified final cursor; no full-domain bound or constant-rate forecast.',
                             'Timings include the pipeline, durable journal/checkpoint and periodic GMP audit overhead.'])
    (ROOT/'gpu-validation-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='trials'},indent=2),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
