from pathlib import Path
import hashlib,json,shutil
r=Path(__file__).resolve().parent
package=r/'ada-admission-package'
shared=Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/compute-Ija5nMHk/readiness-handoff')
dest=shared/'probe-v2-package';dest.mkdir(mode=0o700,exist_ok=False)
for name in ('ada_export_store.py','admission-plan.json'):shutil.copyfile(package/name,dest/name)
s=(package/'protocol_probe.py').read_text();old="ROOT=BASE/'TEST_ONLY_cabbage_admission_20261108'";assert s.count(old)==1
s=s.replace(old,old+"/'probe-v2-Ija5nMHk'")
assert not Path('/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/probe-v2-Ija5nMHk').exists()
(dest/'protocol_probe.py').write_text(s)
meta=dict(status='PREPARED_NOT_EXECUTED',TEST_ONLY=True,production_coverage=False,root='/mnt/nfs_share/TEST_ONLY_cabbage_admission_20261108/probe-v2-Ija5nMHk',only_script_change='ROOT moves to a fresh child namespace; actual role/adapter/mount/protocol checks unchanged.',source_adapter_sha256=hashlib.sha256((dest/'ada_export_store.py').read_bytes()).hexdigest(),commands=dict(ada='python3 -B '+str(dest/'protocol_probe.py')+' ada',cabbage='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python -B '+str(dest/'protocol_probe.py')+' cabbage'),files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file()})
(dest/'PREPARED.json').write_text(json.dumps(meta,indent=2)+'\n')
shutil.copytree(dest,r/'probe-v2-package')
print('Fresh cross-host probe prepared but not run:',dest)
