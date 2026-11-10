#!/usr/bin/env python3
"""Read-only grouping gate; emits a proposal, never installs or starts services."""
import argparse, hashlib, json, math, statistics, time
from pathlib import Path

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def choose(samples, first, source_identity, host, measured_host):
    # Never transfer a speed finding between hosts or coordinates implicitly.
    if host != measured_host: raise ValueError('benchmark belongs to a different host')
    rows=[s for s in samples if s.get('first')==first and s.get('group_limit') in (4,8)]
    by={g:[s for s in rows if s['group_limit']==g] for g in (4,8)}
    for g, rs in by.items():
        if len(rs)<3: raise ValueError('need at least three repeats per group at current cursor')
        if len({r.get('repeat') for r in rs}) != len(rs): raise ValueError('duplicate repeat')
        for r in rs:
            if not all(r.get(k) is True for k in ('TEST_ONLY','recovery_passed','durable','durable_journal_closed_before_timing_end')): raise ValueError('missing correctness/durability gate')
            if r.get('status')!='passed' or r.get('audit_count',0)<1: raise ValueError('failed audit/status')
            if r.get('workers')!=16 or r.get('patches')!=32768: raise ValueError('unexpected benchmark scope')
            if not math.isfinite(r.get('steady_seconds',0)) or r['steady_seconds']<=0: raise ValueError('invalid time')
        for key in ('points','physical_tasks','signatures_sha256','hits'):
            if len({json.dumps(r[key],sort_keys=True) for r in rs})!=1: raise ValueError('same-group repeat mismatch')
    if by[4][0]['hits'] != by[8][0]['hits']: raise ValueError('hit sets differ')
    med={g:statistics.median(r['patches']/r['steady_seconds'] for r in rs) for g,rs in by.items()}
    gain=med[8]/med[4]
    group=8 if gain>=1.10 else 4
    return {'group_limit':group,'dispatch_chunksize':2 if group==8 else 4,
            'benchmark_first':first,'benchmark_last':first+32768,
            'median_cells_per_second':med,'ratio_group8_over4':gain,
            'host':host,'source_identity':source_identity,
            'scope':'bounded canary only; not a general region-wide speed claim',
            'maximum_canary_cells':1048576 if group==8 else 0,
            'automatic_resume':False,'production_started':False}

def reconcile(local, replica, supervisor):
    if local != replica: raise ValueError('local and replica checkpoints differ')
    if supervisor.get('worker_exit_code')!=0 or supervisor.get('leases_released') is not True or supervisor.get('error') is not None: raise ValueError('supervisor not clean/final')
    n=local['next_patch']; w=local['window']
    if not isinstance(n,int) or not w['first']<=n<=w['last']: raise ValueError('checkpoint cursor outside window')
    return n

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host',choices=['ada','boole','cabbage'],required=True)
    p.add_argument('--config',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--replica-checkpoint',required=True);p.add_argument('--supervisor',required=True)
    p.add_argument('--receipt',help='JSON with measured_host, source_identity and samples_file (relative to receipt)')
    p.add_argument('--output',required=True)
    a=p.parse_args(); c=json.loads(Path(a.config).read_text()); cp=json.loads(Path(a.checkpoint).read_text())
    first=reconcile(cp,json.loads(Path(a.replica_checkpoint).read_text()),json.loads(Path(a.supervisor).read_text()))
    if digest(c['manifest'])!=c['manifest_sha256']: raise ValueError('source manifest changed')
    expected=hashlib.sha256(json.dumps(dict(manifest_sha256=c['manifest_sha256'],config=c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if cp['identity'] != dict(trial=c['run_id'],source_identity=expected): raise ValueError('checkpoint identity differs from configuration')
    plan={'group_limit':4,'dispatch_chunksize':4,'reason':'default; no matching host/current-cursor benchmark','production_started':False,'automatic_resume':False}
    if a.receipt:
        rp=Path(a.receipt);r=json.loads(rp.read_text())
        if r['parent_checkpoint_sha256']!=digest(a.checkpoint):raise ValueError('checkpoint moved since benchmark')
        if r['source_identity']!=cp['identity']['source_identity']:raise ValueError('benchmark uses different source identity')
        samples=rp.parent/r['samples_file']
        if digest(samples)!=r['samples_sha256']:raise ValueError('benchmark sample hash mismatch')
        plan=choose(json.loads(samples.read_text()),first,r['source_identity'],a.host,r['measured_host'])
    plan.update(host=a.host,parent_cursor=first,parent_checkpoint_sha256=digest(a.checkpoint),old_config_sha256=digest(a.config),deadline_epoch=c['stop_epoch'],remaining_end=c['range_end'])
    if time.time()>=c['stop_epoch']:raise ValueError('authorized deadline expired; no continuation proposal')
    if plan['group_limit']==8: plan['canary_end']=min(first+plan['maximum_canary_cells'],c['range_end'])
    with open(a.output,'x') as f:json.dump(plan,f,indent=2);f.write('\n')
if __name__=='__main__':main()
