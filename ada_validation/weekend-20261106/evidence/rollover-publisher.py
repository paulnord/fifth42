"""Ada-owned pinned bulk-storage publisher; setup verifies inherited claim and parent archive."""
from datetime import datetime, timezone, timedelta
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
SETTINGS = json.loads((ROOT/'publisher-settings.json').read_bytes())
SHARE = Path(SETTINGS['share'])
LEDGER = Path('/mnt/nfs_share/fifth42-shared-20261107')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stable(row):
    return json.dumps(row, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return json.loads(Path(path).read_bytes())


def atomic(path, row):
    temporary = path.with_name(path.name+'.'+str(os.getpid())+'.tmp')
    with temporary.open('w') as stream:
        json.dump(row, stream, indent=2); stream.write('\n')
        stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)


def snapshot():
    spec=read(ROOT/'publication-spec.json')
    require(sha((SHARE/'publication-spec.json').read_bytes())==spec['collector_spec_sha256'],
            'Frozen collector specification changed')
    row=read(SHARE/'status.json')
    require(row['host']==SETTINGS['host'] and row['TEST_ONLY'] is False and row['run_id']==spec['run_id'],
            'Wrong bulk-storage collector identity')
    for key in ('manifest_sha256','config_sha256','source_identity','ledger_claim_sha256'):
        require(row[key]==spec[key],'Collector identity changed: '+key)
    first,last=spec['reserved_interval']
    require(row['reserved_interval']==[first,last], 'Collector reserved interval changed')
    require(row['stop_epoch']==spec['stop_epoch'] and
            abs(datetime.fromisoformat(row['stop_local']).timestamp()-spec['stop_epoch'])<.001,
            'Collector deadline changed')
    for key in ('workers','backend','geometry_policy','journal_limit_bytes','minimum_free_disk_bytes'):
        require(row[key]==spec[key],'Collector execution policy changed: '+key)
    require(row['completed_bound'] is None,'Selected work claimed full-box coverage')
    cp=row['checkpoint']
    if cp is None:
        require(row['phase'] in ('admitted_not_started','validating','stopping','failed') and row['production_launched'] is False and
                row['committed_interval']==[first,first] and row.get('mathematical_coverage_claim') is False,
                'Missing checkpoint is valid only before production starts')
    else:
        require(cp['identity']==dict(trial=spec['run_id'],source_identity=spec['source_identity']),
                'Checkpoint source/runtime identity changed')
        require(type(cp['next_patch']) is int and type(cp['patches']) is int and
                first<=cp['next_patch']<=last and cp['patches']==cp['next_patch']-first and
                row['committed_interval']==[first,cp['next_patch']] and
                cp['window']['first']==first and cp['window']['last']==last and
                cp['completed_bound'] is None,'Checkpoint interval/totals changed')
        parent=spec['parent_committed_interval']
        expected=dict(parent_committed_interval=parent,
                      combined_committed_interval=[parent[0],cp['next_patch']],
                      combined_selected_patches=spec['parent_selected_patches']+cp['patches'],
                      parent_audit_sha256=spec['parent_audit_sha256'])
        for key,value in expected.items():
            if key in row:require(row[key]==value,'Collector parent lineage changed: '+key)
            row[key]=value
    require(row['phase'] in ('admitted_not_started','validating','running','stopping','stopped','failed','attention_required'),
            'Unknown collector phase')
    if row['phase']=='stopped':
        supervisor=row.get('supervisor') or {}
        require(row.get('final_replica_verified') is True and
                row['local_next_patch']==cp['next_patch'] and
                row['service']['MainPID']=='0' and
                supervisor.get('leases_released') is True and supervisor.get('worker_exit_code')==0,
                'Terminal publication must wait for the final replicated checkpoint and released owner')
    age=time.time()-datetime.fromisoformat(row['snapshot_utc']).timestamp()
    require(-5<=age and (age<=120 or row['phase'] in ('stopped','failed')),'Stale collector snapshot')
    if row['phase'] in ('validating','running'):
        require(row['service']['ActiveState']=='active' and row['deadline_timer']['ActiveState']=='active',
                'Worker/deadline service inactive')
    row['journal_storage']='local durable journal; verified bulk replica every 60 seconds'
    if cp:require(cp.get('coverage_schema')=='logical-width8-physical-groups-v1','Grouped checkpoint schema missing')
    return row


def render(row):
    node=SETTINGS['host'].capitalize()
    if row['checkpoint'] is None:
        return f"""# {node} combined search

Updated: {row['snapshot_utc']}

State: **admitted, not started**. Run **{row['run_id']}**.
The protected child claim, final parent audit, archived parent and fresh runtime are verified.
Fresh interval: `{row['reserved_interval']}`. No new checkpoint or new mathematical coverage yet.
Deadline: **{row['stop_local']}**. Journal cap: {row['journal_limit_bytes']/1024**3:g} GiB.
Journal storage: **local durable journal, verified bulk copy every minute**. Reporting every **15 minutes**.

[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Selected coverage only; no completed full-box bound.
"""
    cp,metrics=row['checkpoint'],row['worker_metrics']
    return f"""# {node} combined search

Updated: {row['snapshot_utc']}

State: **{row['phase']}**. Run **{row['run_id']}**; {row['backend']} with {row['workers']} preparation workers.
Verified replicated cursor: **{cp['next_patch']:,}**.
New replicated logical patches: **{cp['patches']:,}** in {cp['chunks']:,} chunks.
Combined verified selected patches, including parents: **{row['combined_selected_patches']:,}**.
Fresh interval: `{row['reserved_interval']}`; replicated: `{row['committed_interval']}`.
Local cursor: {row['local_next_patch']:,}; physical tasks group up to {row['group_limit']} original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: {metrics.get('dispatch_chunksize')}; ready queue: {metrics.get('prefetch')}; buffer: {metrics.get('journal_buffer')}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **{row['journal_limit_bytes']/1024**3:g} GiB**;
free-space reserve: {row['minimum_free_disk_bytes']/1024**3:g} GiB.
Observed rate: **{metrics['patches_per_second']:,.0f} patches/s**; new independent GMP audits: {metrics['gmp_audited_chunks']:,}.
Deadline: **{row['stop_local']}**. Independent worker/deadline services on {node}; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: {row['alerts'] or 'None reported'}.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
"""


def remote_readback(bridge, receipt, row):
    environment = dict(os.environ, GIT_TERMINAL_PROMPT='0',
        GIT_SSH_COMMAND='ssh -i /home/pnord/.ssh/fifth42_status_20261105 -o IdentitiesOnly=yes '
        '-o IdentityAgent=none -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 '
        '-o UserKnownHostsFile=/home/pnord/fifth-lattice-gpu/github_known_hosts')
    with tempfile.TemporaryDirectory(prefix='readback-', dir=ROOT) as temporary:
        repo = str(Path(temporary)/'repository.git')
        def git(*args):
            result = subprocess.run(['git','--git-dir',repo,*args], env=environment,
                                    capture_output=True, timeout=45)
            require(result.returncode == 0, 'Fresh GitHub readback failed: '+result.stderr.decode()[-2000:])
            return result.stdout
        git('init','--bare',repo)
        git('fetch','--depth=1',bridge.REMOTE,receipt['commit'])
        require(git('rev-parse','FETCH_HEAD').decode().strip() == receipt['commit'], 'Readback commit mismatch')
        expected = {'status.json':(json.dumps(row,indent=2)+'\n').encode(), 'STATUS.md':render(row).encode()}
        for name, raw in expected.items():
            require(git('show','FETCH_HEAD:'+SETTINGS['publication_path']+'/'+name) == raw,
                    'GitHub content readback mismatch: '+name)
    return dict(status='passed', commit=receipt['commit'], verified_utc=datetime.now(timezone.utc).isoformat(),
                method='Fresh empty Git repository fetched exact commit from GitHub; both status files matched byte for byte.')


def publish(bridge, original, row):
    receipt = original(row)
    verified = remote_readback(bridge, receipt, row)
    path = ROOT/'publication-history.jsonl'
    previous = [json.loads(line) for line in path.read_bytes().splitlines()] if path.exists() else []
    event = dict(receipt=receipt, readback=verified, production_snapshot=row['host']==SETTINGS['host'])
    with path.open('a') as stream:
        stream.write(json.dumps(event,sort_keys=True)+'\n'); stream.flush(); os.fsync(stream.fileno())
    history = previous+[event]
    intervals = [datetime.fromisoformat(b['receipt']['published_utc']).timestamp()-
                 datetime.fromisoformat(a['receipt']['published_utc']).timestamp()
                 for a,b in zip(history,history[1:])]
    proof = dict(status=('collector_bound_not_started' if row['phase']=='admitted_not_started' else
                         'production_reporting') if event['production_snapshot'] else 'awaiting_bulk_collector',
                 checked_utc=verified['verified_utc'], repository=SETTINGS['repository'], branch=SETTINGS['branch'],
                 publication_path=SETTINGS['publication_path'], service_name=SETTINGS['service_name'],
                 first_push=history[0]['receipt'], first_readback=history[0]['readback'], latest_push=receipt,
                 latest_readback=verified, production_snapshot_published=any(item['production_snapshot'] for item in history),
                 latest_checkpoint=row['checkpoint'],final_replica_verified=row.get('final_replica_verified',False),
                 cadence=dict(interval_seconds=900, configured=True, observed_intervals_seconds=intervals,
                              next_due_utc=(datetime.now(timezone.utc)+timedelta(seconds=900)).isoformat(),
                              note='Regular updates use 900 seconds; startup and terminal changes publish immediately. Poll/network time can add seconds.'),
                 collector_bound=(ROOT/'binding.json').exists(),
                 production_worker_running=row['host']==SETTINGS['host'] and row['phase']=='running')
    service = subprocess.run(['systemctl','--user','show',SETTINGS['service_name'],
                              '-p','ActiveState','-p','SubState','-p','MainPID','-p','Restart'],
                             capture_output=True,text=True,timeout=5)
    proof['service'] = dict(line.split('=',1) for line in service.stdout.splitlines() if '=' in line)
    atomic(ROOT/'readiness.json',proof)
    atomic(SHARE/'ada-publisher-readiness.json',proof)
    return receipt


def main():
    path = ROOT/'bridge_base.py'
    require(sha(path.read_bytes()) == SETTINGS['bridge_base_sha256'], 'Frozen publisher transport changed')
    spec = importlib.util.spec_from_file_location('cabbage_bridge_base',path)
    bridge = importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)
    bridge.ROOT, bridge.SHARE, bridge.PUBLIC = ROOT, SHARE, SETTINGS['publication_path']
    bridge.snapshot, bridge.render = snapshot, render
    original = bridge.publish
    bridge.publish = lambda row:publish(bridge,original,row)
    return bridge.main()



_native_snapshot=snapshot
def snapshot():
    row=_native_snapshot()
    cursor=(row.get('checkpoint') or {}).get('next_patch',0)
    row['analytic_tail']=dict(interval=[10881882043,11250000001],
        excluded_cells=368117958,residual_caps_supported=[42,100],native_visits=0,
        proof_evidence='evidence/analytic-tail-proof.json',
        controller_status='native_boundary_reached' if cursor>=10881882112 and row['phase']=='stopped' else 'armed',
        native_counters_preserved=True)
    return row
_native_render=render
def render(row):
    return _native_render(row)+'\nAn independent exact symmetry proof excludes cells [10881882043, 11250000001) for absolute residuals at most 100. These 368,117,958 cells are analytic coverage with zero native visits. Native counters above retain their journal meaning. The controller stops after the crossing native window; overlapping native and analytic intervals are counted once. See [the exact proof](evidence/analytic-tail-proof.json).\n'

if __name__ == '__main__':
    raise SystemExit(main())
