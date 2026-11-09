"""Finish auditing the stopped trial using journal evidence for collected units."""
from datetime import datetime,timezone
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W),'/home/pnord/boole-continuation-check-20261108']
import policy,audit_grouped
from check_continuation import owner_is_locked
def read(p):return json.loads(p.read_bytes())
def main():
    folder=ROOT/'runtime/deadline-timer';cfg=read(folder/'configuration.json')
    local=Path(cfg['output']);replica=Path(cfg['replica_output'])
    cp=read(local/'checkpoint.json');status=read(local/'status.json');sup=read(folder/'supervisor-report.json')
    assert sup['status']=='finished' and sup['error'] is None and sup['worker_exit_code']==0 and sup['leases_released']
    assert status['status']=='stopped' and status['error'] is None and cp['next_patch']<cfg['range_end']
    finished=datetime.fromisoformat(status['updated_utc']).timestamp()
    assert cfg['stop_epoch']-11<=finished<cfg['stop_epoch']
    cmd=['journalctl','--user','-u',cfg['service_name'],'-u',cfg['deadline_service_name'],'-u',cfg['deadline_service_name'].replace('.service','.timer'),'--since','@'+str(int(cfg['stop_epoch']-120)),'--no-pager','-o','short-iso']
    evidence=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=15)
    assert 'Service reached runtime time limit.' in evidence.stdout
    assert 'Starting '+cfg['deadline_service_name'] in evidence.stdout and 'Finished '+cfg['deadline_service_name'] in evidence.stdout
    (folder/'systemd-deadline.log').write_text(evidence.stdout)
    result=audit_grouped.audit_suffix(local,dict(checkpoint=dict(next_patch=cfg['initial_patch']),config=cfg),cp,'fresh',cfg['gmp_audit_period'])
    cleanup=['/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python','-B',str(W/'finalize_replica.py'),'--config',str(folder/'configuration.json'),'--config-sha256',policy.digest(folder/'configuration.json')]
    done=subprocess.run(cleanup,capture_output=True,text=True,check=True,timeout=120)
    assert (local/'checkpoint.json').read_bytes()==(replica/'checkpoint.json').read_bytes()
    assert audit_grouped.audit_suffix(replica,dict(checkpoint=dict(next_patch=cfg['initial_patch']),config=cfg),cp,'fresh',cfg['gmp_audit_period'])==result
    controls=read(local/'controls.json')
    assert controls['status']=='passed' and all(c['hits'] and c['full_oracle_equal'] for c in controls['cases'])
    assert not owner_is_locked(Path(cfg['ledger_root'])/'jobs'/cfg['ledger_job']/'journal.jsonl')
    policy.validate_archive(cfg)
    result.update(case='deadline-timer',status='passed',actual_systemd=True,TEST_ONLY=True,controls='passed',original_parent_unchanged=True,leases_released=True,hard_deadline=cfg['stop_local'],worker_finished_epoch=finished,runtime_max_stop_passed=True,independent_deadline_timer_passed=True,timer_evidence=dict(command=cmd,stdout=evidence.stdout),completion_method='Read-only completion of the already stopped trial after --collect unloaded its transient timer; no recomputation.',finished_utc=datetime.now(timezone.utc).isoformat(),final_replication=dict(command=cleanup,stdout=done.stdout))
    (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    report=read(ROOT/'runtime-validation.json')
    for case in report['cases']:
        if case['case']=='deadline':case['case']='interval-completion-before-deadline'
    report['cases'].append(result)
    report['runtime_max_deadline_passed']=True;report['independent_deadline_timer_passed']=True
    report['deadline_test_note']='The first deadline trial completed its small interval early. The longer deadline-timer trial confirmed the runtime cutoff and actual independent stop-service execution in the system journal; transient --collect units may already be unloaded at readback.'
    (ROOT/'runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    for script in ['prepare_launch.py','prepare_reporting.py']:
        subprocess.run(['/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python','-B',str(ROOT/script)],cwd=ROOT,check=True,timeout=30)
    print(json.dumps({k:v for k,v in result.items() if k not in ['timer_evidence','final_replication']},indent=2),flush=True)
if __name__=='__main__':main()
