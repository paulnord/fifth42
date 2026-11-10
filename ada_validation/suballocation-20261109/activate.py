"""One explicit, measured Ada handoff; no failed production run is resumed."""
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
W = ROOT/'worker'
OLD = Path('/home/pnord/ada-overnight-20261109/worker')
PYTHON = '/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
EVENTS = []
def read(p): return json.loads(Path(p).read_bytes())
def write(p, x): Path(p).write_text(json.dumps(x, indent=2)+'\n')
def run(args, timeout=45):
    start = time.monotonic()
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    row = dict(command=args, exit_code=p.returncode, seconds=time.monotonic()-start,
               stdout=p.stdout, stderr=p.stderr)
    EVENTS.append(row)
    write(ROOT/'activation-events.json', EVENTS)
    print(json.dumps(row), flush=True)
    p.check_returncode()
def script(name): run([PYTHON, '-B', str(ROOT/name)])
def main():
    assert not (ROOT/'activation-start.json').exists()
    old = read(OLD/'config.json')
    assert read(ROOT/'rolling-seal-status.json')['status']=='caught_up'
    assert read(Path(old['output'])/'status.json')['status']=='running'
    write(ROOT/'activation-start.json', dict(started_epoch=time.time(), started_utc=datetime.now(timezone.utc).isoformat()))
    run(['systemctl','--user','stop',old['service_name']], 12)
    (ROOT/'FINALIZE_PARENT').touch()
    until = time.monotonic()+40
    while not (ROOT/'sealed-parent.json').exists():
        if time.monotonic()>until: raise TimeoutError('Stopped parent seal did not finish')
        time.sleep(.1)
    script('prepare_prototype.py')
    script('run_gpu_probes.py')
    probes = read(ROOT/'gpu-probe-results.json')
    assert probes['status']=='passed'
    cfg = read(W/'config.json')
    mf = read(W/'release-manifest.json'); baseline = read(OLD/'release-manifest.json')
    changed = sorted(n for n in mf['files'] if mf['files'][n]!=baseline['files'].get(n))
    assert changed==['policy.py','search_supervisor.py','suballocation_guard.py','transition_resources.py']
    validation = dict(status='passed', manifest_sha256=cfg['manifest_sha256'], actual_gpu=True,
                      actual_parent_lease=True, signal_stop_passed=True, cases=probes['cases'],
                      unchanged_math_packet_kernel_and_gmp=True, changed_runtime_files=changed,
                      baseline_manifest_sha256=old['manifest_sha256'], validated_utc=datetime.now(timezone.utc).isoformat())
    write(ROOT/'gpu-validation.json', validation)
    write(ROOT/'runtime-validation.json', validation)
    script('freeze_allocation.py')
    cfg = read(W/'config.json')
    runtime = max(60, int(cfg['stop_epoch']+1800-time.time()))
    run(['systemd-run','--user','--unit=ada-suballocation-parent-20261109','--collect',
         '--service-type=exec','--property=Restart=no','--property=UMask=0077',
         '--property=RuntimeMaxSec='+str(runtime),'--working-directory='+str(ROOT),
         '--property=StandardOutput=append:'+str(ROOT/'parent.stdout.log'),
         '--property=StandardError=append:'+str(ROOT/'parent.stderr.log'),
         PYTHON,'-B','-u',str(ROOT/'parent_coordinator.py'),
         '--grant',cfg['suballocation_grant_file'],'--grant-sha256',cfg['suballocation_grant_sha256'],
         '--retained-config',str(W/'config.json')])
    until = time.monotonic()+5
    while not (Path(cfg['ledger_root'])/'coordinator-state.json').exists():
        assert time.monotonic()<until, 'Parent coordinator failed to acquire lease'
        time.sleep(.05)
    script('prepare_launch.py')
    script('prepare_reporting.py')
    script('start_production.py')
    print('Bounded Ada production launched; verify the first audited prefix before enabling Boole.',flush=True)
if __name__=='__main__': main()
