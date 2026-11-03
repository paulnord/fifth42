#!/usr/bin/env python3
"""Run only the approved GPU calibrations, then estimate an hour-sized box.

The user approved B=10^6 (10 s budget), followed by B=10^7 (300 s budget)
when calibration supports it. This helper does not launch an hour-long job,
change the arithmetic limit, resume an interrupted job, or modify validation.
Run it in the normal GPU-visible Ada terminal.
"""
import argparse
import json
import math
from pathlib import Path
import socket
import subprocess
import sys
import time

import run

ROOT = Path(__file__).resolve().parent
STAGES = ((1_000_000, 10), (10_000_000, 300))
CHUNK_ROWS = 65_536
FUTURE_SAFE_BOUND = 35_000_000


def summary(state):
    run.coverage(state)
    return {
        'bound': state['config']['bound'],
        'rows_committed': state['next_row'], 'total_rows': state['total_rows'],
        'complete': state['next_row'] == state['total_rows'],
        'steps': sum(c['steps'] for c in state['chunks']),
        'search_seconds': sum(c['search_seconds'] for c in state['chunks']),
        'chunk_wall_seconds': sum(c['wall_seconds'] for c in state['chunks']),
        'setup_seconds': sum(c['setup_seconds'] for c in state['chunks']),
        'verified_candidates': sum(len(c['hits']) for c in state['chunks']),
    }


def projections(base):
    """Conditional projections, never coverage claims or execution authority."""
    measured_steps = base['steps']
    if not base['complete'] or measured_steps <= 0:
        return []
    search_s = base['search_seconds']
    wall_s = base['chunk_wall_seconds']
    estimates = []
    for bound in (10_000_000, 20_000_000, 30_000_000, 35_000_000):
        e = run.estimate(bound, CHUNK_ROWS)
        ratio = e['step_upper_bound'] / measured_steps
        estimates.append({
            'bound': bound,
            'projected_search_seconds': search_s * ratio,
            'projected_engine_wall_seconds': wall_s * ratio,
            'gpu_buffer_MB': e['gpu_device_bytes_approx'] / 1e6,
            'host_table_MB': e['gpu_host_table_bytes_approx'] / 1e6,
            'requires_raising_and_retesting_guard': bound > run.MAX_BOUND,
            'uncertainty': 'Quadratic extrapolation from the completed ten-million run. '
                           'Larger tables can change cache and memory behavior; context overhead is additional.',
        })
    return estimates


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan-only', action='store_true', help='Show the approved stages; run nothing')
    args = ap.parse_args()
    if args.plan_only:
        print(json.dumps({'stages': [{'bound': b, 'search_budget_seconds': t} for b,t in STAGES],
                          'hour_job_will_be_launched': False,
                          'future_safe_bound_after_guard_change_and_tests': FUTURE_SAFE_BOUND}, indent=2))
        return
    if socket.gethostname() != 'ada':
        raise ValueError('This calibration is authorized only on ada')
    validation = json.loads((ROOT / 'runs/validation.json').read_text())
    if validation.get('gpu_status') != 'passed' or validation.get('gpu_fingerprint') != run.fingerprint('gpu'):
        raise ValueError('Current GPU validation is not passed; run make test-gpu in the normal Ada terminal')
    report = {'created_utc': run.now(), 'hostname': socket.gethostname(),
              'approval': 'User: "Oh yes. Let\'s make it bigger." Approved the previously proposed calibration stages.',
              'hour_job_started': False, 'stages': [], 'projections': []}
    output = ROOT / 'runs/gpu-calibration.json'
    for bound, budget in STAGES:
        directory = ROOT / f'runs/gpu-B{bound}'
        newly_run = False
        if not directory.exists():
            if bound == 10_000_000:
                previous = report['stages'][-1]
                scale = run.estimate(bound,CHUNK_ROWS)['step_upper_bound'] / previous['steps']
                estimate = previous['chunk_wall_seconds'] * scale
                report['ten_million_projected_engine_wall_seconds_from_first_stage'] = estimate
                if estimate > budget:
                    report['stopped_reason'] = 'Million-bound calibration projects more than 300 s for ten million; revise the budget before launching it.'
                    run.atomic_json(output, report)
                    print(json.dumps(report, indent=2))
                    return
            command = [sys.executable, str(ROOT / 'run.py'), 'new', '--backend', 'gpu',
                       '--bound', str(bound), '--chunk-rows', str(CHUNK_ROWS),
                       '--max-seconds', str(budget), '--approved-long', '--run', str(directory)]
            print(f'Approved calibration: B={bound:,}, budget={budget}s, one GPU.', flush=True)
            begin = time.monotonic()
            completed = subprocess.run(command, cwd=ROOT)
            invocation_wall_seconds = time.monotonic() - begin
            if completed.returncode:
                report['stopped_reason'] = f'Calibration command failed with exit {completed.returncode}; no automatic retry.'
                run.atomic_json(output,report)
                raise RuntimeError(report['stopped_reason'])
            newly_run = True
        state = json.loads((directory / 'state.json').read_text())
        if (state['fingerprint'] != run.fingerprint('gpu') or
                state['hostname'] != 'ada' or state['config']['bound'] != bound or
                state['config']['backend'] != 'gpu' or state['config']['target'] != 42 or
                state['config']['filter'] != 'mod11'):
            raise ValueError(f'Existing run has different configuration/fingerprints: {directory}')
        s = summary(state)
        s['checkpoint'] = str(directory / 'state.json')
        if newly_run:
            s['invocation_wall_seconds_including_preflight'] = invocation_wall_seconds
        report['stages'].append(s)
        run.atomic_json(output,report)
        if not s['complete']:
            report['stopped_reason'] = 'Stage has partial coverage; retained its checkpoint and did not resume or launch the next stage.'
            run.atomic_json(output,report)
            print(json.dumps(report,indent=2))
            return
    base = report['stages'][-1]
    report['projections'] = projections(base)
    # Leave 10% of an hour for overhead/variance, then round down to a million.
    if base['chunk_wall_seconds'] > 0:
        raw = base['bound'] * math.sqrt(3240 / base['chunk_wall_seconds'])
        recommended = min(FUTURE_SAFE_BOUND, int(raw // 1_000_000) * 1_000_000)
        report['conditional_hour_bound_with_10_percent_reserve'] = recommended
    report['next_step'] = ('Review the measured calibration and choose bounds/resources before approving an hour job. '
                           'Bounds above ten million need a tested guard change; do not bypass it.')
    run.atomic_json(output,report)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as e:
        print(f'ERROR: {e}',file=sys.stderr)
        sys.exit(1)
