"""Ada collector for the separately frozen bulk-storage continuation."""
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'collector-settings.json').read_bytes());SETTINGS=BASE
OUT=Path(SETTINGS['output'])
def sha(raw):return hashlib.sha256(raw).hexdigest()
def atomic(path,row):
    temp=path.with_name(path.name+'.'+str(os.getpid())+'.tmp')
    with temp.open('w') as f:json.dump(row,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
def unit(name):
    result=subprocess.run(['systemctl','--user','show',name,'-p','ActiveState','-p','SubState','-p','MainPID','-p','NRestarts'],capture_output=True,text=True,check=True,timeout=5)
    return dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
def snapshot():
    global SETTINGS
    SETTINGS=dict(BASE,**json.loads(Path(BASE['active_configuration']).read_bytes()))
    raw=Path(SETTINGS['config']).read_bytes();manifest=Path(SETTINGS['manifest']).read_bytes()
    assert sha(raw)==SETTINGS['config_sha256'] and sha(manifest)==SETTINGS['manifest_sha256']
    cfg=json.loads(raw);local_run=Path(cfg['output']);run=Path(cfg['replica_output'])
    fingerprint=sha(json.dumps(dict(manifest_sha256=cfg['manifest_sha256'],config=cfg),sort_keys=True,separators=(',',':')).encode())
    service=unit(cfg['service_name']);timer=unit(cfg['deadline_service_name'].replace('.service','.timer'))
    cp_raw=(run/'checkpoint.json').read_bytes() if (run/'checkpoint.json').exists() else None
    cp=json.loads(cp_raw) if cp_raw else None
    replica=json.loads((run/'replica-state.json').read_bytes()) if cp else None
    if cp:
        assert sha(cp_raw)==replica['checkpoint_sha256'] and cp['identity']==replica['identity']
        assert cp['journal_offset']==replica['committed_bytes'] and cp['journal_sha256']==replica['journal_sha256']
        assert (run/'coverage.jsonl').stat().st_size>=cp['journal_offset']
    local_cp=json.loads((local_run/'checkpoint.json').read_bytes()) if (local_run/'checkpoint.json').exists() else None
    native=json.loads((local_run/'status.json').read_bytes()) if (local_run/'status.json').exists() else None
    supervisor=json.loads(Path(SETTINGS['supervisor_report']).read_bytes()) if Path(SETTINGS['supervisor_report']).exists() else None
    alerts=[]
    if native and native.get('error'):alerts.append(native['error'])
    if supervisor and supervisor.get('error'):alerts.append(supervisor['error'])
    first,last=cfg['initial_patch'],cfg['range_end']
    row=dict(snapshot_utc=datetime.now(timezone.utc).isoformat(),host=SETTINGS['host'],TEST_ONLY=False,
             run_id=cfg['run_id'],manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(raw),
             source_identity=fingerprint,ledger_claim_sha256=cfg['ledger_claim_sha256'],
             reserved_interval=[first,last],committed_interval=[first,cp['next_patch'] if cp else first],
             workers=cfg['workers'],backend=cfg['backend'],geometry_policy=cfg['geometry_policy'],
             stop_local=cfg['stop_local'],stop_epoch=cfg['stop_epoch'],service=service,deadline_timer=timer,
             completed_bound=None,journal_limit_bytes=cfg['journal_limit_bytes'],
             minimum_free_disk_bytes=cfg['minimum_free_disk_bytes'],report_interval_seconds=900,
             coverage_scope='Verified selected interval and parent lineage only; no full-box bound.',
             production_launched=bool(cp),mathematical_coverage_claim=False,
             phase='admitted_not_started',alerts=alerts,checkpoint=cp,worker_metrics={},supervisor=supervisor,local_next_patch=local_cp['next_patch'] if local_cp else first,replica=replica,group_limit=cfg['group_limit'],journal_storage='local durable journal; verified bulk replica every 60 seconds')
    if cp:
        assert cp['identity']==dict(trial=cfg['run_id'],source_identity=fingerprint)
        row['phase']=('attention_required' if alerts else 'running') if service['ActiveState']=='active' else ('failed' if alerts else 'stopped')
        row['worker_metrics']={key:native[key] for key in ('updated_utc','patches_per_second','gmp_audited_chunks','search_seconds','error','reason','prefetch','journal_buffer','dispatch_chunksize') if key in native}
        origin=first-cfg['parent_selected_patches']
        row.update(parent_committed_interval=[origin,first],combined_committed_interval=[origin,cp['next_patch']],
                   combined_selected_patches=cfg['parent_selected_patches']+cp['patches'],
                   parent_audit_sha256=cfg['parent_audit_sha256'])
    row['controller']=json.loads(Path(BASE['controller_state']).read_bytes()) if Path(BASE['controller_state']).exists() else None
    row['original_ledger_job']=cfg['ledger_job'];row['fresh_reservation']=cfg.get('fresh_reservation',False)
    return row
def main():
    while time.time()<SETTINGS['stop_epoch']+1800:
        try:
            row=snapshot();atomic(OUT/'status.json',row)
            atomic(OUT/'collector-health.json',dict(status='ok',updated_utc=row['snapshot_utc']))
        except Exception as error:
            atomic(OUT/'collector-health.json',dict(status='error',error=repr(error),updated_utc=datetime.now(timezone.utc).isoformat()))
        time.sleep(5)
if __name__=='__main__':main()
