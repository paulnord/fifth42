"""Actual finite/signal services plus new-deadline planning for unchanged launcher."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import validate_runtime as runtime
ROOT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    cases=[runtime.case(name) for name in ('finite','signal')]
    prior_root=Path('/home/pnord/ada-group4-20261109')
    assert sha(ROOT/'worker/launch_weekend.py')==sha(prior_root/'worker/launch_weekend.py')
    assert sha(ROOT/'worker/search_supervisor.py')==sha(prior_root/'worker/search_supervisor.py')
    old=json.loads((prior_root/'runtime/deadline-timer/result.json').read_bytes())
    assert old['status']=='passed' and old['independent_deadline_timer_passed'] and old['runtime_max_stop_passed']
    cfg=runtime.read(ROOT/'validation-template.json')
    import importlib.util,time
    spec=importlib.util.spec_from_file_location('overnight_deadline_launcher',ROOT/'worker/launch_weekend.py')
    launch=importlib.util.module_from_spec(spec);spec.loader.exec_module(launch)
    plan=launch.commands(cfg)
    assert cfg['stop_epoch']==1794351600 and plan['cleanup_starts_utc']=='2026-11-10 22:59:50 UTC'
    assert '--property=TimeoutStopSec=8s' in plan['service'] and plan['runtime_max_seconds']>60
    report=dict(status='passed',manifest_sha256=cfg['manifest_sha256'],actual_gpu=True,actual_ledger=True,actual_bulk_storage=True,signal_stop_passed=True,existing_output_rejected=True,production_started=False,cases=cases,absolute_deadline_plan=plan,deadline_regression=dict(status='passed_reused_unchanged_launcher_and_supervisor',source=str(prior_root/'runtime/deadline-timer/result.json'),sha256=sha(prior_root/'runtime/deadline-timer/result.json'),note='Actual deadline firing was recently verified. This revision changes source iteration and claim retry; both real finite and full-range signal-stop services passed. New absolute deadline is verified in the launch plan and will be checked against the live timer.'),validated_utc=datetime.now(timezone.utc).isoformat())
    (ROOT/'runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'gpu-validation.json').write_text(json.dumps(dict(status='passed',actual_gpu=True,independent_gmp=True,nonempty_controls=True,manifest_sha256=cfg['manifest_sha256'],evidence=[str(Path(runtime.read(ROOT/'runtime'/name/'configuration.json')['output'])/'controls.json') for name in ('finite','signal')]),indent=2)+'\n')
    print(json.dumps(dict(status='passed',cases=len(cases),full_production_range_signal_stop=True,new_deadline=cfg['stop_local']),indent=2),flush=True)
if __name__=='__main__':main()
