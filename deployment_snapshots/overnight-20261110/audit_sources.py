"""Capture and verify immutable production handoffs without touching live jobs."""
from datetime import datetime, timezone
import hashlib, io, json, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
KNOWN=set(json.loads(Path('/home/pnord/.cache/fifth42-github-known-blobs-20261110.json').read_bytes()))
FILES={}; ARCHIVES=[]; SKIPPED=[]
def sha(raw): return hashlib.sha256(raw).hexdigest()
def gitsha(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def put(name,raw):
    assert name not in FILES or FILES[name]==raw, name
    FILES[name]=raw
def archive(path,prefix,expected=None,manifest=None):
    raw=path.read_bytes()
    if expected: assert sha(raw)==expected, str(path)
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
        members={m.name:m for m in tar.getmembers() if m.isfile()}
        data={n:tar.extractfile(m).read() for n,m in members.items()}
    if manifest:
        for n,h in manifest.items(): assert n in data and sha(data[n])==h, str(path)+' '+n
    for n,blob in data.items():
        p=Path(n); assert not p.is_absolute() and '..' not in p.parts
        if 'bin' in p.parts:
            SKIPPED.append(dict(path=prefix+n,sha256=sha(blob),reason='native executable retained in verified NFS archive')); continue
        try: blob.decode('utf-8')
        except UnicodeDecodeError:
            SKIPPED.append(dict(path=prefix+n,sha256=sha(blob),reason='binary')); continue
        if b'\0' in blob:
            SKIPPED.append(dict(path=prefix+n,sha256=sha(blob),reason='binary')); continue
        put(prefix+n,blob)
    ARCHIVES.append(dict(path=str(path),prefix=prefix,sha256=sha(raw),members=len(data),manifest_files_checked=len(manifest or {})))
    return data
def handoff(host,path,manifest_name,expected_key):
    ready=json.loads((path/'READY.json').read_bytes());manifest=json.loads((path/manifest_name).read_bytes())
    if host=='boole': expected=ready[expected_key]
    else: expected=ready['artifacts'][expected_key]
    prefix=host+'/handoff/'
    archive(path/'source.tar.gz',prefix+'source/',expected,manifest['files'])
    for p in path.iterdir():
        if p.is_file() and p.suffix not in ('.gz','.tar'):
            put(prefix+p.name,p.read_bytes())
    if (path/'results').is_dir():
        for p in (path/'results').glob('*.json'):put(prefix+'results/'+p.name,p.read_bytes())
def stages(host,share):
    for folder in sorted((share/'runs').iterdir()):
        if not folder.is_dir() or not (folder/'source.tar.gz').exists():continue
        mf=json.loads((folder/'source-manifest.json').read_bytes())
        prefix=host+'/runs/'+folder.name+'/'
        archive(folder/'source.tar.gz',prefix+'source/',manifest={'worker/'+n:h for n,h in mf['files'].items()})
        for p in folder.iterdir():
            if p.is_file() and p.suffix not in ('.gz','.tar'):put(prefix+'evidence/'+p.name,p.read_bytes())
    active=(share/'active-publication-spec.json').read_bytes()
    spec=json.loads(active); folder=share/'runs'/spec['run_id']
    assert sha((folder/'source.tar.gz').read_bytes())==spec['source_archive_sha256']
    for name,h in spec['evidence_sha256'].items(): assert sha((folder/name).read_bytes())==h
    put(host+'/active-publication-spec.json',active)
def main():
    handoff('boole',Path('/mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/delegated-r1'),'source-manifest.json','source_bundle_sha256')
    handoff('cabbage',Path('/mnt/nfs_share/fifth42-integration-20261109/extended/cabbage/20261109-r1'),'controller-manifest.json','source.tar.gz')
    for host in ('boole','cabbage'):
        share=Path('/mnt/nfs_share/'+('boole-delegated' if host=='boole' else 'cabbage-extended')+'-publishing-20261109')
        stages(host,share)
    missing=[n for n,b in FILES.items() if gitsha(b) not in KNOWN]
    report=dict(status='passed',captured_utc=datetime.now(timezone.utc).isoformat(),verified_archives=ARCHIVES,
                text_files=len(FILES),text_bytes=sum(map(len,FILES.values())),new_blob_paths=missing,
                existing_github_blobs=len(FILES)-len(missing),excluded_binary_files=SKIPPED,
                scope='Exact Boole delegated queue plus Cabbage extension and every currently archived successor; production untouched')
    (ROOT/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    cached=ROOT/'captured';cached.mkdir(exist_ok=True)
    for n,b in FILES.items():
        p=cached/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    print(json.dumps(dict(status=report['status'],archives=len(ARCHIVES),text_files=len(FILES),text_bytes=report['text_bytes'],new_blobs=len(missing),new_code=[n for n in missing if n.endswith('.py')],binary_files=len(SKIPPED)),indent=2))
if __name__=='__main__':main()
