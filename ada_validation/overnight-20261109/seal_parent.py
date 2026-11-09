"""Read-only full audit and byte verification of the stopped Ada parent."""
from datetime import datetime, timezone
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OLD = Path('/home/pnord/ada-group4-20261109/worker')
sys.path.insert(0, str(OLD))
import audit_grouped
sys.path.insert(0, '/home/pnord/boole-continuation-check-20261108')
from check_continuation import owner_is_locked

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024**2), b''): h.update(block)
    return h.hexdigest()

def identity(path):
    s = path.stat()
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def write(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2)+'\n')

def main():
    cfg = json.loads((OLD/'config.json').read_bytes())
    local, replica = map(Path, (cfg['output'], cfg['replica_output']))
    assert (local/'checkpoint.json').read_bytes() == (replica/'checkpoint.json').read_bytes()
    cp = json.loads((local/'checkpoint.json').read_bytes())
    status = json.loads((local/'status.json').read_bytes())
    assert status['status']=='stopped' and status['error'] is None
    assert not owner_is_locked(Path(cfg['ledger_root'])/'jobs'/cfg['ledger_job']/'journal.jsonl')
    before = [identity(p/'coverage.jsonl') for p in (local, replica)]
    assert all(s[2]==cp['journal_offset'] for s in before)
    audited = audit_grouped.audit_suffix(replica, dict(checkpoint=dict(next_patch=cfg['initial_patch']),config=cfg), cp, 'fresh', cfg['gmp_audit_period'])
    raw = sha(local/'coverage.jsonl')
    assert sha(replica/'coverage.jsonl') == raw
    assert before == [identity(p/'coverage.jsonl') for p in (local, replica)]
    assert (local/'status.json').read_bytes() == (replica/'status.json').read_bytes()
    audited.update(status='passed', final_checkpoint=True, captured_checkpoint_sha256=sha(replica/'checkpoint.json'), committed_chain_sha256=cp['journal_sha256'], committed_raw_sha256=raw, committed_bytes=cp['journal_offset'], selected_interval=[cfg['initial_patch'],cp['next_patch']], uncommitted_trailing_bytes=0, owner_lock_released=True, local_and_replica_equal=True, verified_utc=datetime.now(timezone.utc).isoformat())
    write('final-parent-audit.json', audited)
    seal = dict(status='verified',local=str(local),replica=str(replica),final_cursor=cp['next_patch'],checkpoint=cp,source_manifest_sha256=cfg['manifest_sha256'],config_sha256=sha(OLD/'config.json'),audit_sha256=sha(ROOT/'final-parent-audit.json'),local_journal_identity=before[0],replica_journal_identity=before[1],raw_sha256=raw,cumulative_selected_patches=cfg['parent_selected_patches']+cp['patches'])
    write('sealed-parent.json', seal)
    print(json.dumps(dict(status='verified',next_patch=cp['next_patch'],bytes=cp['journal_offset'],chunks=cp['chunks'],audits=audited['new_gmp_audited_chunks']),indent=2),flush=True)

if __name__=='__main__': main()
