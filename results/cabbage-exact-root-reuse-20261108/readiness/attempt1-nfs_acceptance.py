import hashlib,json,os,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
review=root/'review-bundle'
sys.path.insert(0,str(review));import cabbage_export_store as w
share=Path((root/'nfs-root.txt').read_text().strip())
assert share.parent==Path('/mnt/nfs_share') and share.name=='TEST_ONLY_cabbage_saved_root_20261108_Ija5nMHk'
fs=json.loads(subprocess.check_output(['findmnt','--json','--target','/mnt/nfs_share','--output','TARGET,SOURCE,FSTYPE,OPTIONS'],text=True,timeout=5))['filesystems'][0]
assert fs['source']=='ada:/mnt/nfs_share' and fs['fstype']=='nfs4'
assert not set(fs['options'].split(',')) & {'nolock','local_lock=all','local_lock=posix'}
os.mkdir(share,0o700) # Requires a NEW namespace; never reuse old acceptance files.
(share/'TEST_ONLY.json').write_text(json.dumps(dict(TEST_ONLY=True,production_coverage=False,host='cabbage',purpose='saved-root isolated storage acceptance',manifest_sha256=hashlib.sha256((review/'STAGED-MANIFEST.json').read_bytes()).hexdigest()),indent=2)+'\n')
for variant in ('baseline','candidate'):
 subprocess.run([sys.executable,str(root/'nfs_variant.py'),variant],check=True,timeout=90,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'))
a=json.loads((root/'nfs-baseline-results.json').read_text());b=json.loads((root/'nfs-candidate-results.json').read_text())
assert a['controls']==b['controls'],'NFS baseline/candidate nonempty controls differ'
assert a['signatures']==b['signatures'],'NFS baseline/candidate exact counts/geometry/hits differ'
identity=a['manifest_sha256'];first=3000000000
s=w.Store(share/'locking');r=s.reserve('one',first,first+256,identity)
assert s.reserve('one',first,first+256,identity)==r
s.reserve('adjacent',first+256,first+512,identity)
try:s.reserve('overlap',first+1,first+2,identity);raise AssertionError('Overlap accepted')
except w.Conflict:pass
try:s.reserve('one',first,first+256,'0'*64);raise AssertionError('Changed reservation identity accepted')
except w.Conflict:pass
# Actual server-coherent POSIX locks, using another process on Cabbage.
code="""import sys;sys.path.insert(0,sys.argv[1]);import cabbage_export_store as w
s=w.Store(sys.argv[2])
try:s.claim('one')
except w.Busy:print('busy');raise SystemExit(0)
raise RuntimeError('Expected lock exclusion')
"""
lock=s.root/'reservations.jsonl';inode=lock.stat().st_ino
with s.locked(lock):
 p=subprocess.run([sys.executable,'-c',code,str(review),str(s.root)],capture_output=True,text=True,timeout=10,check=True)
 assert p.stdout.strip()=='busy'
assert lock.stat().st_ino==inode
# Kill a test-only lock holder, then verify release without replacing the inode.
code="""import sys,time;sys.path.insert(0,sys.argv[1]);import cabbage_export_store as w
s=w.Store(sys.argv[2])
with s.locked(s.root/'reservations.jsonl'):
 print('ready',flush=True);time.sleep(30)
"""
p=subprocess.Popen([sys.executable,'-c',code,str(review),str(s.root)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
 import selectors
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ)
 assert sel.select(10),'Lock holder readiness timeout'
 assert p.stdout.readline().strip()=='ready'
 try:s.claim('one');raise AssertionError('Duplicate lock acquired')
 except w.Busy:pass
finally:
 p.kill();p.communicate(timeout=5)
with s.locked(lock):pass
assert lock.stat().st_ino==inode
# A local path is rejected by the real verifier, with no local fallback.
wrong=root/'must-not-be-created'
try:w.Store(wrong);raise AssertionError('Local fallback accepted')
except w.Integrity:pass
assert not wrong.exists()
report=dict(status='passed',TEST_ONLY=True,production_coverage=False,namespace=str(share),filesystem=fs,manifest_sha256=identity,baseline_candidate_exact_equal=True,reservation_overlap_rejected=True,reservation_identity_immutable=True,posix_lock_exclusion=True,lock_holder_death_releases_lock=True,stable_inode_preserved=True,local_fallback_rejected=True,storage_adapter_sha256=hashlib.sha256((review/'cabbage_export_store.py').read_bytes()).hexdigest(),actual_cabbage_host_verified=True,guard_substitution=False,limitations=['Single NFS client host; no cross-host failover/reboot tests.','Production shared ledger was never inspected or changed.'])
(root/'nfs-acceptance-results.json').write_text(json.dumps(report,indent=2)+'\n')
print('NFS acceptance passed; baseline/candidate exact records identical; all writes confined to',share,flush=True)
