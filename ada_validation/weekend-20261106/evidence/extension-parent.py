"""Acquire the original parent only after old workers and queues are sealed."""
from pathlib import Path
import argparse
import fcntl
import json
import os
import signal
import time
import allocation_guard as guard

def verify_acknowledgments(grant,folder,expected):
    proofs={}
    for host in ('ada','boole','cabbage'):
        path=Path(folder)/('ACK-'+host+'.json');proof=guard.read(path)
        guard.require(proof.get('host')==host and proof.get('grant_sha256')==expected and proof.get('status')=='ready_for_generation','Host acknowledgment is missing or for another generation: '+host)
        guard.require(proof.get('native_validation')=='passed' and proof.get('new_deadline_timers_prepared') is True,'Host has not validated its new runtime/deadline: '+host)
        validation_path=Path(proof['validation_file']);validation=guard.read(validation_path)
        guard.require(guard.sha(validation_path)==proof['validation_sha256'] and validation.get('status')=='passed' and
                      validation.get('host')==host and validation.get('grant_sha256')==expected and
                      validation.get('stop_epoch')==grant['stop_epoch'] and
                      validation.get('first_middle_last_native_gmp')=='passed' and
                      validation.get('signal_and_deadline_cleanup')=='passed','Host validation does not identify this allocation: '+host)
        if not grant['TEST_ONLY']:
            guard.require(validation.get('native_binaries')==grant['native_binaries'][host],'Native binaries changed: '+host)
        if host in ('ada','boole'):
            guard.require(proof.get('legacy_controller_stopped') is True and proof.get('legacy_stop_intent_persisted') is True and proof.get('worker_leases_released') is True,'Legacy owner can still restart: '+host)
            run=Path(proof['sealed_replica']);raw=(run/'checkpoint.json').read_bytes();cp=json.loads(raw);status=guard.read(run/'status.json')
            guard.require(guard.sha(run/'checkpoint.json')==proof['checkpoint_sha256'] and cp['next_patch']==proof['next_patch'],'Sealed frontier changed: '+host)
            guard.require(status.get('status')=='stopped' and status.get('error') is None,'Predecessor did not stop cleanly: '+host)
            guard.require(status.get('journal_buffer',{}).get('pending_chunks')==0 and status['journal_buffer'].get('pending_bytes')==0,'Predecessor has pending records: '+host)
            receipt=guard.read(run/'replica-state.json')
            guard.require(receipt.get('status')=='verified' and receipt['checkpoint_sha256']==guard.sha(run/'checkpoint.json') and receipt['committed_bytes']==cp['journal_offset'] and receipt['journal_sha256']==cp['journal_sha256'] and receipt['next_patch']==cp['next_patch'],'Final replica mismatch: '+host)
            guard.require((run/'coverage.jsonl').stat().st_size==cp['journal_offset'],'Final replica length mismatch: '+host)
        else:
            guard.require(proof.get('current_owner_completion_required_before_launch') is True,'Cabbage must finish/stop its independent owner before launching')
        proofs[host]=dict(path=str(path),sha256=guard.sha(path),next_patch=proof.get('next_patch'))
    return proofs

class Coordinator:
    def __init__(self,path,expected,test=False):
        self.path=Path(path);self.expected=expected;self.test=test;self.g=guard.load_grant(path,expected,test);self.fd=None
        guard.require(guard.sha(__file__)==self.g['coordinator_source_sha256'],'Coordinator source differs from grant')
        guard.require(guard.sha(guard.__file__)==self.g['guard_source_sha256'],'Allocation guard differs from grant')
    def acquire(self):
        g=self.g;guard.verify_mount(g['child_ledger'],self.test)
        self.proofs=verify_acknowledgments(g,self.path.parent,self.expected)
        parent=guard.claim(g['parent_ledger'],g['parent_job'])
        guard.require((parent['sha256'],parent['first'],parent['last'])==(g['parent_claim_sha256'],g['parent_first'],g['parent_last']),'Original parent reservation changed')
        for row in g['assignments']:
            original=guard.claim(g['child_ledger'],row['job'])
            guard.require((original['sha256'],original['first'],original['last'],original['identity'])==(row['claim_sha256'],row['first'],row['last'],row['claim_identity']),'Original child reservation changed: '+row['job'])
            guard.require(not guard.locked_by_other(Path(g['child_ledger'])/'jobs'/row['job']/'journal.jsonl'),'Legacy child owner remains active: '+row['job'])
        path=Path(g['parent_ledger'])/'jobs'/g['parent_job']/'journal.jsonl'
        self.fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW)
        try:fcntl.lockf(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BaseException:os.close(self.fd);self.fd=None;raise
        self.inode=(os.fstat(self.fd).st_dev,os.fstat(self.fd).st_ino)
        self.heartbeat()
        guard.atomic(self.path.parent/g['active_file'],dict(status='active_allocation_ready',grant_sha256=self.expected,stop_epoch=g['stop_epoch'],acknowledgments=self.proofs,coordinator_pid=os.getpid(),activated_epoch=time.time(),coverage_claimed=False))
    def heartbeat(self):
        g=self.g;guard.require(self.fd is not None and guard.sha(self.path)==self.expected,'Grant changed or parent not acquired')
        guard.require(guard.sha(__file__)==g['coordinator_source_sha256'] and guard.sha(guard.__file__)==g['guard_source_sha256'],'Coordinator source changed')
        stat=(Path(g['parent_ledger'])/'jobs'/g['parent_job']/'journal.jsonl').stat()
        guard.require((stat.st_dev,stat.st_ino)==self.inode,'Stable parent lease inode was replaced')
        # Never reopen the parent lease inode here: closing any such descriptor
        # would release this process's POSIX record lock.
        for proof in self.proofs.values():guard.require(guard.sha(proof['path'])==proof['sha256'],'Accepted host acknowledgment changed')
        guard.atomic(self.path.parent/g['state_file'],dict(status='active',grant_sha256=self.expected,stop_epoch=g['stop_epoch'],coordinator_pid=os.getpid(),updated_epoch=time.time(),TEST_ONLY=self.test))
    def close(self):
        if self.fd is not None:os.close(self.fd);self.fd=None

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--grant',required=True);parser.add_argument('--grant-sha256',required=True);parser.add_argument('--wait',action='store_true');parser.add_argument('--test-only',action='store_true');args=parser.parse_args()
    guard.require(os.uname().nodename.split('.')[0]=='ada','Parent coordinator runs on Ada')
    coordinator=Coordinator(args.grant,args.grant_sha256,args.test_only);stopping=[False]
    signal.signal(signal.SIGTERM,lambda *_:stopping.__setitem__(0,True));signal.signal(signal.SIGINT,lambda *_:stopping.__setitem__(0,True))
    try:
        while not stopping[0] and time.time()<coordinator.g['stop_epoch']-60:
            try:coordinator.acquire();break
            except (FileNotFoundError,BlockingIOError):
                if not args.wait:raise
                guard.atomic(Path(args.grant).parent/'WAITING.json',dict(status='waiting_for_host_acknowledgments_or_parent_lease',updated_epoch=time.time(),compute_started=False));time.sleep(2)
        while coordinator.fd is not None and not stopping[0] and time.time()<coordinator.g['stop_epoch']+1800:
            coordinator.heartbeat();time.sleep(1)
    finally:coordinator.close()

if __name__=='__main__':main()
