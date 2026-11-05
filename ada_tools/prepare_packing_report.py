"""Review and publish packing-only measurements without duplicating count tables."""
from dataclasses import fields
import hashlib
import json
from pathlib import Path
import statistics
import sys

sys.dont_write_bytecode=True
ROOT=Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
sys.path.insert(0,str(ROOT))
import prepare_long_reports as out
GPU=Path('/home/pnord/fifth-lattice-gpu')
sys.path.insert(0,str(GPU))
import scaling_core as core
import packing_opt as optimized
RUN=GPU/'packing-runs/20261105T212247Z-i0gdlbsz'
REFERENCE=GPU/'scaling-runs/20261105T210028Z-7wjebufp'
DEST=out.REPO/'ada_validation/lattice-packing-20261105'
out.ALIASES.insert(0,(str(RUN),'${PACKING_RUN_DIR}'))
out.ALIASES.insert(0,(str(REFERENCE),'${REFERENCE_SCALING_RUN_DIR}'))

def freeze(value):return tuple(freeze(v) for v in value) if isinstance(value,list) else value

def prepare():
    report=json.loads((RUN/'report.json').read_text());result=report['results']
    if report['status']!='passed' or result['status']!='passed':raise RuntimeError('Packing comparison did not pass')
    if report['elapsed_seconds']>600 or result['gpu_request_wall_seconds']>120:
        raise RuntimeError('Packing comparison exceeded its resource allowance')
    if not result['all_geometry_and_packet_bytes_equal'] or not result['fresh_geometry_every_timed_variant']:
        raise RuntimeError('Packing comparison identity/freshness checks failed')
    for name,digest in report['source_sha256'].items():
        if out.sha(RUN/'workspace'/name)!=digest:raise RuntimeError('Executed source hash mismatch: '+name)
    for name,digest in report['binary_sha256'].items():
        if out.sha(RUN/'workspace/bin'/name)!=digest:raise RuntimeError('Executed binary hash mismatch: '+name)
    for key in ('source_files_preserved','lattice_source_preserved','direct_sources_preserved'):
        if report[key] is not True:raise RuntimeError('Run preservation check failed: '+key)
    if out.sha(GPU/'packing_opt.py')!=report['source_sha256']['packing_opt.py']:
        raise RuntimeError('Installed optimized packer differs from the measured packer')
    core.initialize(out.REPO/'lattice_prototype')
    plans={};identities={}
    for bound in (8000,32000):
        data=json.loads((REFERENCE/'plans'/f'B{bound}.json').read_text())
        tasks=[core.Task(**{k:freeze(v) for k,v in row.items()}) for batch in data['batches'] for row in batch['tasks']]
        specifications,direct=core.specs(bound,42)
        tokens=[core.task_digest(t) for t in tasks]
        if any(optimized.task_digest(t)!=digest for t,digest in zip(tasks,tokens)):
            raise RuntimeError('Canonical certificate hashes differ')
        baseline=core.assemble(bound,42,specifications,direct,tasks,tokens)
        candidate=optimized.assemble(bound,42,specifications,direct,tasks,tokens)
        if baseline!=candidate or baseline.certificate_sha256!=data['certificate_sha256']:
            raise RuntimeError('Complete baseline/candidate/reference plans differ')
        plans[bound]=baseline
        identities[bound]=dict(certificate_sha256=baseline.certificate_sha256,tasks=baseline.tasks,
            points=baseline.points,packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in baseline.batches],
            direct_hits=[list(h) for h in baseline.direct_hits])
        rows=[]
        for batch_id,batch in enumerate(baseline.batches):
            for local,task in enumerate(batch.tasks):
                rows.append(dict(batch=batch_id,local_task=local,global_task=task.id,coefficient_points=task.points))
        out.csv_write(DEST/'counts'/f'B{bound}.csv',rows)
    samples=[];medians=[];table=[];observations=0
    for case in result['cases']:
        if not case['complete'] or case['identity']!=identities[case['bound']]:
            raise RuntimeError('Measured case identity mismatch')
        plan=plans[case['bound']]
        oracle=json.loads((RUN/'oracles'/f"B{case['bound']}-cap42.json").read_text())
        expected={tuple(h) for h in oracle['hits']}
        for variant,backends in case['samples'].items():
            for backend,rows in backends.items():
                if len(rows)!=5:raise RuntimeError('Missing paired repeat')
                for sample in rows:
                    path=RUN/sample['result_file']
                    if out.sha(path)!=sample['sha256']:raise RuntimeError('Raw trial hash mismatch')
                    trial=json.loads(path.read_text());hits=set(plan.direct_hits)
                    if len(trial['batches'])!=len(plan.batches):raise RuntimeError('Missing streamed batch')
                    for batch,data in zip(plan.batches,trial['batches']):
                        hits|=core.decode_batch(batch,data,'gpu' if backend=='cuda' else 'emulated')
                    if hits!=expected or hits!={tuple(h) for h in trial['exact_hits']} or not trial['oracle_equal']:
                        raise RuntimeError('Independent exact trial hit set mismatch')
                    for key,value in trial['metrics'].items():
                        if sample[key]!=value:raise RuntimeError('Trial metric mismatch')
                    samples.append(dict(regime=case['regime'],bound=case['bound'],variant=variant,backend=backend,
                        repeat=sample['repeat'],**{k:sample.get(k,'') for k in ('prepare_seconds','certificate_seconds',
                            'packing_seconds','total_preparation_seconds','engine_seconds','kernel_seconds',
                            'request_wall_seconds','output_verification_seconds','end_to_end_seconds',
                            'cold_startup_seconds','shutdown_seconds','cold_one_pass_seconds')},
                        original_result_sha256=sample['sha256']))
                    observations+=1
                calculated={key:statistics.median(row[key] for row in rows)
                    for key in case['medians'][variant][backend]}
                if calculated!=case['medians'][variant][backend]:raise RuntimeError('Median mismatch')
                medians.append(dict(regime=case['regime'],bound=case['bound'],variant=variant,backend=backend,
                    **{k:calculated.get(k,'') for k in ('packing_seconds','total_preparation_seconds',
                        'end_to_end_seconds','cold_one_pass_seconds')}))
        key='cold_one_pass_seconds' if case['regime']=='cold_one_pass' else 'end_to_end_seconds'
        a=case['medians']['baseline']['cuda'][key];b=case['medians']['optimized']['cuda'][key]
        table.append(f"| {'Cold one-pass' if case['regime']=='cold_one_pass' else 'Persistent engines'} | "
            f"{case['bound']:,} | {a:.6f} | {b:.6f} | {100*(1-b/a):.1f}% |")
    if observations!=60:raise RuntimeError('Expected all 60 timed pipeline observations')
    review=dict(status='passed',timed_pipeline_observations=observations,paired_repeats_per_case=5,
        freshly_prepared_timed_variants=40,all_medians_recomputed=True,
        every_batch_and_task_coverage_count_verified=True,every_exact_hit_set_matches_independent_oracle=True,
        original_and_optimized_plans_equal=True,all_original_canonical_hashes_and_packet_bytes_equal=True,
        measured_source_and_binary_hashes_verified=True,installed_packer_matches_measured_source=True,
        resource_and_preservation_checks_passed=True,identities=identities)
    out.js(DEST/'post-run-review.json',review)
    out.csv_write(DEST/'samples.csv',samples);out.csv_write(DEST/'medians.csv',medians)
    for name in ('report.json','results.json','events.jsonl','config.json','build.stdout.txt','build.stderr.txt',
                 'host-tests.stdout.txt','host-tests.stderr.txt','scaling-worker.stdout.txt','scaling-worker.stderr.txt'):
        out.export(RUN/name,DEST/name)
    for path in (RUN/'oracles').iterdir():out.export(path,DEST/'oracles'/path.name)
    for name in report['source_sha256']:
        out.export(RUN/'workspace'/name,DEST/'executed-source'/(name+'.txt'))
    installed={}
    for name in ('packing_opt.py','packing_benchmark.py','scaling.py','tests/test_packing.py','PACKING.md'):
        installed[name]=dict(sha256=out.sha(GPU/name),measured_sha256=report['source_sha256'].get(name))
        out.export(GPU/name,DEST/'installed-source'/(name+'.txt'))
    out.js(DEST/'installed-source-identities.json',installed)
    profile=GPU/'packing-runs/profile-6ycl6rox'
    for name in ('packing-profile.txt','paired-packing.json','report.json'):
        if name=='packing-profile.txt':
            out.write(DEST/'diagnostic-profile'/name,(profile/name).read_text().rstrip()+'\n')
        else:
            out.export(profile/name,DEST/'diagnostic-profile'/name)
    manifest={str(p.relative_to(RUN)):dict(sha256=out.sha(p),bytes=p.stat().st_size)
        for p in sorted(RUN.rglob('*')) if p.is_file()}
    out.js(DEST/'local-artifact-manifest.json',manifest)
    out.write(DEST/'README.md',f'''# Packing-only optimization on ADA — 2026-11-05

**PASS:** the optimized packer preserves the exact geometry, canonical JSON
certificate bytes and SHA-256 values, immutable plans, streamed engine packet
bytes, candidate boxes, coverage counts, and exact hit sets. All 60 timed
pipeline observations passed. Each of four cases contains five alternating
baseline/optimized pairs. The experiment used 16 physical CPU cores and one
RTX 3080 Ti, with a ten-minute total allowance. Suite elapsed time was
**{report['elapsed_seconds']:.3f} seconds**; this is distinct from per-search timing.

## Per-search medians

All values are seconds. Every timed variant generated and certified **fresh
geometry**. No prepared-geometry cache or changed patch width contributed to
the measured gain.

| Execution regime | Bound | Baseline GPU pipeline | Optimized GPU pipeline | Time reduction |
|---|---:|---:|---:|---:|
{chr(10).join(table)}

Persistent-engine measurements retain the existing worker pool and CPU/CUDA
engine processes, while rebuilding the geometry and verifying it for every
variant. They include preparation, certification, packing, engine requests,
and exact output validation. Actual cold one-pass measurements create fresh
workers and a fresh GPU process for each variant and include their startup
and shutdown in measured elapsed time. Cold values are real lifetime
measurements, rather than warm medians plus an estimated startup constant.
Report-file writes are outside both timing definitions.

The persistent-engine CPU pipeline was also paired against the same change;
all CPU and CUDA samples and stage metrics are in [samples.csv](samples.csv).
Medians are recomputed independently in [medians.csv](medians.csv).
Each preparation is charged once to each CPU/GPU pipeline measurement using it;
there were 40 fresh preparations across the timed comparisons.

## Change and validation

Profiling identified repeated recursive `dataclasses.asdict()` conversion
inside parent-process certificate identity checks. Task fields are immutable
integer/tuple data. The new serializer reads those fields directly and uses
the **same** canonical JSON settings and SHA-256 hash. It keeps the full
parent-process identity check and all exact arithmetic, transform, enclosure,
resource, and coverage guards. Packet construction is unchanged.

At bound 32,000, persistent-engine packing medians fell from 0.632695 to
0.360282 seconds. The full pipeline gain was 17.6%, not the hypothetical
1.7x ceiling for eliminating all packing. The diagnostic profiler and isolated
packing timing reused saved geometry solely to locate/measure the packing
cost; those results are clearly labeled and are not full-workflow evidence.

Four targeted tests cover canonical bytes for every task field, complete plan
and packet identity across split batches, tampering/missing patches/exhausted
budgets, and AST equality of the assembly algorithm after namespace
normalization. All 22 local tests passed before and after launcher integration;
the frozen benchmark scratch ran 19 tests (the three unrelated older benchmark
tests are not copied into that scratch workspace). Nonempty oracle controls
at bounds 34 and 100 preceded timing. Post-run review verified every trial
hash, decoded every streamed response with the original checks, checked every
task's full count, compared exact results with the independent oracle, and
recomputed every median. See [post-run-review.json](post-run-review.json).

## Use and reproduce

The installed `scaling.py` launcher now selects optimized packing by default.
`--packing baseline` retains the old path. This selection changes only which
assembly function is called; the exact canonical hash format is unchanged.
The measured optimized module is byte-identical to the installed module.

```bash
python3 ~/fifth-lattice-gpu/scaling.py --wait
python3 ~/fifth-lattice-gpu/scaling.py --packing baseline --wait
python3 ~/fifth-lattice-gpu/packing_benchmark.py --wait
```

The first two commands run the larger scaling matrix. The third reproduces
this isolated 16-worker packing comparison. Execute GPU commands in an
approved GPU-visible environment. The ordinary scaling matrix retains its
20-minute cap; the packing comparison has a ten-minute cap. No wider-patch
or preparation-reuse experiment was started. Production source, binaries,
checkpoints, and the original pinned lattice package were preserved.

## Artifacts

The full local benchmark remains at `${{PACKING_RUN_DIR}}`.
[local-artifact-manifest.json](local-artifact-manifest.json) records every
original local file's hash and size. This publication retains all timing
samples and original trial hashes, canonical task-count tables, exact oracles,
executed source transcripts, build/test logs, and the post-run review. Repeated
large count tables and binaries remain local. Canonical geometry/packet
identities match the earlier complete scaling plans.

[executed-source](executed-source/) contains exactly the code used for the
measurements. [installed-source](installed-source/) records the subsequent
launcher default and rollback-option integration, checked with the same unit
tests. Source transcripts use ordinary local filenames plus `.txt` and replace
absolute local paths with aliases; substitute actual paths before installing
elsewhere. Original hashes refer to local bytes, while
[SHA256SUMS](SHA256SUMS) verifies the published artifact bytes.
''')
    out.sums(DEST)
    entries=[dict(path=str(p.relative_to(out.REPO)),mode='100644',type='blob',content=p.read_text())
        for p in sorted(DEST.rglob('*')) if p.is_file()]
    payload=dict(repository_full_name='paulnord/fifth42',base_tree_sha='095541604d5cc94398f8295b15c294637eae68f6',tree_elements=entries)
    (ROOT/'github-packing-publication.json').write_text(json.dumps(payload))
    print(json.dumps(dict(report=str(DEST),files=len(entries),observations=observations,
        payload_bytes=(ROOT/'github-packing-publication.json').stat().st_size)))

if __name__=='__main__':prepare()
