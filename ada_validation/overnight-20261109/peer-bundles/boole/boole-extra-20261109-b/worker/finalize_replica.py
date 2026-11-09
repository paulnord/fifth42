"""Finish replicating a stopped search; never starts or resumes computation."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import time

from durable_mirror import PrefixMirror,atomic


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--config-sha256',required=True)
    parser.add_argument('--wait',action='store_true')
    args=parser.parse_args();raw=args.config.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==args.config_sha256,'Frozen cleanup config changed'
    cfg=json.loads(raw);source=Path(cfg['output'])
    fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=cfg['manifest_sha256'],config=cfg),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    identity=dict(trial=cfg['run_id'],source_identity=fingerprint)
    until=cfg['stop_epoch']+1800 if args.wait else time.time()+120
    while time.time()<until:
        try:
            state=json.loads((source/'status.json').read_bytes())
            if state['status'] not in ('stopped','failed','completed_test'):
                if not args.wait:raise RuntimeError('Compute owner is still active')
                time.sleep(2);continue
            with (source/'writer.lock').open('r+b') as owner:
                fcntl.flock(owner,fcntl.LOCK_EX|fcntl.LOCK_NB)
                mirror=PrefixMirror(source,cfg['replica_output'],identity)
                try:receipt=mirror.sync()
                finally:mirror.close()
            assert receipt is not None
            assert (Path(cfg['replica_output'])/'checkpoint.json').read_bytes()==(source/'checkpoint.json').read_bytes(),'Final checkpoint moved during cleanup'
            atomic(source/'final-replica.json',dict(status='verified',receipt=receipt,finished_epoch=time.time(),compute_started=False))
            print(json.dumps(dict(status='verified',run_id=cfg['run_id'],next_patch=receipt['next_patch'],committed_bytes=receipt['committed_bytes'])),flush=True)
            return 0
        except (FileNotFoundError,BlockingIOError):
            if not args.wait:raise
            time.sleep(2)
    raise TimeoutError('Final replication did not finish in its cleanup window')

if __name__=='__main__':raise SystemExit(main())
