"""Archive tested sources/results and stage Git objects without native binaries."""
from datetime import datetime,timezone
import hashlib,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
BUNDLE=Path('/mnt/nfs_share/fifth42-integration-20261109/combined/wide-groups-r1')
PREFIX='ada_validation/wide-groups-20261109/'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(path,row):path.write_text(json.dumps(row,indent=2)+'\n')
def main():
    result=json.loads((ROOT/'results.json').read_bytes());assert result['status']=='passed' and result['production_unchanged']
    source=json.loads((ROOT/'experiment-manifest.json').read_bytes())
    files={}
    for name,expected in source['worker_files'].items():
        raw=(W/name).read_bytes();assert sha(raw)==expected,name
        files['worker/'+name]=sha(raw)
    names=['README.txt','HANDOFF_CABBAGE.txt','wider-groups.patch','run_comparison.py','trial_wide_groups.py','resource_helper.py','package_results.py','baseline-manifest.json','experiment-manifest.json','results.json','preflight.json','controls.json','production-stop-status.json','progress.json']
    for name in names:files[name]=sha((ROOT/name).read_bytes())
    for path in (ROOT/'logs').iterdir():
        if path.is_file():files[str(path.relative_to(ROOT))]=sha(path.read_bytes())
    BUNDLE.mkdir(mode=0o700,parents=True,exist_ok=False)
    manifest=dict(schema='fifth42-source-archive-v1',status='verified',created_utc=datetime.now(timezone.utc).isoformat(),baseline_manifest_sha256=source['baseline_manifest_sha256'],experiment_manifest_sha256=sha((ROOT/'experiment-manifest.json').read_bytes()),TEST_ONLY=True,files=dict(sorted(files.items())))
    write(BUNDLE/'SOURCE_MANIFEST.json',manifest)
    with tarfile.open(BUNDLE/'source.tar.gz','w:gz') as archive:
        for name in sorted(files):archive.add(ROOT/name,arcname=name,recursive=False)
    with tarfile.open(BUNDLE/'source.tar.gz','r:gz') as archive:
        assert {m.name for m in archive.getmembers()}==set(files)
        for member in archive.getmembers():assert member.isfile() and sha(archive.extractfile(member).read())==files[member.name]
    entries=[];index={}
    for name in sorted(files):
        if 'bin' in Path(name).parts:continue
        raw=(ROOT/name).read_bytes()
        try:content=raw.decode('utf-8')
        except UnicodeDecodeError:continue
        entry=dict(path=PREFIX+name,mode='100644',type='blob')
        # All unchanged worker text objects are already in the parent commit.
        rel=name.removeprefix('worker/')
        if name.startswith('worker/') and rel not in source['source_delta']:
            entry['sha']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        else:entry['content']=content
        entries.append(entry);index[name]=sha(raw)
    public=dict(status='verified_source_index',TEST_ONLY=True,baseline_manifest_sha256=source['baseline_manifest_sha256'],experiment_manifest_sha256=manifest['experiment_manifest_sha256'],files=index,binaries='Hashes retained in experiment-manifest.json; native binaries included in the NFS archive.')
    entries.append(dict(path=PREFIX+'SOURCE_MANIFEST.json',mode='100644',type='blob',content=json.dumps(public,indent=2)+'\n'))
    write(ROOT/'github-tree-payload.json',entries)
    raw=json.dumps(entries,indent=2)+'\n';chunks=ROOT/'github-chunks';chunks.mkdir(mode=0o700)
    parts=[raw[i:i+20000] for i in range(0,len(raw),20000)]
    for i,part in enumerate(parts):write(chunks/(str(i)+'.json'),dict(part=part))
    report=dict(status='archive_verified_awaiting_github',bundle=str(BUNDLE),archive_members=len(files),git_entries=len(entries),git_chunks=len(parts),source_archive_sha256=sha((BUNDLE/'source.tar.gz').read_bytes()))
    write(ROOT/'archive-state.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
