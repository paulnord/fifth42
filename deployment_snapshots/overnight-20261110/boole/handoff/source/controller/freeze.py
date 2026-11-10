"""Freeze the 67 existing Ada child claims; never reserve or rewrite ownership."""
import hashlib,json,os,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;T=Path('/home/pnord/boole-delegated-template-20261109');sys.path[:0]=[str(T/'worker'),str(T/'worker/source/lattice_gpu')]
import policy,ada_export_store,bulk_data_store
from durable_mirror import atomic
GRANT=Path('/mnt/nfs_share/fifth42-shared-20261107/suballocations/ada-boole-20261109-r1/GRANT.json')

def main():
 os.umask(0o077);g=json.loads(GRANT.read_bytes());sha=policy.digest(GRANT)
 assert sha=='7c8422f5e9086519db3bc8ad2e8eeab8d7d1d60706f9b327766ba0a069c6a389'
 allocations=json.loads((GRANT.parent/'BOOLE_ALLOCATIONS.json').read_bytes())['allocations'];assert len(allocations)==67
 store=ada_export_store.Store(GRANT.parent);until=time.monotonic()+2
 while True:
  try:
   with store.locked(store.root/'reservations.jsonl') as fd:claims={r['job']:r for r in store.claims(fd)}
   break
  except ada_export_store.Busy:
   assert time.monotonic()<until;time.sleep(.02)
 shutil.copy2(T/'worker/bin/gmp_reference',T/'worker/bin/scaling_gmp')
 stages=[];cursor=7000000000
 for a in allocations:
  claim=claims[a['job']];assert claim['sha256']==a['claim_sha256'] and claim['identity']==sha and claim['first']==a['first']==cursor and claim['last']==a['last']
  assert 0<a['last']-a['first']<=64000000;cursor=a['last']
  name=a['job'];root=Path('/home/pnord')/name;shutil.copytree(T,root,ignore=shutil.ignore_patterns('__pycache__'));w=root/'worker'
  shutil.copy2(w/'origin-claim.json',w/'baseline-origin-claim.json');atomic(w/'child-claim.json',claim);shutil.copy2(GRANT,w/'protected-grant.json')
  c=json.loads((w/'production-config.json').read_bytes())
  local=policy.LOCAL/name/name;local.mkdir(mode=0o700,parents=True,exist_ok=False);replica=policy.BULK/'runs'/name/name/'run';assert not replica.exists()
  c.update(run_id=name,allocation_role='boole',suballocation_grant_file=str(GRANT),suballocation_grant_sha256=sha,
   initial_patch=a['first'],range_end=a['last'],ledger_root=str(store.root),ledger_job=name,ledger_device=store.device,ledger_claim_sha256=claim['sha256'],
   reservation_initial_patch=claim['first'],reservation_manifest_sha256=claim['identity'],origin_claim_file=str(w/'child-claim.json'),origin_claim_file_sha256=policy.digest(w/'child-claim.json'),
   manifest=str(w/'release-manifest.json'),parent_audit_file=str(w/'parent-audit.json'),parent_lineage_file=str(w/'parent-lineage.json'),coverage_file=str(w/'final-coverage.json'),
   output=str(local/'run'),replica_output=str(replica),local_data_device=local.stat().st_dev,data_device=bulk_data_store.verify_share(replica),service_name=name+'.service',deadline_service_name=name+'-deadline.service',
   authorization='User authorized continued production until 2026-11-10 17:00 Central and appending all 67 Ada-protected child claims; no automatic crash resume.')
  coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=c['initial_patch'],parent_checkpoint_sha256=c['parent_checkpoint_sha256'],parent_journal_sha256=c['parent_journal_sha256'],covered_intervals=[],completed_bound=None,scope='Fresh reserved interval; parent history and reservations are not imported as completed coverage.')
  atomic(w/'final-coverage.json',coverage);c['coverage_sha256']=policy.digest(w/'final-coverage.json')
  files={str(p.relative_to(w)):policy.digest(p) for p in sorted(w.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ('release-manifest.json','base-config.json','production-config.json')}
  code={name:value for name,value in files.items() if Path(name).suffix in ('.py','.cpp','.cu','.hpp','.h') or name.startswith('bin/')}
  manifest=dict(host='boole',provenance='Unchanged tested Boole overnight mathematics/native binaries; exact Ada supplied suballocation guard; fresh existing child claim.',
   upstream_suballocation_commit='3a17f457780c87987feec1586688b24854666ecf',baseline_manifest_sha256='4b5da65fe1219caf4e2d4ef971a2075f7e824e671f3458b8210efb8c146faf3c',
   files=files,external_files={str(p):policy.digest(p) for p in sorted(root.glob('*.py'))},code_equivalence_sha256=hashlib.sha256(policy.stable(code).encode()).hexdigest())
  atomic(w/'release-manifest.json',manifest);c['manifest_sha256']=policy.digest(w/'release-manifest.json');atomic(w/'base-config.json',c);atomic(w/'production-config.json',c)
  # Isolated interpreter prevents module-cache reuse between frozen roots.
  import subprocess
  subprocess.run([sys.executable,'-B','-c',"import sys;sys.path[:0]=sys.argv[1:3];import policy;policy.load_config(sys.argv[3])",str(w),str(w/'source/lattice_gpu'),str(w/'production-config.json')],check=True)
  rec=dict(root=str(root),config=str(w/'production-config.json'),config_sha256=policy.digest(w/'production-config.json'),manifest_sha256=c['manifest_sha256'],first=a['first'],last=a['last'],service=c['service_name'],ledger_job=name,claim_sha256=claim['sha256'],code_equivalence_sha256=manifest['code_equivalence_sha256'])
  atomic(root/'FROZEN.json',dict(status='frozen_awaiting_local_gpu_validation',**rec));stages.append(rec)
 assert cursor==11250000001 and len({r['code_equivalence_sha256'] for r in stages})==1
 atomic(ROOT/'stages.json',dict(status='frozen',stages=stages,grant_sha256=sha,total_cells=4250000001))
 print(json.dumps(dict(status='frozen',stages=len(stages),cells=4250000001)),flush=True)
if __name__=='__main__':main()
