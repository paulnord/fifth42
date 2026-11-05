"""Review the extended CPU trial and stage its report plus the terminal GPU runner."""
import csv
import hashlib
import io
import json
from pathlib import Path
import statistics
import sys

ROOT=Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
REPO=Path('/home/pnord/fifth42-lattice-optimizations-91bb89b')
GPU=Path('/home/pnord/fifth-lattice-gpu')
RUN=ROOT/'scaling-runs/20261105T192957Z-cp6kee4w'
CPU_DEST=REPO/'ada_validation/lattice-scaling-128000-20261105'
GPU_DEST=REPO/'ada_validation/lattice-cuda-benchmark-20261105'
BASE_TREE='8b9827f294bb7ec1cf43c001e32729cbe5d1eb8f'
ALIASES=sorted({str(RUN):'${RUN_DIR}',str(ROOT/'venv/bin/python'):'${VALIDATION_PYTHON}',
    str(ROOT):'${CPU_BENCHMARK_WORKSPACE}',str(REPO):'${EVIDENCE_CHECKOUT}',
    str(GPU):'${GPU_WORKSPACE}','/home/pnord/fifth42':'${PRODUCTION_CHECKOUT}',
    '/home/pnord':'${USER_HOME}'}.items(),key=lambda pair:len(pair[0]),reverse=True)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path,content):
    for original,replacement in ALIASES:content=content.replace(original,replacement)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content)

def js(path,value):write(path,json.dumps(value,indent=2)+'\n')

def export(source,destination):write(destination,source.read_text())

def sums(folder):
    paths=sorted(p for p in folder.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    write(folder/'SHA256SUMS',''.join(f'{sha(p)}  {p.relative_to(folder)}\n' for p in paths))

def csv_write(path,rows):
    if not rows:return
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows);write(path,stream.getvalue())

def gpu():
    preparation=json.loads((GPU/'benchmark-preparation.json').read_text())
    for name,digest in preparation['source_sha256'].items():
        if sha(GPU/name)!=digest:raise RuntimeError('Prepared GPU runner changed: '+name)
    js(GPU_DEST/'preparation.json',preparation)
    export(GPU/'oracle-host-check-j_nobenc/report.json',GPU_DEST/'independent-oracle-host-checks.json')
    for name in ('benchmark.py','near_oracle.cpp','tests/test_benchmark.py'):
        export(GPU/name,GPU_DEST/'source-transcripts'/(name+'.txt'))
    export(GPU/'BENCHMARK.md',GPU_DEST/'TERMINAL_INSTRUCTIONS.md')
    write(GPU_DEST/'README.md','''# Larger CUDA benchmark runner — 2026-11-05

The separate larger timing runner is ready in the existing ADA GPU workspace:

```bash
python3 ~/fifth-lattice-gpu/benchmark.py --wait
```

Run this in a normal ADA terminal with GPU access. It waits up to 30 minutes
for the CPU benchmark and production locks before starting its own ten-minute
allowance. It compares CUDA with ordinary CPU emulation at 2,000, 4,000, and
8,000, with five alternating paired repeats at each completed level. Packets
are prepared once per domain; preparation, kernel, engine process, exact host
verification, cached-packet, and end-to-end times are recorded separately.

The new runner passed 11 host tests, including expanded-domain interval
coverage, unchanged original bound guards, certificate/count rejection, and
safe waiting on the CPU lock. Its independent exact positive-domain oracle
matched seven Python brute-force cases, including nonempty controls, and
rejected out-of-profile arguments. All 16 original validated GPU source files
remain unchanged. The prior successful CUDA validation remains the prerequisite.
This publication contains preparation evidence and makes no new CUDA timing claim.

The isolated benchmark planner permits bound 8,000; the validated default
planner retains its 1,000 ceiling. The 4,096-task, 50-million packet point,
10-million patch point, integer-overflow, certificate, output, and complete
coverage guards remain in force. An independent unfiltered native 128-bit
oracle must match every full positive-domain result. Nonempty controls run
before the larger comparisons. CUDA processes share an additional cumulative
120-second wall allowance inside the overall ten-minute benchmark cap.

See [TERMINAL_INSTRUCTIONS.md](TERMINAL_INSTRUCTIONS.md) for the domain, metric
definitions, resource limits, output paths, and stopping behavior. Results go
under `~/fifth-lattice-gpu/benchmark-runs/`. The comparison uses the earlier
coefficient-box CUDA prototype; it does not compare CUDA against the optimized
direct CPU solver or against the newer fpylll/GMP lattice implementation.

The sources under [source-transcripts](source-transcripts/) are review copies
of files installed in the ADA GPU workspace. Absolute local paths are
replaced by `${GPU_WORKSPACE}`, `${CPU_BENCHMARK_WORKSPACE}`, and related
aliases. Substitute actual paths and restore ordinary filenames before
installing a transcript elsewhere. Preparation hashes describe original local
bytes; [SHA256SUMS](SHA256SUMS) checks the published artifact bytes.
''')
    sums(GPU_DEST);print('GPU_RUNNER_REPORT',GPU_DEST)

def cpu():
    report=json.loads((RUN/'report.json').read_text())
    if report['status']=='running':raise RuntimeError('CPU comparison still running')
    result=report['results']
    if report['status']!='passed' or result['status']!='passed':
        raise RuntimeError('CPU comparison did not finish all requested pairs')
    if report['hard_wall_cap_seconds']!=1200 or report['per_lattice_call_guard_seconds']!=300:
        raise RuntimeError('Unexpected CPU limits')
    if report['elapsed_seconds']>1200:raise RuntimeError('CPU overall allowance exceeded')
    if report['completed_bounds']!=[128000]:raise RuntimeError('Unexpected completed bounds')
    case=result['cases'][0]
    oracle=RUN/case['oracle']['result_file']
    if sha(oracle)!=case['oracle']['sha256']:raise RuntimeError('Oracle hash mismatch')
    expected={tuple(h) for h in case['oracle']['hits']}
    rows=[];normalized=[]
    for variant,samples in case['samples'].items():
        if len(samples)!=5:raise RuntimeError('Five paired repeats are required')
        for sample in samples:
            p=RUN/sample['result_file']
            if sha(p)!=sample['result_sha256']:raise RuntimeError('Trial hash mismatch')
            trial=json.loads(p.read_text());actual=trial['result']
            hits=({tuple(h) for h in actual['signed_hits']} if variant=='mpq_prune'
                  else {tuple(sorted(h)) for h in actual['hits']})
            if hits!=expected or not trial['oracle_equal']:raise RuntimeError('Trial/oracle mismatch')
            if variant=='mpq_prune':
                if not actual['complete'] or actual['stats']['patches']!=case['geometry']['patches']:
                    raise RuntimeError('Lattice coverage mismatch')
                if actual['stats']['enumeration_nodes']>report['max_nodes']:
                    raise RuntimeError('Lattice node budget exceeded')
                d=json.loads(json.dumps(actual));d['stats'].pop('seconds');normalized.append(d)
            else:
                if not (actual['row_start']==0 and actual['row_stop']==actual['total_rows']):
                    raise RuntimeError('Direct CPU row coverage mismatch')
            rows.append(dict(bound=128000,variant=variant,repeat=sample['repeat'],
                pipeline_seconds=sample['pipeline_seconds'],search_seconds=sample['search_seconds'],
                cpu_seconds=sample['cpu_seconds'],process_wall_seconds=sample.get('process_wall_seconds','')))
        for key,value in case['medians'][variant].items():
            if statistics.median(s[key] for s in samples)!=value:raise RuntimeError('Median mismatch')
    if any(d!=normalized[0] for d in normalized[1:]):raise RuntimeError('Repeated lattice counters differ')
    previous=json.loads((ROOT/'scaling-runs/20261105T191425Z-72atoebe/scaling-results.json').read_text())
    prior=next(c for c in previous['cases'] if c['bound']==128000)
    if prior['geometry']['sha256']!=case['geometry']['sha256']:
        raise RuntimeError('Extended-limit geometry differs from the previous attempt')
    for name,digest in report['frozen_code_sha256'].items():
        if sha(RUN/'code'/name)!=digest:raise RuntimeError('Executed source hash mismatch')
    for key in ('published_package_unchanged','production_sources_unchanged','production_status_unchanged'):
        if report.get(key) is not True:raise RuntimeError('Preservation check failed: '+key)
    review=dict(status='passed',exact_checked_timed_trials=10,paired_repeats=5,
        medians_recomputed=True,repeated_outputs_and_counters_equal=True,
        geometry_matches_previous_128000_attempt=True,
        executed_source_hashes_verified=True,all_preservation_checks_pass=True,
        within_1200_second_allowance=True)
    js(CPU_DEST/'post-run-review.json',review)
    for name in ('report.json','scaling-results.json','events.jsonl','pip-freeze.txt','config.json',
        'compile-native.stdout.txt','compile-native.stderr.txt','compile-oracle.stdout.txt',
        'compile-oracle.stderr.txt','scaling-worker.stdout.txt','scaling-worker.stderr.txt'):
        if (RUN/name).exists():export(RUN/name,CPU_DEST/name)
    for folder in ('trials','oracles','direct-source'):
        for p in (RUN/folder).iterdir():
            if p.is_file():export(p,CPU_DEST/folder/p.name)
    for p in (RUN/'code').iterdir():export(p,CPU_DEST/'executed-code'/(p.name+'.txt'))
    csv_write(CPU_DEST/'samples.csv',rows)
    a,b=case['medians']['mpq_prune'],case['medians']['direct_native128']
    csv_write(CPU_DEST/'medians.csv',[dict(variant=v,**{k:m.get(k,'') for k in
        ('pipeline_seconds','search_seconds','cpu_seconds','setup_seconds','process_wall_seconds')})
        for v,m in case['medians'].items()])
    write(CPU_DEST/'README.md',f'''# ADA CPU comparison at bound 128,000 — 2026-11-05

**PASS:** five alternating paired repeats completed. Every lattice and direct
CPU result matched the independent complete signed-box oracle for
`x^5+y^5+z^5=42`, modulo permutations. The reported signed solution set is
{json.dumps(case['oracle']['hits'])}.

The user's requested limit extension raised the lattice trial allowance from
120 seconds to **300 seconds**, and the overall run allowance from 600 seconds
to **1,200 seconds**, so the five pairs could finish. This run requested only
128,000; it did not redo the completed 64,000 step or start 256,000. Actual
coordinator elapsed time was **{report['elapsed_seconds']:.3f} seconds**.

## Median timings

All values are seconds. Medians summarize five paired repeats, alternating
the order of the two methods.

| Bound | Lattice preparation + search | Direct CPU setup + search | Direct CPU full process wall | Warm-time gap |
|---:|---:|---:|---:|---:|
| 128,000 | {a['pipeline_seconds']:.6f} | {b['pipeline_seconds']:.6f} | {b['process_wall_seconds']:.6f} | {a['pipeline_seconds']/b['pipeline_seconds']:.2f}x |

Lattice uses the same isolated GMP mpq arithmetic, fpylll reduction, and exact
modular pruning as the previous scaling reports. Direct CPU uses the unchanged
native 128-bit production solver with its modulo-11 filter and production
compiler flags, rebuilt in scratch. Independent oracles, imports, separate
geometry checks, and result serialization are excluded from these medians.
Direct process wall time is recorded separately from its internal setup/search
clocks. All trials are retained in [samples.csv](samples.csv).

## Exact checks, limits, and provenance

The independent signed native 128-bit oracle enumerates sorted x <= y <= z
over the entire signed box without modular filters or shared lattice code.
It passed 44 Python oracle controls and matched all five hash-verified archived
unfiltered GMP oracle results at 2,000 through 32,000. Separate nonempty
controls for residuals 12/384 and 2951 passed with both arithmetic paths and
both CPU binaries before the larger comparison.

All {case['geometry']['patches']:,} patch enclosures, bases, exact reduction
transforms, and Gram–Schmidt values matched between Fraction and GMP. The
geometry transcript hash also matches the previous 128,000 attempt that
stopped at 120 seconds. Post-run review rechecked every trial hash and result,
recomputed the medians, and verified repeated lattice outputs and counters.

The finite 500-million-node and 150,000-patch allowances are unchanged from
the preceding continuation. The run used one logical CPU, nice 19, one
numerical-library thread, and a 2 GiB address-space cap per process. Active
production state, job locks, memory, CPU load, and the GPU validator lock were
monitored. The source package, production CPU sources, and production checkout
status were preserved. No GPU workload or production search was launched.

The lattice source remains pinned to
`91bb89b0ff49974e9458faf19015908e44b85cb8`, and production native source to
`853fd98fc91968987fcb3e9e4c43b4fe880c8246`. This bound is within previously
completed production coverage and adds performance evidence only. The direct
CPU solver remains faster at this measured point; no crossover is projected.

Commands, environment, source/binary identities, and all repeats are in
[report.json](report.json). Executed sources are review transcripts under
[executed-code](executed-code/). Absolute local paths are replaced with
`${{RUN_DIR}}`, `${{CPU_BENCHMARK_WORKSPACE}}`, `${{EVIDENCE_CHECKOUT}}`, and related
aliases. Original source/result hashes refer to local unredacted bytes;
[SHA256SUMS](SHA256SUMS) checks the published artifact bytes.
''')
    sums(CPU_DEST);print('CPU_REPORT',CPU_DEST)

def payload():
    entries=[]
    for directory in (CPU_DEST,GPU_DEST):
        for p in sorted(directory.rglob('*')):
            if p.is_file():entries.append(dict(path=str(p.relative_to(REPO)),mode='100644',type='blob',content=p.read_text()))
    path=ROOT/'github-long-publication.json'
    path.write_text(json.dumps(dict(repository_full_name='paulnord/fifth42',base_tree_sha=BASE_TREE,tree_elements=entries)))
    print('PAYLOAD',path,'FILES',len(entries))

if __name__=='__main__':
    for action in sys.argv[1:] or ('gpu','cpu','payload'):
        {'gpu':gpu,'cpu':cpu,'payload':payload}[action]()
