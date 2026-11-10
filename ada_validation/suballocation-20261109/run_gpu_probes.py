"""Two isolated real GPU services during an explicitly bounded owner handoff."""
import importlib.util,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
sys.path[:0]=[str(W)]
import policy,audit_grouped
PYTHON='/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
def read(p):return json.loads(Path(p).read_bytes())
def command(args,timeout=15):
    done=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
    if done.returncode:raise RuntimeError(repr(args)+' '+done.stderr[-1500:])
    return done.stdout
def case(name):
    folder=ROOT/'preflight'/name;cf=folder/'configuration.json';c=read(cf)
    parent=subprocess.Popen([PYTHON,'-B','-u',str(ROOT/'parent_coordinator.py'),'--grant',c['suballocation_grant_file'],'--grant-sha256',c['suballocation_grant_sha256'],'--retained-config',str(cf),'--test-only'],stdout=(folder/'coordinator.stdout.log').open('w'),stderr=(folder/'coordinator.stderr.log').open('w'),start_new_session=True)
    timer=c['deadline_service_name'].replace('.service','.timer');output=Path(c['output']);replica=Path(c['replica_output'])
    try:
        until=time.monotonic()+5
        while not (Path(c['ledger_root'])/'coordinator-state.json').exists():
            assert parent.poll() is None,'Probe parent failed';assert time.monotonic()<until;time.sleep(.02)
        policy.load_config(cf)
        spec=importlib.util.spec_from_file_location('probe_launcher',W/'launch_weekend.py');launch=importlib.util.module_from_spec(spec);spec.loader.exec_module(launch)
        plan=launch.commands(c);plan['service'][-1]=str(cf)
        command(plan['timer']);command(plan['service']);signaled=False;until=time.monotonic()+20
        while time.monotonic()<until:
            state=command(['systemctl','--user','show',c['service_name'],'-p','ActiveState','--value']).strip()
            if name=='signal' and not signaled and (output/'checkpoint.json').exists() and read(output/'checkpoint.json')['chunks']>=2:
                command(['systemctl','--user','stop',c['service_name']]);signaled=True
            if state in ('inactive','failed'):break
            time.sleep(.1)
        else:raise TimeoutError('Probe exceeded the twenty-second service allowance')
        sup=read(W/'supervisor-report.json');status=read(output/'status.json');cp=read(output/'checkpoint.json')
        assert sup['status']=='finished' and sup['error'] is None and sup['worker_exit_code']==0 and sup['leases_released']
        assert status['status']==('completed_test' if name=='finite' else 'stopped') and status['error'] is None
        checked=audit_grouped.audit_suffix(output,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',1)
        command([PYTHON,'-B',str(W/'finalize_replica.py'),'--config',str(cf),'--config-sha256',policy.digest(cf)],timeout=15)
        assert (output/'checkpoint.json').read_bytes()==(replica/'checkpoint.json').read_bytes()
        assert audit_grouped.audit_suffix(replica,dict(checkpoint=dict(next_patch=c['initial_patch']),config=c),cp,'fresh',1)==checked
        controls=read(output/'controls.json');assert controls['status']=='passed' and all(x['hits'] and x['full_oracle_equal'] for x in controls['cases'])
        result=dict(status='passed',case=name,TEST_ONLY=True,actual_gpu=True,actual_parent_lease=True,independent_gmp_every_chunk=True,source_manifest_sha256=c['manifest_sha256'],**checked)
        (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);return result
    finally:
        subprocess.run(['systemctl','--user','stop',c['service_name'],timer],capture_output=True,timeout=10)
        parent.terminate()
        try:parent.wait(timeout=3)
        except subprocess.TimeoutExpired:parent.kill();parent.wait(timeout=3)
        for n in ['worker.stdout.log','worker.stderr.log','supervisor-report.json','service.stdout.log','service.stderr.log']:
            p=W/n
            if p.exists():p.rename(folder/n)
def main():
    results=[case(n) for n in ('finite','signal')]
    (ROOT/'gpu-probe-results.json').write_text(json.dumps(dict(status='passed',cases=results),indent=2)+'\n')
if __name__=='__main__':main()
