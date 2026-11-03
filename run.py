#!/usr/bin/env python3
"""Budgeted, single-process exact searches with transactional restart records."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import time

from reference import verify

ROOT = Path(__file__).resolve().parent
MAX_BOUND = 35_000_000
SMALL_BOUND = 100_000


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(backend):
    files = [ROOT / 'src/exact.hpp', ROOT / 'src/search_common.hpp',
             ROOT / f'src/search_{backend}.{ "cu" if backend == "gpu" else "cpp"}',
             ROOT / f'bin/search_{backend}', ROOT / 'run.py', ROOT / 'reference.py',
             ROOT / 'Makefile', ROOT / 'tests/test_search.py', ROOT / 'tests/arithmetic.cpp',
             ROOT / 'bin/arithmetic_cpu', ROOT / 'bin/arithmetic_cpu_sanitize',
             ROOT / 'bin/search_cpu_sanitize']
    if backend == 'gpu':
        files += [ROOT / 'compat/bits/mathcalls.h', ROOT / 'bin/cuda_smoke',
                  ROOT / 'configure_cuda.py', ROOT / 'src/cuda_smoke.cu',
                  ROOT / 'src/search_cpu.cpp', ROOT / 'bin/search_cpu']
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def rows(bound, filter_name):
    return 2 * (bound // 11) + 1 if filter_name == 'mod11' else 2 * bound + 1


def x_count(bound, filter_name):
    if filter_name == 'none':
        return 2 * bound + 1
    return sum((bound-r)//11 - (-bound-1-r)//11 for r in (2, 6, 7, 8, 10))


def estimate(bound, chunk_rows=128, filter_name='mod11'):
    m, n = x_count(bound, filter_name), rows(bound, filter_name)
    chunk_rows = min(chunk_rows, n)
    return {'bound': bound, 'filter': filter_name, 'x_count': m, 'z_rows': n,
            'step_upper_bound': m*n,
            'cpu_table_bytes_approx': m*20,
            'gpu_host_table_bytes_approx': m*36 + chunk_rows*20,
            'gpu_device_bytes_approx': m*20 + chunk_rows*28 + 120_008,
            'note': 'Excludes process/CUDA context overhead, vector spare capacity and result/log storage. '
                    'No measured GPU rate is available until GPU validation and benchmarking pass.'}


def atomic_json(path, obj):
    """File and directory fsync + atomic rename: committed prefix is never torn."""
    path = Path(path)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.checkpoint-')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2, sort_keys=True)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
        dfd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(directory):
    with (directory / '.lock').open('a') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('another runner owns this run') from None
        yield


def validate_result(result, config, start, stop):
    for key, value in [('backend', config['backend']), ('bound', config['bound']),
                       ('target', config['target']), ('filter', config['filter']),
                       ('row_start', start), ('row_stop', stop),
                       ('total_rows', rows(config['bound'], config['filter'])),
                       ('x_count', x_count(config['bound'], config['filter']))]:
        if result.get(key) != value:
            raise ValueError(f'engine metadata mismatch: {key}')
    if (type(result.get('steps')) is not int or not 0 <= result['steps'] <=
            (stop-start)*result['x_count']):
        raise ValueError('invalid step count')
    if type(result.get('hits')) is not list:
        raise ValueError('missing candidate list')
    seen = set()
    for hit in result['hits']:
        verify(hit, config['bound'], config['target'])
        a, b, z = hit
        if a > b:
            raise ValueError('candidate violates symmetry ordering')
        if config['filter'] == 'mod11':
            if z % 11 or pow(a, 5, 11) != 10 or pow(b, 5, 11) != 10:
                raise ValueError('candidate violates mod11 role assignment')
            row = z//11 + config['bound']//11
        else:
            row = z + config['bound']
        if not start <= row < stop or tuple(hit) in seen:
            raise ValueError('candidate row/uniqueness check failed')
        seen.add(tuple(hit))


def execute_engine(command, timeout):
    """Kill the whole engine process group if interrupted or over its wall budget."""
    p = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        stdout, stderr = p.communicate(timeout=timeout)
    except BaseException:
        os.killpg(p.pid, signal.SIGKILL)
        p.communicate()
        raise
    if p.returncode:
        raise RuntimeError(f'engine failed ({p.returncode}): {stderr.strip()}')
    return json.loads(stdout)


def gpu_gate():
    """Do not permit a production GPU run based on compilation alone."""
    report = json.loads((ROOT / 'runs/validation.json').read_text())
    if report.get('gpu_status') != 'passed' or report.get('gpu_fingerprint') != fingerprint('gpu'):
        raise ValueError('GPU validation not passed for these files; run make test on a GPU-visible session')
    for command in ([str(ROOT / 'bin/cuda_smoke')], [str(ROOT / 'bin/search_gpu'), '--self-test']):
        subprocess.run(command, cwd=ROOT, check=True, timeout=15, stdout=subprocess.DEVNULL)


def coverage(state):
    """Validate checkpoint continuity and candidate records before trusting resume."""
    config = state['config']
    next_row = 0
    for chunk in state['chunks']:
        if chunk['row_start'] != next_row:
            raise ValueError('checkpoint contains a gap or overlap')
        if not next_row < chunk['row_stop'] <= state['total_rows']:
            raise ValueError('invalid checkpoint row interval')
        validate_result(chunk, config, next_row, chunk['row_stop'])
        next_row = chunk['row_stop']
    if next_row != state['next_row'] or not 0 <= next_row <= state['total_rows']:
        raise ValueError('invalid checkpoint prefix')
    if state['total_rows'] != rows(config['bound'], config['filter']):
        raise ValueError('row space changed')
    return next_row


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='action', required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('--bound', type=int, required=True)
    new = sub.add_parser('new')
    new.add_argument('--bound', type=int, required=True)
    new.add_argument('--backend', choices=['cpu', 'gpu'], default='cpu')
    new.add_argument('--target', type=int, default=42)
    new.add_argument('--filter', choices=['mod11', 'none'], default='mod11')
    new.add_argument('--chunk-rows', type=int, default=128)
    resume = sub.add_parser('resume')
    status = sub.add_parser('status')
    for parser in (new, resume, status):
        parser.add_argument('--run', type=Path, required=True)
    for parser in (new, resume):
        parser.add_argument('--max-seconds', type=float, default=10)
        parser.add_argument('--max-chunks', type=int, default=100000)
        parser.add_argument('--approved-long', action='store_true',
                            help='Use only after explicit approval for the bounds and resources')
    args = ap.parse_args()
    if args.action in ('plan', 'new') and not 0 <= args.bound <= MAX_BOUND:
        raise ValueError(f'bound must be in [0,{MAX_BOUND}]')
    if args.action == 'plan':
        print(json.dumps(estimate(args.bound), indent=2))
        return
    if args.action in ('new', 'resume'):
        if not 0 < args.max_seconds <= 86400 or args.max_chunks < 1:
            raise ValueError('invalid execution budget')
        if args.max_seconds > 30 and not args.approved_long:
            raise ValueError('over 30 seconds requires explicit approval and --approved-long')
    directory = args.run.resolve()
    if args.action == 'new':
        if args.bound > SMALL_BOUND and not args.approved_long:
            raise ValueError('bounds above 100000 require approval; use plan first')
        if not -(1 << 63) <= args.target < (1 << 63):
            raise ValueError('target outside signed 64-bit range')
        if args.filter == 'mod11' and args.target % 11 != 9:
            raise ValueError('mod11 filter requires target == 9 (mod 11)')
        if not 1 <= args.chunk_rows <= 65536:
            raise ValueError('chunk rows must be in [1,65536]')
        if directory.exists():
            raise ValueError('run directory exists; use resume or a new directory')
        if args.backend == 'gpu':
            gpu_gate()
        config = {k: getattr(args, k) for k in ('bound', 'backend', 'target', 'filter', 'chunk_rows')}
        state = {'schema': 1, 'created_utc': now(), 'updated_utc': now(),
                 'hostname': socket.gethostname(), 'config': config,
                 'fingerprint': fingerprint(args.backend), 'next_row': 0,
                 'total_rows': rows(args.bound, args.filter), 'chunks': []}
        directory.mkdir(parents=True)
        atomic_json(directory / 'state.json', state)
    with locked(directory):
        state = json.loads((directory / 'state.json').read_text())
        coverage(state)
        config = state['config']
        if args.action == 'status':
            print(json.dumps({'config': config, 'next_row': state['next_row'],
                              'total_rows': state['total_rows'],
                              'complete': state['next_row'] == state['total_rows'],
                              'verified_candidates': sum(len(c['hits']) for c in state['chunks']),
                              'steps': sum(c['steps'] for c in state['chunks']),
                              'search_seconds': sum(c['search_seconds'] for c in state['chunks'])}, indent=2))
            return
        if config['bound'] > SMALL_BOUND and not args.approved_long:
            raise ValueError('resuming bounds above 100000 requires approval and --approved-long')
        if state['hostname'] != socket.gethostname():
            raise ValueError('resume must use the original machine')
        if state['fingerprint'] != fingerprint(config['backend']):
            raise ValueError('source/runner/binary changed; retain old run and start a new one')
        if args.action == 'resume' and config['backend'] == 'gpu':
            gpu_gate()
        deadline = time.monotonic() + args.max_seconds
        done = 0
        try:
            while state['next_row'] < state['total_rows'] and done < args.max_chunks:
                remaining = deadline - time.monotonic()
                if remaining < 0.05:
                    break
                start = state['next_row']
                stop = min(start+config['chunk_rows'], state['total_rows'])
                command = [str(ROOT / f'bin/search_{config["backend"]}'),
                           '--bound', str(config['bound']), '--target', str(config['target']),
                           '--filter', config['filter'], '--row-start', str(start), '--row-stop', str(stop)]
                begin = time.monotonic()
                try:
                    result = execute_engine(command, timeout=remaining)
                except subprocess.TimeoutExpired:
                    print(f'Budget expired in rows [{start},{stop}); chunk not committed.', file=sys.stderr)
                    break
                validate_result(result, config, start, stop)
                if state['fingerprint'] != fingerprint(config['backend']):
                    raise ValueError('source/runner/binary changed during execution; chunk not committed')
                result.update(completed_utc=now(), wall_seconds=time.monotonic()-begin,
                              candidates_verified_with='Python arbitrary-precision integers')
                state['chunks'].append(result)
                state['next_row'] = stop
                state['updated_utc'] = now()
                atomic_json(directory / 'state.json', state)
                done += 1
        except KeyboardInterrupt:
            print('Interrupted; last committed prefix is intact.', file=sys.stderr)
            state = json.loads((directory / 'state.json').read_text())
        print(json.dumps({'run': str(directory), 'rows_committed': state['next_row'],
                          'total_rows': state['total_rows'],
                          'complete': state['next_row'] == state['total_rows'],
                          'verified_candidates': sum(len(c['hits']) for c in state['chunks'])}))


if __name__ == '__main__':
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
