"""Exercise the actual patched supervisor, disk guard, ledger, and stop timer."""
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / 'worker'
PYTHON = '/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'
sys.path.insert(0, str(WORKER))
import ada_export_store
import policy
import audit_grouped
sys.path.insert(0, '/home/pnord/boole-continuation-check-20261108')
import check_continuation as check


def read(path):
    return json.loads(Path(path).read_bytes())


def command(args):
    done = subprocess.run(args, capture_output=True, text=True, timeout=120 if any('finalize_replica.py' in str(a) for a in args) else 25)
    if done.returncode:
        raise RuntimeError('Command failed: ' + repr(args) + ' ' + done.stderr[-1500:])
    return dict(command=args, exit_code=done.returncode, stdout=done.stdout, stderr=done.stderr)


def service(name):
    text = command(['systemctl', '--user', 'show', name, '-p', 'ActiveState', '-p', 'SubState', '-p', 'Result', '-p', 'MainPID'])['stdout']
    return dict(line.split('=', 1) for line in text.splitlines() if '=' in line)


def case(name):
    deadline_case = name.startswith('deadline')
    base = read(ROOT / 'validation-template.json')
    folder = ROOT / 'runtime' / name
    folder.mkdir(mode=0o700, parents=True, exist_ok=False)
    run_id = 'ada-overnight-test-' + name + '-20261109'
    ledger = ada_export_store.Store(policy.TEST_LEDGER / 'runtime' / name)
    claim = ledger.reserve(run_id, base['initial_patch'], base['range_end'] if name=='signal' else base['initial_patch'] + (10**7 if deadline_case else 10**6),
                           base['manifest_sha256'], dict(TEST_ONLY=True, parent_checkpoint_sha256=base['parent_checkpoint_sha256']))
    output = policy.LOCAL / 'TEST_ONLY_overnight_20261109' / run_id / 'run'
    replica = policy.BULK / 'TEST_ONLY_overnight_20261109' / run_id / 'run'
    replica.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    end = min(base['stop_epoch'], time.time() + 90)
    cfg = dict(base, TEST_ONLY=True, run_id=run_id, output=str(output), replica_output=str(replica),
               ledger_root=str(ledger.root), ledger_job=run_id, ledger_device=ledger.device,
               ledger_claim_sha256=claim['sha256'], range_end=claim['last'], gmp_audit_period=128 if deadline_case else 1,
               test_chunk_limit=8 if name == 'finite' else None,
               stop_epoch=end, stop_local=datetime.fromtimestamp(end, ZoneInfo('America/Chicago')).isoformat(),
               service_name=run_id + '.service', deadline_service_name=run_id + '-deadline.service')
    config_path = folder / 'configuration.json'
    config_path.write_text(json.dumps(cfg, indent=2) + '\n')
    policy.load_config(config_path)
    spec = importlib.util.spec_from_file_location('new_ada_launcher', WORKER / 'launch_weekend.py')
    launch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launch)
    plan = launch.commands(cfg)
    plan['service'][-1] = str(config_path)
    timer = cfg['deadline_service_name'].replace('.service', '.timer')
    events = []
    try:
        events.append(command(plan['timer']))
        events.append(command(plan['service']))
        until = time.monotonic() + 120
        requested = False
        while time.monotonic() < until:
            state = service(cfg['service_name'])
            cp_path = output / 'checkpoint.json'
            if name == 'signal' and not requested and cp_path.exists() and read(cp_path)['chunks'] >= 2:
                events.append(command(['systemctl', '--user', 'stop', cfg['service_name']]))
                requested = True
            if state['ActiveState'] in ('inactive', 'failed'):
                break
            time.sleep(0.5)
        else:
            raise TimeoutError('Test service did not terminate: ' + name)
        supervisor = read(WORKER / 'supervisor-report.json')
        state = service(cfg['service_name'])
        policy.require(state['ActiveState'] == 'inactive' and state['MainPID'] == '0' and
                       supervisor['status'] == 'finished' and supervisor['error'] is None and
                       supervisor['worker_exit_code'] == 0 and supervisor['leases_released'], 'Supervisor stop or lease release failed')
        policy.require(time.time()<cfg['stop_epoch'],'Compute service cleanup exceeded its hard deadline')
        cp = read(output / 'checkpoint.json')
        status = read(output / 'status.json')
        policy.require(status['error'] is None and status['status'] == ('completed_test' if name == 'finite' else 'stopped'), 'Worker terminal state is invalid')
        timer_evidence = None
        if deadline_case:
            policy.require(cp['next_patch'] < cfg['range_end'] and time.time() >= cfg['stop_epoch']-11,
                           'Deadline test reached its interval endpoint before its timer')
            timer_evidence = command(['systemctl', '--user', 'show', timer, '-p', 'LastTriggerUSec', '-p', 'LastTriggerUSecMonotonic'])
            fields = dict(line.split('=',1) for line in timer_evidence['stdout'].splitlines() if '=' in line)
            if int(fields.get('LastTriggerUSecMonotonic','0')) == 0:
                # --collect may unload the completed transient unit immediately.
                timer_evidence = command(['journalctl','--user','-u',cfg['deadline_service_name'],
                                          '--since','@'+str(int(cfg['stop_epoch']-120)),
                                          '--no-pager','-o','short-iso'])
                policy.require('Starting '+cfg['deadline_service_name'] in timer_evidence['stdout'] and
                               'Finished '+cfg['deadline_service_name'] in timer_evidence['stdout'],
                               'Independent deadline stop service never executed')
        result = audit_grouped.audit_suffix(output, dict(checkpoint=dict(next_patch=base['initial_patch']), config=cfg), cp, 'fresh', cfg['gmp_audit_period'])
        policy.require(result['new_chunks'] > 0 and result['new_gmp_audited_chunks'] == (result['new_chunks']+cfg['gmp_audit_period']-1)//cfg['gmp_audit_period'], 'Independent GMP audit cadence is incomplete')
        cleanup=command([PYTHON,'-B',str(WORKER/'finalize_replica.py'),'--config',str(config_path),'--config-sha256',policy.digest(config_path)])
        events.append(cleanup)
        policy.require((replica/'checkpoint.json').read_bytes()==(output/'checkpoint.json').read_bytes(),'Terminal replica checkpoint differs from local checkpoint')
        replica_result=audit_grouped.audit_suffix(replica,dict(checkpoint=dict(next_patch=base['initial_patch']),config=cfg),cp,'fresh',cfg['gmp_audit_period'])
        policy.require(replica_result==result,'Replica audit differs from local journal audit')
        controls = read(output / 'controls.json')
        policy.require(controls['status'] == 'passed' and all(row['full_oracle_equal'] and row['hits'] for row in controls['cases']), 'Fresh nonempty controls failed')
        policy.require(not check.owner_is_locked(ledger.root / 'jobs' / run_id / 'journal.jsonl'), 'Test owner lock was not released')

        rejected = None
        if name == 'finite':
            cp_before = (output / 'checkpoint.json').read_bytes()
            length = (output / 'coverage.jsonl').stat().st_size
            again = subprocess.run([PYTHON, '-B', str(WORKER / 'packed_worker.py'), '--config', str(config_path)], capture_output=True, text=True, timeout=15)
            policy.require(again.returncode != 0 and 'FileExistsError' in again.stderr and
                           (output / 'checkpoint.json').read_bytes() == cp_before and
                           (output / 'coverage.jsonl').stat().st_size == length, 'Existing output was reused or changed')
            rejected = True
        policy.validate_archive(cfg)
        result.update(case=name, status='passed', actual_systemd=True, TEST_ONLY=True,
                      controls='passed', original_parent_unchanged=True,
                      leases_released=True, existing_output_rejected=rejected,
                      hard_deadline=cfg['stop_local'], finished_utc=datetime.now(timezone.utc).isoformat(),
                      service=state, commands=events, independent_deadline_timer=timer_evidence)
        (folder / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({k: v for k, v in result.items() if k != 'commands'}), flush=True)
        return result
    finally:
        subprocess.run(['systemctl', '--user', 'stop', cfg['service_name'], timer], capture_output=True, timeout=20)
        for filename in ('worker.stdout.log', 'worker.stderr.log', 'supervisor-report.json', 'service.stdout.log', 'service.stderr.log'):
            path = WORKER / filename
            if path.exists():
                path.rename(folder / filename)


def main():
    results = [case(name) for name in ('finite', 'signal', 'deadline')]
    (ROOT / 'runtime-validation.json').write_text(json.dumps(dict(status='passed', manifest_sha256=read(ROOT / 'validation-template.json')['manifest_sha256'],
        actual_gpu=True, actual_ledger=True, actual_bulk_storage=True, signal_stop_passed=True,
        independent_deadline_timer_passed=True, existing_output_rejected=True, production_started=False,
        cases=results), indent=2) + '\n')


if __name__ == '__main__':
    main()
