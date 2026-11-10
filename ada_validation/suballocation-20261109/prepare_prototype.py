"""Freeze guard code and prepare isolated finite/full-range handoff probes."""
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
OLD=Path('/home/pnord/ada-overnight-20261109/worker')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,row):path.write_text(json.dumps(row,indent=2)+'\n')
def main():
    old=json.loads((OLD/'config.json').read_bytes());mf=json.loads((OLD/'release-manifest.json').read_bytes())
    names=list(mf['files'])+['suballocation_guard.py','transition_resources.py']
    current=dict(mf,files={n:sha(W/n) for n in names},release_version='ada-parent-suballocation-r1-20261109',parent_manifest_sha256=old['manifest_sha256'],created_utc=datetime.now(timezone.utc).isoformat())
    existing=json.loads((W/'release-manifest.json').read_bytes()) if (W/'release-manifest.json').exists() else {}
    if existing.get('files')!=current['files'] or existing.get('release_version')!=current['release_version']:write(W/'release-manifest.json',current)
    for n in ['parent-audit.json','final-coverage.json','origin-claim.json']:shutil.copy2(OLD/n,W/n)
    child='/mnt/nfs_share/fifth42-shared-20261107/suballocations/ada-boole-20261109-r1'
    proto=dict(old,run_id='ada-suballocation-20261109',ledger_root=child,ledger_job='ada-suballocated-20261109',range_end=7000000000,manifest=str(W/'release-manifest.json'),manifest_sha256=sha(W/'release-manifest.json'),allocation_role='ada',suballocation_grant_file=child+'/GRANT.json',suballocation_grant_sha256='0'*64,output='/home/pnord/fifth42-local-runs/ada-suballocated-20261109/ada-suballocation-20261109/run',replica_output='/mnt/localstorage/pnord/fifth42-storage/runs/ada-suballocated-20261109/ada-suballocation-20261109/run',service_name='ada-suballocation-20261109.service',deadline_service_name='ada-suballocation-20261109-deadline.service',journal_limit_bytes=116*1024**3,handoff_parent_config_file=str(OLD/'config.json'),handoff_parent_config_sha256=sha(OLD/'config.json'),parent_audit_file=str(W/'parent-audit.json'),coverage_file=str(W/'final-coverage.json'),origin_claim_file=str(W/'origin-claim.json'))
    for key in ['output','replica_output']:Path(proto[key]).parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    for name in ['base-config.json','config.json']:write(W/name,proto)
    write(ROOT/'prototype-config.json',proto)
    import sys
    sys.path.insert(0,str(W));import ada_export_store,suballocation_guard as guard
    for case in ['finite','signal']:
        folder=ROOT/'preflight'/case;folder.mkdir(mode=0o700,parents=True,exist_ok=True)
        parent_root=guard.TEST/('gpu-'+case+'-'+str(time.time_ns()))
        parent=ada_export_store.Store(parent_root);claim=parent.reserve('test-parent',3917103232,11250000001,'a'*64,dict(TEST_ONLY=True))
        (parent_root/'jobs/test-parent/journal.jsonl').touch(mode=0o600)
        child_root=parent_root/'suballocations/retained';store=ada_export_store.Store(child_root)
        end=time.time()+120;last=proto['initial_patch']+2048 if case=='finite' else 7000000000
        grant=dict(schema='fifth42-parent-suballocation-v1',TEST_ONLY=True,parent_ledger=str(parent_root),parent_job='test-parent',parent_claim_sha256=claim['sha256'],parent_first=claim['first'],parent_last=claim['last'],child_ledger=str(child_root),assignments=dict(ada=[proto['initial_patch'],last],boole=[last,11250000001]),stop_epoch=end,retained_manifest_sha256=proto['manifest_sha256'],coverage_claimed=False)
        gp=child_root/'GRANT.json';write(gp,grant)
        job='ada-suballocation-test-'+case;childclaim=store.reserve(job,proto['initial_patch'],last,proto['manifest_sha256'],dict(TEST_ONLY=True))
        own=folder/'origin-claim.json';write(own,childclaim)
        output=Path('/home/pnord/fifth42-local-runs/TEST_ONLY_suballocation_20261109')/job/'run';replica=Path('/mnt/localstorage/pnord/fifth42-storage/TEST_ONLY_suballocation_20261109')/job/'run'
        for p in [output,replica]:p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        cfg=dict(proto,TEST_ONLY=True,run_id=job,ledger_root=str(child_root),ledger_job=job,ledger_device=store.device,ledger_claim_sha256=childclaim['sha256'],range_end=last,gmp_audit_period=1,test_chunk_limit=8 if case=='finite' else None,stop_epoch=end,stop_local=datetime.fromtimestamp(end,ZoneInfo('America/Chicago')).isoformat(),service_name=job+'.service',deadline_service_name=job+'-deadline.service',output=str(output),replica_output=str(replica),suballocation_grant_file=str(gp),suballocation_grant_sha256=sha(gp),origin_claim_file=str(own),origin_claim_file_sha256=sha(own),reservation_manifest_sha256=childclaim['identity'],reservation_initial_patch=childclaim['first'])
        write(folder/'configuration.json',cfg)
    print(json.dumps(dict(status='prototype_prepared',manifest_sha256=proto['manifest_sha256']),indent=2))
if __name__=='__main__':main()
