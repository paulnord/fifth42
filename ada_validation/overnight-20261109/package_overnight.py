"""Package the tested continuation and verified peer snapshots; stage Git text."""
from datetime import datetime,timezone
import hashlib,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
BUNDLE=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/overnight-r1-20261109')
PREFIX='ada_validation/overnight-20261109/'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(path,row):path.write_text(json.dumps(row,indent=2)+'\n')
def main():
    cfg=json.loads((W/'config.json').read_bytes());mf=json.loads((W/'release-manifest.json').read_bytes())
    for name,h in mf['files'].items():assert sha((W/name).read_bytes())==h,name
    assert all(json.loads((ROOT/n).read_bytes())['status']=='passed' for n in ['unit-validation.json','gpu-validation.json','runtime-validation.json'])
    files={}
    def add(path):
        p=Path(path);name=str(p.relative_to(ROOT));files[name]=sha(p.read_bytes())
    for name in list(mf['files'])+['release-manifest.json','config.json','base-config.json','origin-claim.json','parent-audit.json','final-coverage.json','preparation-report.json']:add(W/name)
    names=['README.txt','configure.py','seal_parent.py','validate_sources.py','validate_runtime.py','validate_restart_runtime.py','test_scheduling.py','test_buffering.py','test_restart_guards.py','test_reporting_relay.py','prepare_launch.py','prepare_reporting.py','collector.py','publish_buffered.py','peer_reporting_relay.py','start_production.py','package_overnight.py','unit-validation.json','gpu-validation.json','runtime-validation.json','configuration-state.json','READY.json','parent-audit.json','sealed-parent.json','final-parent-audit.json','buffering-tests.log','scheduling-tests.log','reservation-retry-tests.log','coordinator-tests.log','reporting-relay-tests.log','production-admission-snapshots.json']
    for name in names:add(ROOT/name)
    for folder in ['runtime','evidence','peer-bundles']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:add(p)
    BUNDLE.mkdir(mode=0o700,parents=True,exist_ok=False)
    archive_manifest=dict(schema='fifth42-source-archive-v1',created_utc=datetime.now(timezone.utc).isoformat(),status='verified',runtime_manifest_sha256=cfg['manifest_sha256'],config_sha256=sha((W/'config.json').read_bytes()),files=dict(sorted(files.items())))
    write(BUNDLE/'SOURCE_MANIFEST.json',archive_manifest)
    with tarfile.open(BUNDLE/'source.tar.gz','w:gz') as archive:
        for name in sorted(files):archive.add(ROOT/name,arcname=name,recursive=False)
    with tarfile.open(BUNDLE/'source.tar.gz','r:gz') as archive:
        assert {m.name for m in archive.getmembers()}==set(files)
        for member in archive.getmembers():assert member.isfile() and sha(archive.extractfile(member).read())==files[member.name]
    known={}
    for folder in ['ada-buffered-release-20261109','ada-group4-20261109','ada-wide-group-tests-20261109']:
        entries=json.loads((Path('/home/pnord')/folder/'github-tree-payload.json').read_bytes())
        for e in entries:
            if 'content' in e:
                raw=e['content'].encode();known[sha(raw)]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    entries=[];public_files={}
    for name in sorted(files):
        if 'bin' in Path(name).parts:continue
        raw=(ROOT/name).read_bytes()
        try:content=raw.decode('utf-8')
        except UnicodeDecodeError:continue
        if '\0' in content:continue
        e=dict(path=PREFIX+name,mode='100644',type='blob')
        if sha(raw) in known:e['sha']=known[sha(raw)]
        else:e['content']=content
        entries.append(e);public_files[name]=sha(raw)
    index=dict(status='verified_source_index',runtime_manifest_sha256=cfg['manifest_sha256'],config_sha256=archive_manifest['config_sha256'],files=public_files,binaries='Excluded from Git; byte hashes retained in runtime manifests, native binaries included in the fully verified NFS archive.')
    entries.append(dict(path=PREFIX+'SOURCE_MANIFEST.json',mode='100644',type='blob',content=json.dumps(index,indent=2)+'\n'))
    write(ROOT/'github-tree-payload.json',entries);raw=json.dumps(entries,indent=2)+'\n'
    chunks=ROOT/'github-chunks';chunks.mkdir(mode=0o700)
    parts=[raw[i:i+20000] for i in range(0,len(raw),20000)]
    for i,part in enumerate(parts):write(chunks/(str(i)+'.json'),dict(part=part))
    state=dict(status='archive_verified_awaiting_github',bundle=str(BUNDLE),members=len(files),git_entries=len(entries),git_chunks=len(parts),git_payload_bytes=len(raw),source_archive_sha256=sha((BUNDLE/'source.tar.gz').read_bytes()))
    write(ROOT/'archive-state.json',state);print(json.dumps(state,indent=2))
if __name__=='__main__':main()
