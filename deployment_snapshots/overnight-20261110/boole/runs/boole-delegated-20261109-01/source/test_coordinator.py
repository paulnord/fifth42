"""TEST_ONLY parent lease and heartbeat fixture; never handles production grants."""
import argparse,ctypes,hashlib,json,os,signal,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'worker'))
import ada_export_store
from durable_mirror import atomic

def main():
 p=argparse.ArgumentParser();p.add_argument('--grant',type=Path,required=True);a=p.parse_args()
 raw=a.grant.read_bytes();g=json.loads(raw)
 assert g['TEST_ONLY'] is True and Path(g['parent_ledger']).is_relative_to(Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/suballocation-tests/boole-local-delegated-20261109'))
 stop=[False];signal.signal(signal.SIGTERM,lambda *_:stop.__setitem__(0,True))
 libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(1,signal.SIGKILL)==0
 if os.getppid()==1:raise RuntimeError('Fixture parent exited')
 store=ada_export_store.Store(g['parent_ledger'])
 with store.locked(store.root/'jobs'/g['parent_job']/'journal.jsonl'):
  while not stop[0] and time.time()<g['stop_epoch']+5:
   atomic(Path(g['child_ledger'])/'coordinator-state.json',dict(TEST_ONLY=True,status='active',grant_sha256=hashlib.sha256(raw).hexdigest(),stop_epoch=g['stop_epoch'],retained_range_end=g['assignments']['ada'][1],updated_epoch=time.time()))
   if not getattr(main,'ready',False):print('ready',flush=True);main.ready=True
   time.sleep(.2)
if __name__=='__main__':main()
