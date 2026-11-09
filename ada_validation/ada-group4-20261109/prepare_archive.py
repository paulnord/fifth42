"""Package a complete verified revision and prepare Git entries without binaries."""
from datetime import datetime,timezone
import hashlib,json,shutil,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; W=ROOT/'worker'
BUNDLE=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/ada-group4-r1')
PREFIX='ada_validation/ada-group4-20261109/'
OLD_PREFIX='ada_validation/buffered-20261109/'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def write(path,row):path.write_text(json.dumps(row,indent=2)+'\n')
def main():
    cfg=json.loads((W/'config.json').read_bytes());mf=json.loads((W/'release-manifest.json').read_bytes())
    for name,expected in mf['files'].items():assert digest((W/name).read_bytes())==expected,name
    assert all(json.loads((ROOT/n).read_bytes())['status']=='passed' for n in ('unit-validation.json','gpu-validation.json','runtime-validation.json','holdout-results.json'))
    stage=ROOT/'archive-stage';stage.mkdir(mode=0o700,exist_ok=False)
    files={}
    def copy(source,name):
        target=stage/name;target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        shutil.copy2(source,target);files[name]=digest(target.read_bytes())
    for name in list(mf['files'])+['release-manifest.json','config.json','base-config.json','origin-claim.json','parent-audit.json','final-coverage.json','preparation-report.json']:
        copy(W/name,'worker/'+name)
    names=['README.md','configure.py','seal_parent.py','trial_groups.py','benchmark_groups.py','benchmark_groups_holdout.py','check_nonempty_groups.py','test_buffering.py','test_scheduling.py','validate_sources.py','validate_runtime.py','finish_deadline_validation.py','prepare_launch.py','prepare_reporting.py','start_production.py','prepare_archive.py','collector.py','publish_buffered.py','experiment-manifest.json','configuration-state.json','sealed-parent.json','final-parent-audit.json','selection-results.json','holdout-results.json','unit-validation.json','gpu-validation.json','runtime-validation.json','READY.json','buffering-tests.log','scheduling-tests.log','coordinator-tests.log']
    for name in names:copy(ROOT/name,name)
    for folder in ['runtime','benchmarks','benchmarks-holdout']:
        for path in sorted((ROOT/folder).rglob('*')):
            if path.is_file() and path.name not in ('worker.stdout.log','service.stdout.log'):
                copy(path,str(path.relative_to(ROOT)))
    archive_source_manifest=dict(schema='fifth42-source-archive-v1',status='verified',created_utc=datetime.now(timezone.utc).isoformat(),runtime_manifest_sha256=cfg['manifest_sha256'],config_sha256=digest((W/'config.json').read_bytes()),files=dict(sorted(files.items())))
    BUNDLE.mkdir(mode=0o700,parents=True,exist_ok=False)
    write(BUNDLE/'SOURCE_MANIFEST.json',archive_source_manifest)
    with tarfile.open(BUNDLE/'source.tar.gz','w:gz') as archive:
        for name in sorted(files):archive.add(stage/name,arcname=name,recursive=False)
    # Verify every member from a fresh decompression before admitting the bundle.
    with tarfile.open(BUNDLE/'source.tar.gz','r:gz') as archive:
        members=archive.getmembers();assert {m.name for m in members}==set(files)
        for member in members:assert member.isfile() and digest(archive.extractfile(member).read())==files[member.name]
    old_entries=json.loads(Path('/home/pnord/ada-buffered-release-20261109/github-tree-payload.json').read_bytes())
    old_blobs={}
    for entry in old_entries:
        if 'content' in entry:
            raw=entry['content'].encode();sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            old_blobs[digest(raw)]=sha
    entries=[];git_files={}
    for name in sorted(files):
        if 'bin' in Path(name).parts:continue
        raw=(stage/name).read_bytes()
        try:content=raw.decode('utf-8')
        except UnicodeDecodeError:continue
        entry=dict(path=PREFIX+name,mode='100644',type='blob')
        if digest(raw) in old_blobs:entry['sha']=old_blobs[digest(raw)]
        else:entry['content']=content
        entries.append(entry);git_files[name]=digest(raw)
    index=dict(status='verified_source_index',runtime_manifest_sha256=cfg['manifest_sha256'],config_sha256=digest((W/'config.json').read_bytes()),files=git_files,binaries='Omitted from Git; hashes in worker/release-manifest.json and native binaries included in the NFS source archive.')
    write(ROOT/'GITHUB_SOURCE_MANIFEST.json',index)
    entries.append(dict(path=PREFIX+'SOURCE_MANIFEST.json',mode='100644',type='blob',content=json.dumps(index,indent=2)+'\n'))
    write(ROOT/'github-tree-payload.json',entries)
    write(ROOT/'archive-state.json',dict(status='archive_verified_awaiting_github',bundle=str(BUNDLE),archive_members=len(files),git_files=len(entries),source_archive_sha256=digest((BUNDLE/'source.tar.gz').read_bytes())))
    print(json.dumps(json.loads((ROOT/'archive-state.json').read_bytes()),indent=2))
if __name__=='__main__':main()
