from pathlib import Path
import hashlib,json,shutil
r=Path(__file__).resolve().parent
prior=Path('/home/pnord/scratch/saved-root-followup-DL829jCa')
probe=Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108')
capture=r/'cross-host-evidence';capture.mkdir()
for name in ('ada-ready.json','cabbage-ready.json','ada-claim.json','cabbage-claim.json','ada-adjacent.json','cabbage-adjacent.json','ada-holder-ready.json','initial-checkpoint.json','cabbage-busy-confirmed.json','ada-recovery-ready.json','cabbage-holder-ready.json','ada-busy-confirmed.json','ada-result.json','cabbage-result.json'):
 p=probe/name
 if p.exists():shutil.copyfile(p,capture/name)
stop=json.loads((prior/'cross-host-probe-failure.json').read_text())
for filename in ('CABBAGE_READINESS.json','LAUNCH-INTENT.json'):
 p=r/filename;x=json.loads(p.read_text())
 if filename=='CABBAGE_READINESS.json':
  x.update(status='LOCAL_ACCEPTANCE_PASSED_CROSS_HOST_PROBE_INTERRUPTED',cross_host_protocol='stopped on unrelated Cabbage CPU conflict; no complete PASS',cross_host_stop=stop,linger_enabled=False,production_launched=False,production_claim_created=False)
 else:
  x['admission_gates']['cross_host_protocol']='interrupted on CPU conflict; fresh versioned probe required'
  x['admission_gates']['console_independent_user_services']='Cabbage Linger=no; enable and verify at authorized admission'
  x['launch_design']['user_linger']='Required before launch: authorized loginctl enable-linger pnord; no setting was changed by preparation.'
 p.write_text(json.dumps(x,indent=2)+'\n')
shared=Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk/readiness-handoff')
for name in ('CABBAGE_READINESS.json','LAUNCH-INTENT.json'):shutil.copyfile(r/name,shared/name)
for name in ('runtime-acceptance-results.json','nfs-acceptance-results.json','runtime-preparation.json'):shutil.copyfile(r/name,shared/name)
shutil.copyfile(prior/'cross-host-probe-failure.json',shared/'cross-host-probe-failure.json')
print('Updated local and shared handoff: cross-host gate incomplete, no launch. Manifest remains',json.load(open(r/'runtime-preparation.json'))['manifest_sha256'])
