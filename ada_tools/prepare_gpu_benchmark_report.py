"""Review the saved CUDA trials and export compact, complete timing evidence."""
import csv
import hashlib
import importlib.util
import io
import json
from math import prod
from pathlib import Path
import statistics
import sys

sys.dont_write_bytecode=True
ROOT=Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
sys.path.insert(0,str(ROOT))
import prepare_long_reports as out
RUN=Path('/home/pnord/fifth-lattice-gpu/benchmark-runs/20261105T194406Z-r9b5brzu')
DEST=out.GPU_DEST
out.ALIASES.insert(0,(str(RUN),'${GPU_RUN_DIR}'))

def csv_write(path,rows):
    if not rows:return
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows);out.write(path,stream.getvalue())

def prepare():
    report=json.loads((RUN/'report.json').read_text());result=report['results']
    if report['status']!='passed' or result['status']!='passed':raise RuntimeError('GPU benchmark did not pass')
    if report['completed_bounds']!=[2000,4000,8000] or report['elapsed_seconds']>600:
        raise RuntimeError('GPU benchmark bounds/allowance mismatch')
    if result['gpu_process_wall_seconds']>120 or not report['source_files_preserved']:
        raise RuntimeError('GPU allowance/preservation mismatch')
    for name,digest in report['source_sha256'].items():
        if out.sha(RUN/'workspace'/name)!=digest or out.sha(out.GPU/name)!=digest:
            raise RuntimeError('GPU source hash mismatch: '+name)
    for name,digest in report['binary_sha256'].items():
        if out.sha(RUN/'workspace/bin'/name)!=digest:raise RuntimeError('GPU binary hash mismatch')
    if out.sha(RUN/'workspace/benchmark_model.py')!=result['expanded_model_sha256']:
        raise RuntimeError('Expanded model hash mismatch')
    reference=RUN/'workspace/reference/lattice5.py'
    spec=importlib.util.spec_from_file_location('gpu_benchmark_review_reference',reference)
    ref=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ref;spec.loader.exec_module(ref)
    def decode(plan,data):
        if data.get('box_complete') is not True or data['points_visited']!=plan['points']:
            raise RuntimeError('Incomplete GPU/CPU output')
        if len(data['counts'])!=len(plan['tasks']):raise RuntimeError('Missing task counts')
        for task,count in zip(plan['tasks'],data['counts']):
            points=prod(2*j+1 for j in task['J'])
            if task['points']!=points or count!=dict(id=task['id'],expected=points,visited=points):
                raise RuntimeError('Exact task coverage mismatch')
        hits=set();seen=set();patches={}
        for hit in data['hits']:
            task=plan['tasks'][hit['task']]
            key=(hit['task'],hit['linear'])
            if key in seen or not 0<=hit['linear']<task['points']:raise RuntimeError('Candidate index mismatch')
            seen.add(key);index=hit['linear'];ns=[]
            for j in task['J']:
                ns.append(index%(2*j+1)-j);index//=2*j+1
            c,a,b=[sum(ns[i]*task['U'][i][col] for i in range(3)) for col in range(3)]
            r=a**5+b**5-c**5
            if (a,b,c)!=(hit['a'],hit['b'],hit['c']) or not 1<=a<=b<c<=plan['bound'] or abs(r)>plan['cap']:
                raise RuntimeError('Candidate reconstruction/residual mismatch')
            if task['id'] not in patches:
                patches[task['id']]=ref.make_patch(task['cmin'],task['cmax'],ref.Q(*task['left']),
                    ref.Q(*task['right']),task['cap'],task['bits'])
            if patches[task['id']].contains(a,b,c):hits.add((a,b,c,r))
        for lo,hi in plan['direct_shells']:
            for c in range(lo,hi+1):
                for b in range(1,c):
                    for a in range(1,b+1):
                        r=a**5+b**5-c**5
                        if abs(r)<=plan['cap']:hits.add((a,b,c,r))
        return hits
    samples=[];table=[];checks=[]
    for control in result['controls']:
        plan=json.loads((RUN/'plans'/f"B{control['bound']}-cap{control['cap']}.json").read_text())
        expected={tuple(h) for h in control['expected']}
        for name,data in control['backends'].items():
            if decode(plan,data['result'])!=expected:raise RuntimeError('Control oracle mismatch: '+name)
    for case in result['cases']:
        bound=case['bound'];plan_path=RUN/'plans'/f'B{bound}-cap42.json'
        plan=json.loads(plan_path.read_text())
        packet=RUN/'packets'/f'B{bound}-cap42.txt'
        if out.sha(packet)!=case['packet_sha256']:raise RuntimeError('Packet hash mismatch')
        oracle=json.loads((RUN/'oracles'/f'B{bound}-cap42.json').read_text())['result']
        expected={tuple(h) for h in oracle['hits']}
        if not oracle['complete'] or expected!={tuple(h) for h in case['oracle_hits']}:
            raise RuntimeError('Independent positive oracle mismatch')
        raw_candidates=None
        for name,rows in case['samples'].items():
            if len(rows)!=5 or not case['complete']:raise RuntimeError('Missing paired GPU trials')
            for sample in rows:
                path=RUN/sample['result_file']
                if out.sha(path)!=sample['result_sha256']:raise RuntimeError('Trial hash mismatch')
                trial=json.loads(path.read_text());data=trial['result']
                if data['backend']!=('gpu' if name=='cuda' else 'emulated'):raise RuntimeError('Backend label mismatch')
                if decode(plan,data)!=expected or {tuple(h) for h in trial['decoded_hits']}!=expected:
                    raise RuntimeError('Exact decoded trial/oracle mismatch')
                candidate_set=sorted(tuple(h[k] for k in ('task','linear','a','b','c')) for h in data['hits'])
                if raw_candidates is None:raw_candidates=candidate_set
                if candidate_set!=raw_candidates:raise RuntimeError('Raw candidates differ across paired repeats')
                samples.append(dict(bound=bound,backend=name,repeat=sample['repeat'],
                    preparation_seconds=case['preparation_seconds'],
                    **{k:sample[k] for k in case['medians'][name]}))
            for key,value in case['medians'][name].items():
                if statistics.median(row[key] for row in rows)!=value:raise RuntimeError('GPU median mismatch')
        csv_write(DEST/'counts'/f'B{bound}.csv',[dict(task_id=t['id'],expected_points=t['points'],
            emulated_visited=t['points'],cuda_visited=t['points']) for t in plan['tasks']])
        out.js(DEST/'candidates'/f'B{bound}.json',dict(exact_hits=sorted(expected),
            raw_candidates=raw_candidates,raw_fields=['task','linear','a','b','c'],
            identical_across_all_ten_trials=True,plan_sha256=out.sha(plan_path),packet_sha256=out.sha(packet)))
        cpu,cuda=case['medians']['emulated'],case['medians']['cuda']
        table.append(f"| {bound:,} | {cpu['engine_seconds']*1000:.3f} | {cuda['engine_seconds']*1000:.3f} | "
            f"{cpu['end_to_end_seconds']:.3f} | {cuda['end_to_end_seconds']:.3f} |")
        checks.append(dict(bound=bound,exact_checked_trials=10,medians_recomputed=True,
            all_task_counts_complete=True,raw_candidates_identical=True,exact_hits=sorted(expected)))
    review=dict(status='passed',source_files_verified=len(report['source_sha256']),
        timed_trials=30,paired_repeats_per_bound=5,cases=checks,
        both_nonempty_controls_rechecked=True,source_and_binary_hashes_verified=True,
        expanded_model_hash_verified=True,within_600_second_allowance=True,
        within_120_second_cuda_process_allowance=True)
    out.js(DEST/'post-run-review.json',review)
    for name in ('report.json','results.json','events.jsonl','config.json','host-tests.stdout.txt',
        'host-tests.stderr.txt','build.stdout.txt','build.stderr.txt','compile-oracle.stdout.txt',
        'compile-oracle.stderr.txt','benchmark-worker.stdout.txt','benchmark-worker.stderr.txt'):
        out.export(RUN/name,DEST/name)
    for p in (RUN/'oracles').iterdir():out.export(p,DEST/'oracles'/p.name)
    csv_write(DEST/'samples.csv',samples)
    manifest={str(p.relative_to(RUN)):dict(sha256=out.sha(p),bytes=p.stat().st_size)
        for p in sorted(RUN.rglob('*')) if p.is_file()}
    out.js(DEST/'local-artifact-manifest.json',manifest)
    out.write(DEST/'README.md',f'''# ADA larger CUDA benchmark — 2026-11-05

**PASS:** all 30 timed trials completed: five alternating CUDA/CPU-emulation
pairs at 2,000, 4,000, and 8,000. Every decoded exact result matched an
independent unfiltered positive-domain oracle, and every task's complete
coefficient count matched its certified packet. Both nonempty controls passed
on CUDA, ordinary CPU emulation, and sanitized CPU emulation before timing.

The run took **{report['elapsed_seconds']:.3f} seconds** of its ten-minute
allowance. CUDA subprocesses used {result['gpu_process_wall_seconds']:.3f}
seconds of their separate cumulative 120-second allowance. The GPU was an
NVIDIA GeForce RTX 3080 Ti with 12,288 MiB and driver 595.99.02. The run used
one host CPU and one GPU after the CPU scaling benchmark released its lock.

## Median timings

Engine columns are milliseconds; total columns are seconds. Each median
uses five repeats. CPU here means ordinary coefficient-box emulation, a
different comparator from the optimized direct CPU solver in the scaling
reports.

| Bound | CPU engine (ms) | CUDA engine (ms) | CPU total (s) | CUDA total (s) |
|---:|---:|---:|---:|---:|
{chr(10).join(table)}

At 8,000, the CUDA engine was about 3.89 times faster than emulation. Total
CUDA time remained slightly higher. Host plan preparation and packet
certification took 100.048 seconds, and exact host verification took about
3.3 seconds per trial; those stages dominate the total. A CUDA process took
about 0.382 seconds including process/context startup, versus a 0.01072-second
engine time and a 0.000332-second kernel time. These measurements support
faster device enumeration, without an end-to-end speedup for this pipeline.

Each domain was prepared once. Total time charges its preparation cost once
to each trial's process-plus-verification time. Cached-packet timing excludes
that preparation. Every engine invocation starts a new process; kernel and
engine timing exclude process/context startup. All individual metrics are in
[samples.csv](samples.csv) and [results.json](results.json). Independent oracle
work is excluded from medians and included in the overall resource allowance.

## Coverage and verification

The domain was `1 <= a <= b < c <= bound` with
`abs(a^5+b^5-c^5) <= 42`. This is the earlier coefficient-box prototype,
separate from the newer fpylll/pruning/GMP lattice experiment. Patch counts
were 924, 1,846, and 3,690; coefficient counts were 1,519,384, 3,056,728, and
6,643,828. All three bounds found the same exact positive residual tuples:
`(1,1,2,-30)` and `(13,16,17,12)`. Neither is a signed target-42 solution.

The isolated benchmark planner extended the full-domain bound to 8,000.
The validated default planner and all 16 original validated source files
remain unchanged. Task, point, integer, exact-certificate, output, and coverage
guards were retained. Eleven host tests and the serial build passed.

Post-run review verified all 19 executed source identities, all binary hashes,
the isolated model and packet hashes, every raw trial hash, exact candidate
reconstruction and patch membership, every task count, repeated raw candidates,
all decoded hits against the independent oracle, and all reported medians.
The ordinary CPU and CUDA raw candidate sets were identical across all five
pairs at each bound. See [post-run-review.json](post-run-review.json).

## Artifacts and reproduction

[TERMINAL_INSTRUCTIONS.md](TERMINAL_INSTRUCTIONS.md) documents the installed
`python3 ~/fifth-lattice-gpu/benchmark.py --wait` runner and all limits.
The complete local run, including the large exact plans and every original
trial, remains at `${{GPU_RUN_DIR}}`. [local-artifact-manifest.json](local-artifact-manifest.json)
records every local file's original SHA-256 and size. Full plan files total
about 33 MB and are retained locally. This publication includes every trial's
timing and hash, the complete per-task counts without repeating identical
tables ten times, exact candidate summaries, independent oracle outputs,
source review transcripts, and build/test logs.

Absolute local paths and the GPU UUID are replaced with documented aliases.
Original hashes refer to local bytes; [SHA256SUMS](SHA256SUMS) verifies the
published artifact bytes. Source transcripts require actual paths and their
ordinary filenames before installation elsewhere. These results do not add
production search coverage or establish a CUDA win over the direct CPU solver.
''')
    # Preserve hardware model and driver while omitting a machine-specific UUID.
    for p in DEST.rglob('*'):
        if p.is_file() and p.suffix in ('.json','.md','.txt'):
            content=p.read_text()
            import re
            content=re.sub(r'GPU-[0-9a-fA-F-]{36}', '${GPU_UUID}', content)
            p.write_text(content)
    out.sums(DEST)
    print('GPU_BENCHMARK_REPORT',DEST)

if __name__=='__main__':prepare()
