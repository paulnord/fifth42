#!/usr/bin/env python3
"""Package the already completed and audited stage without rewriting its evidence."""
import hashlib,json,tarfile
from pathlib import Path
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((R/'audit_production_report.json').read_text());p=json.loads((R/'runs/progress.json').read_text());e=json.loads((R/'execution_20261104T152037Z.json').read_text())
assert a['complete'] and a['checked_chunks']==180 and a['checked_checkpoints']==180538 and a['exact_solutions']==[]
assert all(v==0 for v in a['raw_matches'].values()) and p['status']=='completed_awaiting_independent_audit' and e['return_code']==0
result=dict(bound=3000000,previous_bound=2100000,target=42,exponent=133,interval_inclusive=True,distinct_base_solutions_found=0,repeated_bases_also_excluded_by_raw_zero=True,independently_audited=True,moduli=list(p['by_modulus']),completed_chunks=180,completed_gap_checkpoints=180538,filtered_entries_per_modulus={m:v['left']+v['right'] for m,v in p['by_modulus'].items()},filtered_entries_total=sum(v['left']+v['right'] for v in p['by_modulus'].values()),modular_matches=0,wall_seconds=e['elapsed_seconds'],summed_chunk_compute_seconds=p['compute_seconds'],peak_search_process_rss_kib=p['peak_rss_kib'],production_log_bytes=p['log_bytes'],stage_allocated_bytes_at_compute_completion=e['directory_allocated_bytes'],source_sha256=sha(R/'search133_incremental.cpp'),driver_sha256=sha(R/'run_incremental.py'),audit_report_sha256=sha(R/'audit_production_report.json'),prior_bundle_sha256=sha(R.parent/'four133_extension_2100000.tar.gz'),scope_caveat='A finite negative computational result, not a global impossibility theorem or formal executable verification.')
(R/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'RESULT.txt').write_text('No four distinct signed integer bases in the inclusive interval [-3,000,000, 3,000,000] have 133rd powers summing to 42.\n\nAll 180 incremental chunks and 180,538 gap checkpoints passed independent reconciliation. Both modular passes found zero candidates, after 15,423,986,252 filtered pair entries in total. Wall time was 21 minutes 42 seconds. Peak search-process RSS was 31,216 KiB. Production logs occupied '+str(p['log_bytes'])+' bytes.\n\nThe shell (2,100,000, 3,000,000] is joined with the preserved prior inclusive 2,100,000 result. The included prior archive contains that evidence. Extract it beside this directory to run the prior-evidence verification. Zero raw matches also exclude repeated-base cases under the audited sign/order reductions.\n\nThis remains a finite negative result, not a proof of global impossibility. No formal proof-checker installation was used.\n')
names=['README.md','RESULT.txt','result.json','independent_extended_proof.md','search133_incremental.cpp','search133_incremental','run_incremental.py','execute_stage.py','build.json','audit_incremental_small.py','audit_incremental_small.json','audit_incremental_ubsan','audit_production_counts.py','audit_production_report.json','execution_20261104T152037Z.log','execution_20261104T152037Z.json','package_completed_stage.py','audit_resume/audit_tests.py','audit_resume/audit_report.json']
files=[R/n for n in names]
files+=list((R/'runs').glob('*.log'))+[R/'runs/config.json',R/'runs/progress.json']
for d in ['audit_resume/isolated','audit_resume/run','test_resume_v3']:
    files += [x for x in (R/d).rglob('*') if x.is_file() and '__pycache__' not in x.parts]
for pat in ['audit_*_400_*.log','audit_*_1000_*.log']:files+=list(R.glob(pat))
files=sorted(set(files));prior=R.parent/'four133_extension_2100000.tar.gz'
entries={str(f.relative_to(R)):dict(bytes=f.stat().st_size,sha256=sha(f)) for f in files}
manifest=dict(result='Completed audited inclusive bound 3,000,000',files=entries,prior_archive=dict(name=prior.name,bytes=prior.stat().st_size,sha256=sha(prior)))
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');files.append(R/'manifest.json')
out=R.parent/'four133_3000000_reproduction.tar.gz'
with tarfile.open(out,'w:gz') as t:
    for f in files:t.add(f,arcname='four133_3000000/'+str(f.relative_to(R)))
    t.add(prior,arcname=prior.name)
with tarfile.open(out,'r:gz') as t:
    for name,desc in entries.items():
        b=t.extractfile('four133_3000000/'+name).read();assert len(b)==desc['bytes'] and hashlib.sha256(b).hexdigest()==desc['sha256']
    assert hashlib.sha256(t.extractfile(prior.name).read()).hexdigest()==sha(prior)
print(json.dumps(dict(archive=str(out),bytes=out.stat().st_size,sha256=sha(out),hashed_members=len(entries)+1,result=result),indent=2))
