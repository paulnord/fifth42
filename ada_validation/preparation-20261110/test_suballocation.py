"""Cross-process parent exclusion, activation, liveness and partition tests."""
import hashlib,json,multiprocessing as mp,os,signal,sys,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'worker'))
import ada_export_store as store_module,suballocation_guard as guard
from parent_coordinator import Coordinator
from durable_mirror import atomic
def broker(path,sha,config,ready,stop):
    c=Coordinator(path,sha,config,True)
    try:
        c.acquire();ready.set()
        while not stop.wait(.02):c.heartbeat()
    finally:c.close()
def holder(path,ready,stop):
    import fcntl
    with open(path,'r+b') as f:
        fcntl.lockf(f,fcntl.LOCK_EX);ready.set();stop.wait(10)
class SuballocationTests(unittest.TestCase):
    def setUp(self):
        self.ctx=mp.get_context('spawn');self.root=guard.TEST/str(time.time_ns())
        self.parent=store_module.Store(self.root);self.claim=self.parent.reserve('old-owner',100000000,300000000,'d'*64,dict(TEST_ONLY=True))
        path=self.root/'jobs/old-owner/journal.jsonl';path.touch(mode=0o600)
        self.old_bytes=(self.root/'reservations.jsonl').read_bytes()
        self.child=self.root/'suballocations/test';store_module.Store(self.child)
        self.g=dict(schema='fifth42-parent-suballocation-v1',TEST_ONLY=True,parent_ledger=str(self.root),parent_job='old-owner',parent_claim_sha256=self.claim['sha256'],parent_first=100000000,parent_last=300000000,child_ledger=str(self.child),assignments=dict(ada=[100000000,200000000],boole=[200000000,300000000]),stop_epoch=time.time()+60,retained_manifest_sha256='e'*64,coverage_claimed=False)
        self.gpath=self.child/'GRANT.json';atomic(self.gpath,self.g);self.gsha=hashlib.sha256(self.gpath.read_bytes()).hexdigest()
        self.c=dict(TEST_ONLY=True,run_id='TEST_ONLY-retained',initial_patch=100000000,range_end=200000000,ledger_root=str(self.child),allocation_role='ada',stop_epoch=self.g['stop_epoch'],manifest_sha256='e'*64,suballocation_grant_file=str(self.gpath),suballocation_grant_sha256=self.gsha,output=str(self.root/'run'))
        self.config=self.root/'retained.json';atomic(self.config,self.c)
        self.processes=[]
    def tearDown(self):
        for child,stop in self.processes:
            if child.is_alive():
                try:os.kill(child.pid,signal.SIGCONT)
                except ProcessLookupError:pass
                stop.set();child.join(2)
                if child.is_alive():child.kill();child.join(2)
        self.assertEqual((self.root/'reservations.jsonl').read_bytes(),self.old_bytes)
    def start_broker(self):
        ready=self.ctx.Event();stop=self.ctx.Event()
        child=self.ctx.Process(target=broker,args=(str(self.gpath),self.gsha,str(self.config),ready,stop));child.start();self.processes.append((child,stop))
        self.assertTrue(ready.wait(5));return child
    def activate(self):
        p=Path(self.c['output']);p.mkdir()
        fingerprint=hashlib.sha256(json.dumps(dict(manifest_sha256=self.c['manifest_sha256'],config=self.c),sort_keys=True,separators=(',',':')).encode()).hexdigest()
        atomic(p/'checkpoint.json',dict(next_patch=self.c['initial_patch']+256,identity=dict(trial=self.c['run_id'],source_identity=fingerprint),window=dict(last=self.c['range_end'])))
        atomic(p/'status.json',dict(status='running',error=None))
        atomic(p/'controls.json',dict(status='passed',cases=[dict(full_oracle_equal=True,hits=[[13,16,17,12]])]))
        until=time.monotonic()+3
        while guard.read(self.child/'coordinator-state.json')['status']!='active':
            self.assertLess(time.monotonic(),until);time.sleep(.02)
    def boole(self):return dict(self.c,allocation_role='boole',initial_patch=200000000,range_end=300000000)
    def test_parent_cannot_be_delegated_while_old_owner_holds_it(self):
        ready=self.ctx.Event();stop=self.ctx.Event();p=self.ctx.Process(target=holder,args=(str(self.root/'jobs/old-owner/journal.jsonl'),ready,stop));p.start();self.processes.append((p,stop));self.assertTrue(ready.wait(5))
        c=Coordinator(self.gpath,self.gsha,self.config,True)
        try:
            with self.assertRaises(store_module.Busy):c.acquire()
        finally:c.close()
    def test_borrower_waits_for_live_bounded_successor(self):
        self.start_broker();self.assertEqual(guard.check(self.c)['assignments']['ada'],[100000000,200000000])
        with self.assertRaises(RuntimeError):guard.check(self.boole())
        self.activate();self.assertEqual(guard.check(self.boole())['assignments']['boole'],[200000000,300000000])
    def test_overlap_and_escape_are_rejected(self):
        bad=dict(self.g,assignments=dict(ada=[100000000,210000000],boole=[200000000,300000000]));atomic(self.gpath,bad)
        with self.assertRaises(RuntimeError):guard.load_grant(self.gpath,hashlib.sha256(self.gpath.read_bytes()).hexdigest(),True)
        atomic(self.gpath,self.g);self.start_broker();self.activate()
        with self.assertRaises(RuntimeError):guard.check(dict(self.boole(),initial_patch=199999999))
    def test_deadline_change_is_rejected(self):
        self.start_broker()
        with self.assertRaises(RuntimeError):guard.check(dict(self.c,stop_epoch=self.g['stop_epoch']+1))
    def test_broker_death_releases_parent_and_stops_dependents(self):
        p=self.start_broker();p.terminate();p.join(3)
        with self.assertRaises(RuntimeError):guard.check(self.c)
        with self.parent.locked(self.root/'jobs/old-owner/journal.jsonl'):pass
    def test_stale_heartbeat_rejected_even_with_parent_lock(self):
        p=self.start_broker();os.kill(p.pid,signal.SIGSTOP)
        state=guard.read(self.child/'coordinator-state.json');state['updated_epoch']=time.time()-30;atomic(self.child/'coordinator-state.json',state)
        with self.assertRaises(RuntimeError):guard.check(self.c)
    def test_grant_tampering_rejected(self):
        self.start_broker();self.gpath.write_bytes(self.gpath.read_bytes()+b' ')
        with self.assertRaises(RuntimeError):guard.check(self.c)
if __name__=='__main__':unittest.main(verbosity=2)
