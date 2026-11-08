from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,tarfile,subprocess,os,shutil
r=Path(__file__).resolve().parent;w=r/'cabbage-runtime'
p=w/'cabbage-release-manifest.json';data=p.read_bytes();m=json.loads(data)
for name,h in m['files'].items():
 f=w/name;assert f.is_file() and not f.is_symlink() and hashlib.sha256(f.read_bytes()).hexdigest()==h,name
meta=json.loads((r/'runtime-acceptance-results.json').read_text());assert meta['manifest_sha256']==hashlib.sha256(data).hexdigest()
sha=meta['manifest_sha256']
assert meta['adapter_sha256']==json.loads((r/'ada-admission-package/admission-plan.json').read_text())['candidate_adapter_sha256']
# A source/binary review archive of precisely the tested files, no journals/configs/leases.
archive=r/'cabbage-candidate-review-20261108.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
 for name in sorted(m['files']):tar.add(w/name,arcname='cabbage-candidate/'+name,recursive=False)
 tar.add(p,arcname='cabbage-candidate/cabbage-release-manifest.json',recursive=False)
with tarfile.open(archive) as tar:
 for name,h in m['files'].items():assert hashlib.sha256(tar.extractfile('cabbage-candidate/'+name).read()).hexdigest()==h
archive_sha=hashlib.sha256(archive.read_bytes()).hexdigest()
(r/'CANDIDATE_SHA256SUMS').write_text(archive_sha+'  '+archive.name+'\n')
intent=dict(status='REVIEW_ONLY_NOT_AUTHORIZED_TO_LAUNCH',host='cabbage',runtime_path=str(w),manifest_sha256=sha,job_id_proposal='cabbage-saved-root-20261108',interval=[2250000000,3000000000],ledger_root='/mnt/nfs_share/fifth42-shared-20261107',production_claim_sha256=None,production_claim_created=False,production_launched=False,workers=16,physical_cpus=list(range(16)),backend='gpu',nice=19,journal_cap_bytes=2*1024**3,minimum_shared_free_bytes=8*1024**3,stop_local='2026-11-09T09:00:00-06:00',stop_epoch=1794236400,cleanup_timer_epoch=1794236390,automatic_restart=False,automatic_resume=False,publication_directory='cabbage_validation/production-20261108',publication_interval_seconds=900,admission_gates=dict(local_compute='passed',actual_nfs='passed',runtime_stops_and_cleanup='passed',cross_host_protocol='pending Ada peer',current_disjoint_ledger_and_disk_refresh='pending final admission',ada_hosted_publisher='pending Ada owner',owner_launch_authorization='not granted'),artifact=dict(path=str(archive),sha256=archive_sha,bytes=archive.stat().st_size),launch_design=dict(service='New systemd user service; Type=exec, Restart=no, KillMode=control-group, Nice=19, CPUAffinity=0-15, TimeoutStopSec=8s; RuntimeMaxSec computed from the fixed deadline with cleanup margin.',worker_command=[str(Path('/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python')),'-B',str(w/'cabbage_supervisor.py'),'--config','FINAL_AUTHORIZED_CONFIG.json'],timer='Independent one-shot user timer to stop the new service at 2026-11-09 14:59:50 UTC. No existing service is stopped or changed.',prelaunch='Reverify manifest and physical topology, idle CPU/GPU, actual adapter/mount/private ownership, both cross-host PASS files, refreshed disjoint common-ledger claim and aggregate disk headroom. Then freeze a fresh config and collector identity.',rollback='On failure stop only the new Cabbage service and its owned processes; preserve its journal and source identity. Do not resume an old journal with changed code or erase durable reservation history. No automatic restart.'),limitations=['The snapshot range proposal is not a current production allocation or storage reservation.','The staged source identity is tested; the final production config and its claim/collector fingerprint are not yet created.','Cross-host protocol and Ada publisher require the Ada-side owner; no remote Ada commands were run.'])
(r/'LAUNCH-INTENT.json').write_text(json.dumps(intent,indent=2)+'\n')
report=dict(status='LOCAL_ACCEPTANCE_PASSED_ADMISSION_PENDING',host='cabbage',runtime_manifest_sha256=sha,runtime_files_verified=len(m['files']),archive_sha256=archive_sha,source_adapter_sha256=meta['adapter_sha256'],range=meta['proposed_interval'],journal_cap_bytes=meta['journal_cap_bytes'],actual_worker_acceptance=meta,remaining_gpu=json.loads((r/'remaining-gpu/results.json').read_text()),nfs_acceptance=json.loads((r/'nfs-acceptance-results.json').read_text()),production_claim_created=False,production_launched=False,production_coverage=False,cross_host_protocol='pending',publisher='pending Ada coordination')
(r/'CABBAGE_READINESS.json').write_text(json.dumps(report,indent=2)+'\n')
shared=Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk/readiness-handoff')
shared.mkdir(mode=0o700,exist_ok=False)
for name in ('CABBAGE_READINESS.json','LAUNCH-INTENT.json','CANDIDATE_SHA256SUMS',archive.name):shutil.copyfile(r/name,shared/name)
print(json.dumps(dict(manifest_sha256=sha,archive_sha256=archive_sha,shared_handoff=str(shared),status=report['status']),indent=2))
