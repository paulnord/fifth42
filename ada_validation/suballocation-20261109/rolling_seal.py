"""Audit a live append-only prefix; finalize a planned, clean handoff on request."""
from datetime import datetime,timezone
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLD=Path('/home/pnord/ada-overnight-20261109/worker')
sys.path[:0]=[str(OLD),'/home/pnord/boole-continuation-check-20261108']
import audit_grouped
from check_continuation import owner_is_locked
def read(p):return json.loads(Path(p).read_bytes())
def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()
def atomic(p,row):
    p=Path(p);t=p.with_name(p.name+'.tmp')
    t.write_text(json.dumps(row,indent=2)+'\n');os.replace(t,p)
def identity(p):
    s=p.stat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def main():
    os.nice(19)
    cfg=read(OLD/'config.json');local=Path(cfg['output']);replica=Path(cfg['replica_output'])
    previous=None;audits=0;started=time.time()
    atomic(ROOT/'rolling-seal-status.json',dict(status='auditing',started_epoch=started))
    while time.time()<cfg['stop_epoch']:
        raw=(replica/'checkpoint.json').read_bytes();cp=json.loads(raw);receipt=read(replica/'replica-state.json')
        if hashlib.sha256(raw).hexdigest()!=receipt['checkpoint_sha256']:
            time.sleep(.5);continue
        if previous is None or cp['journal_offset']>previous['journal_offset']:
            baseline=dict(checkpoint=previous if previous else dict(next_patch=cfg['initial_patch']),config=cfg)
            result=audit_grouped.audit_suffix(replica,baseline,cp,'append' if previous else 'fresh',cfg['gmp_audit_period'])
            audits+=result['new_gmp_audited_chunks'];previous=cp
            atomic(ROOT/'rolling-seal-status.json',dict(status='caught_up',audited_cursor=cp['next_patch'],audited_chunks=cp['chunks'],audited_gmp_samples=audits,checkpoint_sha256=hashlib.sha256(raw).hexdigest(),updated_epoch=time.time()))
        if (ROOT/'FINALIZE_PARENT').exists():
            state=read(local/'status.json')
            if state['status']=='stopped' and state['error'] is None and not owner_is_locked(Path(cfg['ledger_root'])/'jobs'/cfg['ledger_job']/'journal.jsonl'):
                localraw=(local/'checkpoint.json').read_bytes()
                if raw!=localraw:time.sleep(.5);continue
                assert previous==cp and cp['journal_offset']==(local/'coverage.jsonl').stat().st_size==(replica/'coverage.jsonl').stat().st_size
                local_hash=digest(local/'coverage.jsonl');replica_hash=digest(replica/'coverage.jsonl')
                assert local_hash==replica_hash==receipt['raw_sha256']
                assert (local/'status.json').read_bytes()==(replica/'status.json').read_bytes()
                audit=dict(status='passed',final_checkpoint=True,new_chunks=cp['chunks'],new_patches=cp['patches'],new_gmp_audited_chunks=audits,next_patch=cp['next_patch'],captured_checkpoint_sha256=hashlib.sha256(raw).hexdigest(),committed_chain_sha256=cp['journal_sha256'],committed_raw_sha256=local_hash,committed_bytes=cp['journal_offset'],selected_interval=[cfg['initial_patch'],cp['next_patch']],uncommitted_trailing_bytes=0,owner_lock_released=True,local_and_replica_equal=True,verified_utc=datetime.now(timezone.utc).isoformat(),method='Complete live-prefix audit followed by every appended suffix and a full stopped local/replica raw SHA256 comparison')
                atomic(ROOT/'final-parent-audit.json',audit)
                seal=dict(status='verified',local=str(local),replica=str(replica),final_cursor=cp['next_patch'],checkpoint=cp,source_manifest_sha256=cfg['manifest_sha256'],config_sha256=digest(OLD/'config.json'),audit_sha256=digest(ROOT/'final-parent-audit.json'),local_journal_identity=identity(local/'coverage.jsonl'),replica_journal_identity=identity(replica/'coverage.jsonl'),raw_sha256=local_hash,cumulative_selected_patches=cfg['parent_selected_patches']+cp['patches'])
                atomic(ROOT/'sealed-parent.json',seal);atomic(ROOT/'rolling-seal-status.json',dict(status='sealed',cursor=cp['next_patch'],updated_epoch=time.time()))
                print(json.dumps(dict(status='sealed',cursor=cp['next_patch'])),flush=True);return
        time.sleep(2)
    raise TimeoutError('No handoff was requested before the frozen production deadline')
if __name__=='__main__':main()
