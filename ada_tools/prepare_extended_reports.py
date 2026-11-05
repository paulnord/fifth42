"""Review and stage the requested ADA CPU/GPU evidence for the handoff branch."""
from pathlib import Path
import csv
import hashlib
import io
import json
import statistics
import sys

ROOT = Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
CHECKOUT = Path('/home/pnord/fifth42-lattice-optimizations-91bb89b')
GPU_ROOT = Path('/home/pnord/fifth-lattice-gpu')
CPU_RUN = ROOT/'scaling-runs/20261105T191425Z-72atoebe'
GPU_RUN = GPU_ROOT/'validation-runs/20261105T191235Z'
CPU_DEST = CHECKOUT/'ada_validation/lattice-scaling-extended-20261105'
GPU_DEST = CHECKOUT/'ada_validation/lattice-cuda-validation-20261105'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

ALIASES = sorted({
    str(ROOT/'venv/bin/python'): '${VALIDATION_PYTHON}',
    str(CPU_RUN): '${RUN_DIR}', str(GPU_RUN): '${GPU_RUN_DIR}',
    str(CHECKOUT): '${EVIDENCE_CHECKOUT}', str(ROOT): '${VALIDATION_WORKSPACE}',
    str(GPU_ROOT): '${GPU_WORKSPACE}',
    '/home/pnord/fifth-lattice-ada-review': '${CPU_BASELINE_WORKSPACE}',
    '/home/pnord/fifth42': '${PRODUCTION_CHECKOUT}',
    '/home/pnord': '${USER_HOME}',
}.items(), key=lambda pair: len(pair[0]), reverse=True)

def redact(s):
    for original, replacement in ALIASES:
        s = s.replace(original, replacement)
    return s

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(redact(content))

def write_json(path, data):
    write(path, json.dumps(data, indent=2)+'\n')

def export_file(source, target):
    write(target, source.read_text())

def checksums(dest):
    entries = sorted(p for p in dest.rglob('*') if p.is_file() and p.name != 'SHA256SUMS')
    write(dest/'SHA256SUMS', ''.join(f'{sha(p)}  {p.relative_to(dest)}\n' for p in entries))

def csv_file(path, rows):
    if not rows:
        return
    s = io.StringIO()
    writer = csv.DictWriter(s, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    write(path, s.getvalue())

def gpu():
    report = json.loads((GPU_RUN/'report.json').read_text())
    device = json.loads((GPU_RUN/'device-results/report.json').read_text())
    if report['status'] != 'passed' or device['status'] != 'passed':
        raise RuntimeError('GPU validation did not pass')
    for name, digest in report['source_sha256'].items():
        if sha(GPU_RUN/'workspace'/name) != digest or sha(GPU_ROOT/name) != digest:
            raise RuntimeError('GPU source identity mismatch: '+name)
    if len(device['full_domain_cases']) != 8 or device['arithmetic_cases'] != 272:
        raise RuntimeError('GPU validation case count mismatch')
    rows = []
    for case in device['full_domain_cases']:
        for backend in case['backends']:
            if backend['points_visited'] != case['coefficient_points']:
                raise RuntimeError('GPU/host coefficient count mismatch')
            rows.append(dict(bound=case['bound'], mode=case['mode'], cap=case['cap'],
                backend=backend['binary'], preparation_seconds=case['cpu_preparation_seconds'],
                **{k:backend[k] for k in ('engine_seconds','kernel_seconds',
                    'engine_process_seconds','host_verification_seconds','end_to_end_seconds')}))
    negative = sum(c['exit_code'] == 2 for c in device['engine_calls'])
    review = dict(status='passed', source_hashes_verified=len(report['source_sha256']),
        host_tests=8, arithmetic_cases=272, full_domain_cases=8,
        coefficient_counts_match_all_backends=True,
        engine_calls=len(device['engine_calls']), expected_negative_exits=negative,
        selected_large_fixture_patches=device['selected_large_fixture_patches'],
        full_shell_large_fixture_coverage=False, repeated_timing_benchmark=False,
        validation_run=str(GPU_RUN))
    write_json(GPU_DEST/'post-run-review.json', review)
    for name in ('report.json','source-sha256.json','host-tests.stdout.txt','host-tests.stderr.txt',
                 'build.stdout.txt','build.stderr.txt','device-correctness.stdout.txt',
                 'device-correctness.stderr.txt','device-results/report.json'):
        export_file(GPU_RUN/name, GPU_DEST/name)
    for name in report['source_sha256']:
        export_file(GPU_RUN/'workspace'/name, GPU_DEST/'executed-source'/name)
    export_file(GPU_RUN/'workspace/CPU_BASELINE.json', GPU_DEST/'CPU_BASELINE.json')
    csv_file(GPU_DEST/'timings.csv', rows)
    table = []
    for case in device['full_domain_cases']:
        if case['bound'] != 1000:
            continue
        cpu = next(b for b in case['backends'] if b['binary']=='emulated')
        cuda = next(b for b in case['backends'] if b['binary']=='cuda')
        table.append(f"| {case['mode']} | {case['cpu_preparation_seconds']:.6f} | "
                     f"{cpu['engine_seconds']:.8f} | {cuda['engine_seconds']:.8f} | "
                     f"{cuda['kernel_seconds']:.9f} | {cpu['end_to_end_seconds']:.6f} | "
                     f"{cuda['end_to_end_seconds']:.6f} |")
    write(GPU_DEST/'README.md', f'''# ADA CUDA lattice validation — 2026-11-05

**PASS:** the user ran `python3 ~/fifth-lattice-gpu/validate.py` in an ADA
terminal with CUDA device access after reboot. The saved run completed in
{report['total_wall_seconds']:.3f} seconds. Eight host tests, the serial build,
and device correctness checks passed. This is bounded correctness evidence;
`speedup_demonstrated` remains false.

The checks covered 272 signed/cross-limb arithmetic pairs on each of CUDA,
ordinary CPU emulation, and sanitized CPU emulation; eight complete positive
domains through bound 1,000; nonempty controls; and two selected large fixture
patches. The large fixture checks do not establish complete shell coverage.
All backend coefficient counts match the certified boxes. There were
{len(device['engine_calls'])} engine invocations, including {negative} expected
nonzero exits for capacity and malformed-input checks.

## Bound-1,000 timing observations

All times are seconds. These are single validation observations, not medians.
CPU here means ordinary coefficient-box emulation, not the optimized direct
CPU solver used in the separate scaling comparison.

| Mode | Shared CPU preparation | CPU engine | CUDA engine | CUDA kernel | CPU total | CUDA total |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(table)}

Total time includes shared preparation, the engine process, and exact host
verification. CUDA engine timing excludes process startup/context overhead;
kernel timing excludes host transfers and other engine work. The CUDA engine
was faster on these two samples, while total time was higher. The roughly
8.5–8.7 second host preparation dominates both backends. All samples, including
the sanitized backend, are in [timings.csv](timings.csv).

## Scope and next experiment

The tested GPU prototype is separate from the fpylll/pruning/GMP CPU experiment.
Its reference is pinned to `ddf28f04725b29b2f1d53b5d33c16379b0f66a20`.
The validator reused the saved CPU reproduction after verifying its freshness
receipt and regenerated output hashes. See [CPU_BASELINE.json](CPU_BASELINE.json).
This review checked all 16 executed source hashes against the saved workspace
and current source, plus report case counts and coefficient counts.

A suggested later timing experiment is complete domains at 2,000, 4,000, and
8,000 with one GPU, one host CPU, a ten-minute overall cap, and five paired
CUDA/emulation repeats where the cap permits. Prepare and certify each packet
once; retain preparation, kernel, process, and end-to-end measurements
separately, and independently verify exact hits and complete point counts.
This needs a separate guarded runner: the validated host planner currently
rejects full domains above 1,000 and limits packets to 4,096 tasks and
50 million coefficient points. Keep finite limits and record any explicit
changes. No larger CUDA run or automatic continuation was started here.

## Artifacts

The validator and device reports, build/test logs, source identities, and all
executed source files are retained here. The GPU model/driver was not captured
in this validator's report. GPU device access is unavailable to the Codex
sandbox; successful execution was performed in the user's ADA terminal.
Absolute local paths are replaced with `${{GPU_WORKSPACE}}`, `${{GPU_RUN_DIR}}`,
`${{CPU_BASELINE_WORKSPACE}}`, and related aliases. Original executed-source
hashes apply to local unredacted bytes; [SHA256SUMS](SHA256SUMS) checks the
published artifact bytes. Substitute actual paths before reusing a source copy.
''')
    checksums(GPU_DEST)
    print('GPU_REPORT '+str(GPU_DEST))

def cpu():
    report = json.loads((CPU_RUN/'report.json').read_text())
    if report['status'] == 'running':
        raise RuntimeError('CPU sweep still running')
    results = report['results']
    checks = []
    sample_rows, median_rows, table = [], [], []
    for case in results['cases']:
        oracle_path = CPU_RUN/case['oracle']['result_file']
        if sha(oracle_path) != case['oracle']['sha256']:
            raise RuntimeError('CPU oracle file hash mismatch')
        oracle = {tuple(h) for h in case['oracle']['hits']}
        normalized = []
        for variant, samples in case['samples'].items():
            for sample in samples:
                path = CPU_RUN/sample['result_file']
                if sha(path) != sample['result_sha256']:
                    raise RuntimeError('CPU trial file hash mismatch')
                trial = json.loads(path.read_text())
                actual = trial['result']
                hits = ({tuple(h) for h in actual['signed_hits']} if variant=='mpq_prune'
                        else {tuple(sorted(h)) for h in actual['hits']})
                if hits != oracle or not trial['oracle_equal']:
                    raise RuntimeError('CPU trial differs from oracle')
                if variant == 'mpq_prune':
                    if not actual['complete'] or actual['stats']['patches'] != case['geometry']['patches']:
                        raise RuntimeError('CPU lattice patch count mismatch')
                    if actual['stats']['enumeration_nodes'] > report['max_nodes']:
                        raise RuntimeError('CPU enumeration budget exceeded')
                    copy = json.loads(json.dumps(actual));copy['stats'].pop('seconds')
                    normalized.append(copy)
                sample_rows.append(dict(bound=case['bound'], completed_step=case['complete'],
                    variant=variant, repeat=sample['repeat'],
                    pipeline_seconds=sample['pipeline_seconds'], cpu_seconds=sample['cpu_seconds'],
                    search_seconds=sample['search_seconds'],
                    process_wall_seconds=sample.get('process_wall_seconds','')))
        if any(x != normalized[0] for x in normalized[1:]):
            raise RuntimeError('CPU lattice outputs/counters differ across repeats')
        if case['complete']:
            for variant, samples in case['samples'].items():
                if len(samples) != 5:
                    raise RuntimeError('Complete CPU step lacks five repeats')
                for key, value in case['medians'][variant].items():
                    if statistics.median(s[key] for s in samples) != value:
                        raise RuntimeError('CPU reported median mismatch')
                median_rows.append(dict(bound=case['bound'],variant=variant,**case['medians'][variant]))
            a,b = case['medians']['mpq_prune'],case['medians']['direct_native128']
            table.append(f"| {case['bound']:,} | {a['pipeline_seconds']:.6f} | "
                         f"{b['pipeline_seconds']:.6f} | {b['process_wall_seconds']:.6f} | "
                         f"{a['pipeline_seconds']/b['pipeline_seconds']:.2f}x |")
        checks.append(dict(bound=case['bound'],complete=case['complete'],phase=case['phase'],
                           sample_counts={k:len(v) for k,v in case['samples'].items()},
                           recorded_trials_match_oracle=True,lattice_counters_consistent=True))
    for key in ('published_package_unchanged','production_sources_unchanged','production_status_unchanged'):
        if not report[key]:
            raise RuntimeError('CPU preservation check failed: '+key)
    if report['elapsed_seconds'] > 600:
        raise RuntimeError('CPU run exceeded its cap')
    for name, expected in report['frozen_code_sha256'].items():
        if sha(CPU_RUN/'code'/name) != expected:
            raise RuntimeError('CPU executed code identity mismatch')
    review = dict(status='passed_for_recorded_completed_trials',run_status=report['status'],
        elapsed_seconds=report['elapsed_seconds'],within_600_second_cap=True,
        cases=checks,all_preservation_checks_pass=True,executed_code_hashes_verified=True)
    write_json(CPU_DEST/'post-run-review.json', review)
    for name in ('report.json','scaling-results.json','events.jsonl','pip-freeze.txt','config.json',
                 'compile-native.stdout.txt','compile-native.stderr.txt',
                 'compile-oracle.stdout.txt','compile-oracle.stderr.txt',
                 'scaling-worker.stdout.txt','scaling-worker.stderr.txt'):
        path = CPU_RUN/name
        if path.exists():export_file(path, CPU_DEST/name)
    for folder in ('oracles','trials','direct-source'):
        for path in (CPU_RUN/folder).iterdir():
            if path.is_file():export_file(path,CPU_DEST/folder/path.name)
    for path in (CPU_RUN/'code').iterdir():
        export_file(path,CPU_DEST/'executed-code'/(path.name+'.txt'))
    csv_file(CPU_DEST/'samples.csv',sample_rows)
    # Variant metric columns differ; use a fixed schema for the CSV export.
    cols = ['bound','variant','pipeline_seconds','cpu_seconds','search_seconds',
            'setup_seconds','process_wall_seconds']
    csv_file(CPU_DEST/'medians.csv',[{key:row.get(key,'') for key in cols} for row in median_rows])
    incomplete = [c for c in results['cases'] if not c['complete']]
    partial = '\n'.join(f"- Bound {c['bound']:,}: phase `{c['phase']}`, "
        f"{len(c['samples']['mpq_prune'])} completed lattice trials and "
        f"{len(c['samples']['direct_native128'])} completed direct trials."
        for c in incomplete) or '- No partially completed steps.'
    started_bounds = {c['bound'] for c in results['cases']}
    not_started = [b for b in report['requested_bounds'] if b not in started_bounds]
    write(CPU_DEST/'README.md',f'''# ADA further CPU doublings — 2026-11-05

The requested continuation started at 64,000 under one new **600-second total
allowance**, one logical CPU, nice 19, one numerical-library thread, and
2 GiB address space per process. Actual elapsed time was
**{report['elapsed_seconds']:.3f} seconds**. Raw coordinator status:
`{report['status']}`; worker status: `{results['status']}`.

## Completed five-pair comparisons

All values are seconds, using five alternating paired repeats per completed
point. Lattice means fpylll plus exact modular pruning and isolated GMP mpq.
Direct means the unchanged native 128-bit production solver, rebuilt in scratch
with its production flags and modulo-11 filter. Medians exclude independent
oracles, geometry checks, imports, and serialization. Direct process wall time
is retained separately from its setup/search clocks.

| Bound | Lattice preparation + search | Direct setup + search | Direct process wall | Warm-time gap |
|---:|---:|---:|---:|---:|
{chr(10).join(table)}

Each recorded completed trial matched an independent full signed-box exact
oracle, modulo permutations. No crossover is inferred beyond measured points.
All samples are in [samples.csv](samples.csv); only steps with five complete
pairs appear in [medians.csv](medians.csv).

## Stopped or unstarted work

{partial}

Configured bounds not started: {', '.join(f'{b:,}' for b in not_started) or 'none'}.
Partial points have no five-pair median and are not reported as completed
benchmark levels. The final guard/error is recorded verbatim in
[report.json](report.json) and [scaling-results.json](scaling-results.json).
No deadline was renewed, no automatic continuation was installed, and no
production search was started.

## Exact verification and changed harness limits

The previous unfiltered GMP oracle took 78 seconds at 32,000; repeating it
at each larger point would consume the timing allowance. This continuation
uses a separately written, unfiltered signed `__int128` oracle instead.
For every largest coordinate z in [-B,B], it searches x <= y <= z with exact
two-pointer sums. Sorting removes permutations only; every signed solution has
exactly one sorted representative. Powers are formed by five integer
multiplications, with no lattice code, shared production headers, or modular
filters. At the oracle's hard bound of 1,000,000,
3*B^5 + 2^63 < 2^127, so signed 128-bit intermediates cannot overflow.

The independent oracle passed 44 Python dictionary-oracle cases including
zero/negative targets and repeated coordinates. It also matched all five
hash-verified archived unfiltered GMP oracles at 2,000 through 32,000.
Nonempty positive controls 12/384 and 2951 passed with Fraction and GMP lattice
arithmetic and both CPU programs. All patches' exact bases, certified transforms,
and Gram–Schmidt values were compared between Fraction and GMP before each
timed level. Post-run review verified every recorded trial hash, exact result
set, repeated lattice counters, completed-point median, and executed code hash.

Larger boxes explicitly use finite limits of **500 million enumeration nodes**
and **150,000 patches** per lattice call. The per-call time guard remains
120 seconds and all work, including compilation and oracles, shares the
600-second coordinator watchdog. Limits fail closed. No library defaults,
production sources, or original evidence were edited. Production job locks,
the GPU validator lock, CPU load, and memory were monitored throughout.

The lattice package remains pinned to
`91bb89b0ff49974e9458faf19015908e44b85cb8`; production native source is
`853fd98fc91968987fcb3e9e4c43b4fe880c8246`. The package hashes, production CPU
sources, and production working-tree status were preserved. This experiment
uses the same Python/package pins as the preceding scaling report, recorded
in [pip-freeze.txt](pip-freeze.txt). These domains are within previously
completed production coverage; they add timing evidence only.

## Artifacts

Raw results, successful trial files, exact oracles, commands, guard outcomes,
and original code hashes are retained. Executed code is included as text
transcripts under [executed-code](executed-code/). Absolute local paths are
replaced by `${{RUN_DIR}}`, `${{VALIDATION_WORKSPACE}}`, `${{VALIDATION_PYTHON}}`,
`${{EVIDENCE_CHECKOUT}}`, `${{PRODUCTION_CHECKOUT}}`, and `${{USER_HOME}}` aliases.
Original hashes refer to unredacted local bytes; [SHA256SUMS](SHA256SUMS) checks
the published bytes. Substitute actual paths before reusing a code transcript.
''')
    checksums(CPU_DEST)
    print('CPU_REPORT '+str(CPU_DEST))

def payload():
    entries=[]
    for dest in (CPU_DEST,GPU_DEST):
        for path in sorted(dest.rglob('*')):
            if path.is_file():
                entries.append(dict(path=str(path.relative_to(CHECKOUT)),mode='100644',
                                    type='blob',content=path.read_text()))
    path=ROOT/'github-extended-publication.json'
    path.write_text(json.dumps(dict(repository_full_name='paulnord/fifth42',
        base_tree_sha='d88cac5d8e38d67678f93c2dbea74c1fa64ac178',tree_elements=entries)))
    print('PUBLICATION_PAYLOAD',path,'FILES',len(entries))

if __name__=='__main__':
    for action in sys.argv[1:] or ['gpu','cpu','payload']:
        {'gpu':gpu,'cpu':cpu,'payload':payload}[action]()
