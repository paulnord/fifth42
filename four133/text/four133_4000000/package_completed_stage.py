#!/usr/bin/env python3
"""Bundle the completed audited parallel stage and its full prior evidence chain."""
import hashlib,json,tarfile
from pathlib import Path
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((R/'audit_production_report.json').read_text());p=json.loads((R/'runs/progress.json').read_text());e=json.loads((R/'execution_20261104T154820Z.json').read_text());b=json.loads((R/'benchmark/results.json').read_text())
assert a['complete'] and a['checked_chunks']==236 and a['checked_checkpoints']==240226 and a['exact_solutions']==[]
assert all(v==0 for v in a['raw_matches'].values()) and p['status']=='completed_awaiting_independent_audit' and e['return_code']==0
assert p['workers_requested']==p['maximum_active_chunks']==b['selected_workers']==9
prior=R.parent/'four133_3000000_reproduction.tar.gz'
result=dict(bound=4000000,previous_bound=3000000,target=42,exponent=133,interval_inclusive=True,distinct_base_solutions_found=0,repeated_bases_also_excluded_by_raw_zero=True,independently_audited=True,moduli=list(p['by_modulus']),workers=9,completed_chunks=236,completed_gap_checkpoints=240226,filtered_entries_per_modulus={m:v['left']+v['right'] for m,v in p['by_modulus'].items()},filtered_entries_total=sum(v['left']+v['right'] for v in p['by_modulus'].values()),modular_matches=0,wall_seconds=e['elapsed_seconds'],child_cpu_seconds=e['child_user_cpu_seconds']+e['child_system_cpu_seconds'],sampled_combined_peak_rss_kib=e['sampled_coordinator_plus_descendants_peak_rss_kib'],peak_search_process_rss_kib=p['peak_search_process_rss_kib'],production_log_bytes=p['log_bytes'],stage_allocated_bytes_at_compute_completion=e['directory_allocated_bytes'],measured_benchmark_speedup_over_one=b['speedup_over_one'],source_sha256=sha(R/'search133_incremental.cpp'),driver_sha256=sha(R/'run_parallel.py'),audit_report_sha256=sha(R/'audit_production_report.json'),prior_bundle_sha256=sha(prior),scope_caveat='A finite negative computational result, not a global impossibility theorem or formal executable verification.')
(R/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'RESULT.txt').write_text('No four distinct signed integer bases in the inclusive interval [-4,000,000, 4,000,000] have 133rd powers summing to 42.\n\nThe new three-million-to-four-million shell completed with nine workers: all 236 chunks and 240,226 gap checkpoints passed independent reconciliation. Both modular passes found zero candidates, after 33,596,847,250 filtered pair entries. Wall time was 6 minutes 1 second. Sampled combined coordinator-plus-search RSS peaked at 353,392 KiB, about 345 MiB. Production logs occupied 26,728,464 bytes.\n\nThe same bounded worker benchmark measured 29.73 seconds with one worker and 4.01 seconds with nine, a 7.4-fold speedup. That is a measured benchmark comparison, not a separate full serial four-million run.\n\nThe new shell is joined with the frozen, independently audited inclusive three-million result. Its included reproduction archive contains the earlier 2.1-million archive, preserving the complete evidence chain. Unpack each prior archive beside its successor directory before running prior-evidence checks. Zero raw matches also exclude repeated-base cases under the audited sign/order reductions.\n\nThis remains a finite negative result, not a global impossibility proof. No formal proof-checker installation was changed. No ada, Valpo, or BNL resource was used.\n')
names=['README.md','RESULT.txt','result.json','independent_mathematical_audit.md','search133_incremental.cpp','search133_incremental','run_parallel.py','execute_stage.py','build.json','benchmark_parallel.py','benchmark_execution.log','audit_production_counts.py','audit_production_report.json','execution_20261104T154820Z.log','execution_20261104T154820Z.json','package_completed_stage.py']
files=[R/n for n in names]
for d in ['runs','benchmark','audit_parallel/patched']:
    files += [f for f in (R/d).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
files=sorted(set(files));entries={str(f.relative_to(R)):dict(bytes=f.stat().st_size,sha256=sha(f)) for f in files}
manifest=dict(result='Completed audited inclusive bound 4,000,000',files=entries,prior_archive=dict(name=prior.name,bytes=prior.stat().st_size,sha256=sha(prior)))
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');files.append(R/'manifest.json')
out=R.parent/'four133_4000000_reproduction.tar.gz'
with tarfile.open(out,'w:gz') as t:
    for f in files:t.add(f,arcname='four133_4000000/'+str(f.relative_to(R)))
    t.add(prior,arcname=prior.name)
with tarfile.open(out,'r:gz') as t:
    for name,desc in entries.items():
        raw=t.extractfile('four133_4000000/'+name).read();assert len(raw)==desc['bytes'] and hashlib.sha256(raw).hexdigest()==desc['sha256']
    assert hashlib.sha256(t.extractfile(prior.name).read()).hexdigest()==sha(prior)
print(json.dumps(dict(archive=str(out),bytes=out.stat().st_size,sha256=sha(out),hashed_members=len(entries)+1,result=result),indent=2))
