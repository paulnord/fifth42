#!/usr/bin/env python3
"""Run only the handoff's bounded checks and save fresh, isolated evidence."""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import resource
import signal
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/home/pnord/fifth42-lattice-optimizations-91bb89b/lattice_prototype')
PYTHON = str(ROOT / 'venv/bin/python')
FIFTH = Path('/home/pnord/fifth42')
RUNS = ROOT / 'validation-runs'
RUNS.mkdir(exist_ok=True)
OUTPUT = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'), dir=RUNS))
SCRATCH = OUTPUT / 'scratch/lattice_prototype'
REPORT = OUTPUT / 'report.json'
LOGS = OUTPUT / 'logs'
LOGS.mkdir(exist_ok=True)
LOCK_PATHS = []
for base in [FIFTH / 'runs', FIFTH / 'extended/runs', FIFTH / 'optimization/runs',
             Path('/home/pnord/four133-eight-hour/jobs')]:
    if base.exists():
        LOCK_PATHS.extend(p for p in base.rglob('*')
                          if p.is_file() and 'lock' in p.name.lower())
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           PYTHONDONTWRITEBYTECODE='1')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def evidence():
    return {str(p.relative_to(SOURCE)): digest(p)
            for p in SOURCE.rglob('*') if p.is_file()}

def blockers():
    problems = []
    latest = Path('/home/pnord/four133-eight-hour/jobs/latest.json')
    if latest.is_file():
        job = Path(json.loads(latest.read_text())['job'])
        state = json.loads((job / 'progress.json').read_text())
        if state.get('status') in ('starting', 'running') or state.get('active_workers'):
            problems.append('four133 active')
    for p in FIFTH.glob('*/runs/*/job.json'):
        state = json.loads(p.read_text())
        if state.get('status') in ('starting', 'running', 'validating', 'searching',
                                   'calibrating', 'stopping'):
            problems.append('active production job: ' + str(p))
    for p in LOCK_PATHS:
        if not p.is_file():
            continue
        try:
            with p.open('rb') as stream:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(stream, fcntl.LOCK_UN)
        except BlockingIOError:
            problems.append('busy production lock: ' + str(p))
    return problems

def limits():
    os.nice(19)
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))

def normalized(value):
    if isinstance(value, dict):
        return {k: normalized(v) for k, v in value.items() if 'seconds' not in k}
    if isinstance(value, list):
        return [normalized(v) for v in value]
    return value

report = dict(
    status='running', source_commit='91bb89b0ff49974e9458faf19015908e44b85cb8',
    source=str(SOURCE), scratch=str(SCRATCH), started_utc=datetime.now(timezone.utc).isoformat(),
    host=platform.node(), platform=platform.platform(),
    execution='Sequential, one CPU, nice 19, native thread counts 1, 2 GiB per process',
    bounds='signed smoke 100; positive controls 34; upstream comparison 100 and 1000',
    fresh_bound_1000_lattice_search=False, gpu_execution=False, larger_search_started=False,
    commands=[], deferred=[],
)
before = json.loads((ROOT / 'published-sha256.json').read_text())
if evidence() != before:
    raise RuntimeError('Published evidence mismatch before tests')

modular = '''import json
import lattice5 as l
import modular_filters as f
rows = []
for mode in ('none', 'prune'):
    r = f.signed42_filtered(100, mode=mode, backend=BACKEND, max_seconds=20)
    if not r['complete'] or set(map(tuple, r['signed_hits'])) != l.signed_reference(100, 42):
        raise RuntimeError('signed bound-100 check failed')
    rows.append(r)
r = f.search_targets_positive(34, [12, 384], mode='prune', backend=BACKEND, max_seconds=20)
expected = l.direct_positive(1, 34, lambda c: 384, lambda r, c: r in (12, 384))
if not r['complete'] or not expected or set(map(tuple, r['hits'])) != expected:
    raise RuntimeError('nonempty control failed')
rows.append(r)
print(json.dumps(rows, indent=2))
'''
oracle = '''import json
import lattice5 as l
for name in ('smoke-reference', 'smoke-fpylll'):
    p = ROOT / 'logs' / (name + '.stdout.txt')
    if not p.is_file(): continue
    r = json.loads(p.read_text())
    if not r['complete'] or set(map(tuple,r['signed_hits'])) != l.signed_reference(100,42):
        raise RuntimeError('signed smoke mismatch: '+name)
print('PASS: available signed smoke results agree with independent exact oracle')
'''
probe_code = '''import importlib.metadata as m, importlib.util, json, sys
names = ['sympy','fpylll','cysignals','numpy','gmpy2','mpmath']
versions = {}
for name in names:
    try: versions[name] = m.version(name)
    except m.PackageNotFoundError: versions[name] = None
result = {'python':sys.version, 'python_minor':list(sys.version_info[:2]), 'packages':versions}
if versions['fpylll']:
    import fpylll
    result['fplll_version'] = fpylll.config.version
if versions['gmpy2']:
    import gmpy2
    result['gmp_version'] = gmpy2.mp_version()
    result['mpfr_version'] = gmpy2.mpfr_version()
    result['mpc_version'] = gmpy2.mpc_version()
print(json.dumps(result))
'''
probe = subprocess.run(['timeout','-k','5s','30s',PYTHON,'-c',probe_code],
    capture_output=True,text=True,env=ENV,preexec_fn=limits)
if probe.returncode:
    report.update(status='dependency_import_failed', probe_exit_code=probe.returncode,
                  probe_stderr=probe.stderr, published_files_unchanged=evidence()==before)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('Dependency import failed; see '+str(REPORT),flush=True)
    sys.exit(3)
available = json.loads(probe.stdout)
(OUTPUT/'environment-probe.json').write_text(probe.stdout)
pins = {'sympy': '1.14.0', 'fpylll': '0.6.4', 'cysignals': '1.12.5',
        'numpy': '2.3.5', 'gmpy2': '2.2.2'}
missing = {k: dict(required=v, actual=available['packages'].get(k))
           for k, v in pins.items() if available['packages'].get(k) != v}
report['environment'] = available
report['dependency_mismatches'] = missing
if available['python_minor'] != [3,12]:
    missing['python'] = dict(required='3.12',actual=available['python_minor'])
if '--require-complete' in sys.argv and missing:
    report.update(status='dependencies_missing', published_files_unchanged=evidence()==before)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('Missing pinned dependencies; no tests started. REPORT '+str(REPORT),flush=True)
    sys.exit(3)
if os.environ.get('LATTICE_DEPENDENCIES_CHECK_ONLY') == '1':
    report.update(status='dependencies_ready' if not missing else 'dependencies_missing',
                  published_files_unchanged=evidence()==before)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('Dependency check only; no tests started. REPORT '+str(REPORT),flush=True)
    sys.exit(0 if not missing else 3)
busy = blockers()
if busy:
    report.update(status='resources_busy', blockers=busy, published_files_unchanged=evidence()==before)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('Resources busy; no tests started. REPORT '+str(REPORT),flush=True)
    sys.exit(3)
SCRATCH.parent.mkdir(parents=True)
shutil.copytree(SOURCE,SCRATCH)
(SCRATCH/'results/upstream-comparison.json').unlink()
freeze = subprocess.run([PYTHON,'-m','pip','freeze'],capture_output=True,text=True,check=True)
(OUTPUT/'pip-freeze.txt').write_text(freeze.stdout)
has_fpylll = all(k not in missing for k in ['fpylll', 'cysignals', 'numpy'])
has_gmpy2 = 'gmpy2' not in missing
commands = [
    ('smoke-reference', 60, [PYTHON, 'lattice5.py', '--bound', '100', '--mode',
                            'signed42', '--backend', 'reference', '--max-seconds', '30']),
]
if 'sympy' not in missing:
    commands.append(('smoke-sympy', 60, [PYTHON, 'lattice5.py', '--bound', '100',
        '--mode', 'signed42', '--backend', 'sympy', '--max-seconds', '30']))
if has_fpylll:
    commands.append(('smoke-fpylll', 60, [PYTHON, 'lattice5.py', '--bound', '100',
        '--mode', 'signed42', '--backend', 'fpylll', '--max-seconds', '30']))
    commands.append(('smoke-modular-fpylll', 60,
        [PYTHON, '-c', modular.replace('BACKEND', repr('fpylll'))]))
else:
    report['deferred'].extend(['smoke-fpylll', 'smoke-modular-fpylll'])
commands.extend([
    ('smoke-oracle', 60, [PYTHON, '-c', 'from pathlib import Path\nROOT=Path('+repr(str(OUTPUT))+')\n'+oracle.replace("('smoke-reference', 'smoke-fpylll')", "('smoke-reference', 'smoke-fpylll', 'smoke-sympy')")]),
    ('smoke-modular-reference', 60,
        [PYTHON, '-c', modular.replace('BACKEND', repr('reference'))]),
    ('tests', 300, [PYTHON, '-m', 'unittest', '-v', 'test_lattice5', 'audit_tests',
                    'test_backends', 'test_modular_filters']),
    ('tests-optimized', 300, [PYTHON, '-O', '-m', 'unittest', '-v', 'test_backends',
                              'test_modular_filters']),
])
if has_gmpy2 and has_fpylll:
    commands.extend([
        ('compiled-tests', 300, [PYTHON, 'compiled_experiment/test_mpq.py']),
        ('compiled-tests-optimized', 300, [PYTHON, '-O', 'compiled_experiment/test_mpq.py']),
    ])
else:
    report['deferred'].extend(['compiled-tests', 'compiled-tests-optimized'])
commands.append(('upstream-comparison', 300, [PYTHON, 'compare_upstream.py']))
start = time.monotonic()
process = None
try:
    for name, cap, command in commands:
        busy = blockers()
        if busy:
            raise RuntimeError('Yielding to existing production work: '+', '.join(busy))
        outpath = LOGS / (name + '.stdout.txt')
        errpath = LOGS / (name + '.stderr.txt')
        usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
        t = time.monotonic()
        exact_command = ['timeout', '-k', '5s', str(cap)+'s', *command]
        print('START '+name, flush=True)
        with outpath.open('x') as out, errpath.open('x') as err:
            process = subprocess.Popen(exact_command, cwd=SCRATCH, env=ENV,
                stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
            while process.poll() is None:
                if time.monotonic()-t > cap+7:
                    raise TimeoutError('Outer process deadline: '+name)
                busy = blockers()
                if busy:
                    raise RuntimeError('Production resumed: '+', '.join(busy))
                time.sleep(0.25)
        usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)
        record = dict(name=name, command=exact_command, exit_code=process.returncode,
            wall_seconds=time.monotonic()-t,
            cpu_seconds=usage_after.ru_utime+usage_after.ru_stime-usage_before.ru_utime-usage_before.ru_stime,
            stdout=str(outpath), stderr=str(errpath))
        process = None
        log = errpath.read_text()
        match = re.search(r'Ran (\d+) tests? in ([\d.]+)s', log)
        if match:
            record['tests_run'] = int(match[1])
            record['suite_reported_seconds'] = float(match[2])
            for key in ['failures', 'errors', 'skipped']:
                count = re.search(r'\b'+key+r'=(\d+)', log)
                record[key] = int(count[1]) if count else 0
            record['passed'] = record['tests_run']-record['failures']-record['errors']-record['skipped']
        if record['exit_code']==0 and name.startswith('smoke-') and name!='smoke-oracle':
            data = json.loads(outpath.read_text())
            record['results'] = data
            if name in ['smoke-reference','smoke-fpylll','smoke-modular-fpylll']:
                archived_name={'smoke-reference':'smoke-reference.json',
                    'smoke-fpylll':'smoke-fpylll.json','smoke-modular-fpylll':'smoke-modular.json'}[name]
                archived=json.loads((SOURCE/'publication_validation'/archived_name).read_text())
                record['archived_semantic_equal_excluding_seconds'] = normalized(data)==normalized(archived)
        if name=='upstream-comparison' and record['exit_code']==0:
            fresh = SCRATCH/'results/upstream-comparison.json'
            if not fresh.is_file() or fresh.is_symlink():
                raise RuntimeError('Fresh comparator output missing')
            data=json.loads(fresh.read_text())
            record['comparison_cases']=len(data)
            record['upstream_runs']=sum(len(row['runs']) for row in data)
            record['fresh_output_sha256']=digest(fresh)
            for rel in ['results/upstream-comparison.json','publication_validation/upstream-comparison.json']:
                archived=json.loads((SOURCE/rel).read_text())
                record.setdefault('archived_comparisons',{})[rel]=normalized(data)==normalized(archived)
            record['lattice_bound_1000_inputs']='retained published healy-1000.json and signed42-1000.json; not regenerated'
        report['commands'].append(record)
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
        print('FINISH '+json.dumps({k:record[k] for k in ['name','exit_code','wall_seconds','cpu_seconds','tests_run','passed','errors','skipped'] if k in record}),flush=True)
    expected_counts={'tests':31,'tests-optimized':14,'compiled-tests':5,'compiled-tests-optimized':5}
    suites={r['name']:r for r in report['commands'] if r['name'] in expected_counts}
    suites_ok=all(name in suites and suites[name].get('passed')==count
                  and not any(suites[name].get(k,0) for k in ['errors','failures','skipped'])
                  for name,count in expected_counts.items())
    comparisons_ok=all(r.get('archived_semantic_equal_excluding_seconds',True)
                       and all(r.get('archived_comparisons',{}).values())
                       for r in report['commands'])
    report['status']='passed' if not missing and not report['deferred'] and suites_ok and comparisons_ok and all(r['exit_code']==0 for r in report['commands']) else 'incomplete_validation'
except BaseException as exc:
    report['status']='stopped_or_failed'
    report['error']=type(exc).__name__+': '+str(exc)
finally:
    if process is not None and process.poll() is None:
        os.killpg(process.pid,signal.SIGTERM)
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL)
            process.wait()
    report['published_files_unchanged']=evidence()==before
    report['total_wall_seconds']=time.monotonic()-start
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('REPORT '+str(REPORT)+' STATUS '+report['status'],flush=True)
sys.exit(0 if report['status']=='passed' else 1)
