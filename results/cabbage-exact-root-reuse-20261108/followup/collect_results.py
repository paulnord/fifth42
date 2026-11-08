import hashlib,json,statistics
from pathlib import Path
root=Path(__file__).resolve().parent
out=root/'gpu-results'
rows=[];raw_timings=[];native={}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for path in sorted(out.glob('*/result.json')):
 trial=path.parent.name;case,repeat,variant=trial.rsplit('-',2)
 result=json.loads(path.read_text());result.update(case=case,repeat=int(repeat),trial=trial)
 rows.append({k:v for k,v in result.items() if k!='rows'})
 responses=json.loads((out/(trial+'.raw.json')).read_text())
 records=[dict(packet_sha256=r['packet_sha256'],counts=r['response']['counts'],hits=sorted(r['response']['hits'],key=lambda h:(h['task'],h['linear']))) for r in responses]
 key=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert key==result['native_records_sha256']
 if case in native:assert native[case]==records,('Native exact record mismatch',trial)
 else:native[case]=records
 raw_timings.append(dict(trial=trial,packets=[dict(packet_sha256=r['packet_sha256'],rpc_wall_seconds=r['wall_seconds'],native_engine_seconds=r['response']['engine_seconds'],cuda_kernel_seconds=r['response']['kernel_seconds'],points=r['response']['points_visited']) for r in responses]))
summary=[];pairs=[]
for case in ('boole','ada','higher_cost'):
 group={v:sorted([r for r in rows if r['case']==case and r['variant']==v],key=lambda r:r['repeat']) for v in ('baseline','candidate')}
 matched=[]
 for a in group['baseline']:
  b=next((r for r in group['candidate'] if r['repeat']==a['repeat']),None)
  if b is None:continue
  for k in ('signatures_sha256','native_records_sha256','points','exact_hits'):assert a[k]==b[k],(case,k)
  assert a['recovery_passed'] and b['recovery_passed']
  matched.append((a,b));pairs.append(dict(case=case,repeat=a['repeat'],points=a['points'],signatures_sha256=a['signatures_sha256'],native_records_sha256=a['native_records_sha256'],exact_hits=a['exact_hits'],recovery_passed=True))
 med={v:statistics.median(r['steady_seconds'] for r in g) if g else None for v,g in group.items()}
 summary.append(dict(case=case,complete_pairs=len(matched),medians=med,throughput_ratio=med['baseline']/med['candidate'] if matched else None,samples={v:[{k:r[k] for k in ('repeat','steady_seconds','startup_seconds','shutdown_seconds','native_engine_seconds','cuda_kernel_seconds','gpu_rpc_seconds','points')} for r in g] for v,g in group.items()}))
report=dict(status='stopped_on_resource_conflict',cuda_executed=True,production_coverage=False,gpu_correctness_passed=True,planned_timing_trials=30,completed_timing_trials=len(rows),completed_pairs=len(pairs),summary=summary,pair_checks=pairs,rows=rows,stop=json.loads((root/'gpu-suite-failure.json').read_text()),limitations=['Fresh local journals only; no NFS or shared ledger tests.','Bounded selected windows, not full-shell coverage.','Short samples; resource monitoring and clock variability can affect timings.','Same range-corrected native binary for both host-source variants.','Incomplete higher-cost pair excluded from speedup claims.'])
(out/'partial-benchmark-results.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'native-timings.json').write_text(json.dumps(raw_timings,indent=2)+'\n')
for case,records in native.items():(out/f'{case}-exact-native-records.json').write_text(json.dumps(records,separators=(',',':'))+'\n')
files={str(p.relative_to(root)):dict(sha256=digest(p),bytes=p.stat().st_size) for folder in ('device','baseline/source/lattice_prototype','candidate/source/lattice_prototype') for p in sorted((root/folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
(root/'source-and-binary-identities.json').write_text(json.dumps(dict(tested_commit='be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f',files=files),indent=2)+'\n')
assert len(rows)==21 and len(pairs)==10
print(json.dumps(summary,indent=2))
