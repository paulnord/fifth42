"""Hold the legacy parent claim while independently leased child jobs run."""
import argparse,fcntl,hashlib,json,os,signal,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'worker')]
import ada_export_store,suballocation_guard as guard
from durable_mirror import atomic
STOP=False
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def parent_claim(store,job):
    until=time.monotonic()+5
    while True:
        try:return store.claim(job)
        except ada_export_store.Busy:
            if time.monotonic()>=until:raise
            time.sleep(.05)
class Coordinator:
    def __init__(self,grant_path,grant_sha,retained_config,test=False):
        self.path=Path(grant_path);self.sha=grant_sha;self.g=guard.load_grant(self.path,grant_sha,test)
        self.cfg_path=Path(retained_config);self.test=test;self.context=None;self.fd=None;self.active=False;self.activation_audit=None
        if not test:guard.require(sha(__file__)==self.g['coordinator_source_sha256'],'Coordinator source differs from grant')
    def acquire(self):
        g=self.g;store=ada_export_store.Store(g['parent_ledger']);claim=parent_claim(store,g['parent_job'])
        guard.require((claim['sha256'],claim['first'],claim['last'])==(g['parent_claim_sha256'],g['parent_first'],g['parent_last']),'Original parent claim changed')
        self.context=store.locked(store.root/'jobs'/g['parent_job']/'journal.jsonl')
        self.fd=self.context.__enter__();self.store=store
        self.cfg=read(self.cfg_path);self.cfg_sha=sha(self.cfg_path)
        c=self.cfg;a=g['assignments']['ada']
        guard.require(c['TEST_ONLY'] is self.test and [c['initial_patch'],c['range_end']]==a,'Retained configuration does not enforce its hard cap')
        guard.require(c['stop_epoch']==g['stop_epoch'] and c['manifest_sha256']==g['retained_manifest_sha256'],'Retained source/deadline changed')
        guard.require(Path(c['ledger_root'])==Path(g['child_ledger']) and c['suballocation_grant_sha256']==self.sha,'Retained grant/child ledger mismatch')
        if not self.test:
            guard.require(sha(c['manifest'])==c['manifest_sha256'],'Retained manifest changed')
            m=read(c['manifest']);w=Path(c['manifest']).parent
            for n,h in m['files'].items():guard.require(sha(w/n)==h,'Retained runtime changed: '+n)
            guard.require((w/'base-config.json').read_bytes()==self.cfg_path.read_bytes(),'Retained immutable base differs')
        self.heartbeat()
    def heartbeat(self):
        guard.require(self.fd is not None,'Parent lease not acquired')
        g=self.g;path=Path(g['parent_ledger'])/'jobs'/g['parent_job']/'journal.jsonl'
        a,b=os.fstat(self.fd),path.stat();guard.require((a.st_dev,a.st_ino)==(b.st_dev,b.st_ino),'Parent lease inode was replaced')
        guard.require(sha(self.path)==self.sha and sha(self.cfg_path)==self.cfg_sha,'Frozen grant/retained configuration changed')
        guard.require(parent_claim(self.store,g['parent_job'])['sha256']==g['parent_claim_sha256'],'Parent reservation changed while delegated')
        if not self.active:
            p=Path(self.cfg['output']);cp=p/'checkpoint.json';status=p/'status.json';controls=p/'controls.json'
            if cp.exists() and status.exists() and controls.exists():
                state=read(status);point=read(cp);control=read(controls)
                fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=self.cfg['manifest_sha256'],config=self.cfg),sort_keys=True,separators=(',',':')).encode()).hexdigest()
                if state['status'] in (('running','completed_test') if self.test else ('running',)) and state['error'] is None and point['next_patch']>self.cfg['initial_patch']:
                    guard.require(point['identity']==dict(trial=self.cfg['run_id'],source_identity=fingerprint),'Retained live identity mismatch')
                    guard.require(point['window']['last']==g['assignments']['ada'][1] and point['next_patch']<=g['assignments']['ada'][1],'Retained live window exceeds cap')
                    guard.require(control['status']=='passed' and all(x['full_oracle_equal'] and x['hits'] for x in control['cases']),'Retained nonempty controls failed')
                    if not self.test:
                        import audit_grouped
                        audited=audit_grouped.audit_suffix(p,dict(checkpoint=dict(next_patch=self.cfg['initial_patch']),config=self.cfg),point,'fresh',self.cfg['gmp_audit_period'])
                        self.activation_audit=dict(status='passed',**audited)
                    self.active=True
        atomic(Path(g['child_ledger'])/'coordinator-state.json',dict(status='active' if self.active else 'prepared',grant_sha256=self.sha,coordinator_pid=os.getpid(),parent_job=g['parent_job'],parent_claim_sha256=g['parent_claim_sha256'],retained_configuration_sha256=self.cfg_sha,retained_manifest_sha256=g['retained_manifest_sha256'],retained_range_end=g['assignments']['ada'][1],activation_audit=self.activation_audit,stop_epoch=g['stop_epoch'],updated_epoch=time.time(),TEST_ONLY=self.test))
    def close(self):
        if self.context:
            self.context.__exit__(None,None,None);self.context=None;self.fd=None
def main():
    global STOP
    p=argparse.ArgumentParser();p.add_argument('--grant',type=Path,required=True);p.add_argument('--grant-sha256',required=True);p.add_argument('--retained-config',type=Path,required=True);p.add_argument('--test-only',action='store_true');a=p.parse_args()
    signal.signal(signal.SIGTERM,lambda *_:globals().__setitem__('STOP',True));signal.signal(signal.SIGINT,lambda *_:globals().__setitem__('STOP',True))
    c=Coordinator(a.grant,a.grant_sha256,a.retained_config,a.test_only)
    try:
        c.acquire()
        while not STOP and time.time()<c.g['stop_epoch']+1800:c.heartbeat();time.sleep(1)
    except BaseException as error:
        atomic(Path(c.g['child_ledger'])/'coordinator-failure.json',dict(error=repr(error),epoch=time.time()));raise
    finally:c.close()
if __name__=='__main__':main()
