"""Seal verified final coverage and fresh shared claims; never stop or launch work."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import ada_export_store
import policy

ROOT=Path(__file__).resolve().parent
PREFLIGHT=Path('/home/pnord/fifth-switch-preflight-20261107')
OLD=Path('/home/pnord/fifth-weekend-runs/20261106T230428Z')
SHARED=Path('/mnt/nfs_share')
ORIGINAL_SERVICE='fifth-packed-weekend-20261106T230428Z.service'


def write(path,value):
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('w') as stream:
        json.dump(value,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    temporary.replace(path)
    fd=os.open(path.parent,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)


def gates():
    adapter_hash=policy.digest(ROOT/'ada_export_store.py')
    probe=SHARED/'TEST_ONLY_boole_ada_protocol_20261107_v1'
    for role in ('ada','boole'):
        protocol=json.loads((probe/(role+'-result.json')).read_bytes())
        policy.require(protocol['status']=='PASS' and protocol['host']==role and
                       protocol['TEST_ONLY'] is True and protocol['mathematical_coverage'] is False,
                       'Cross-host protocol evidence missing')
        actual=json.loads((SHARED/'TEST_ONLY_ada_export_adapter_20261107_ada'/
                           (role+'-actual-adapter-result.json')).read_bytes())
        policy.require(actual['status']=='PASS' and actual['host']==role and
                       actual['source_sha256']==adapter_hash and
                       actual['actual_deployment_verifier'] is True and
                       actual['in_memory_guard_substitution'] is False,
                       'Actual deployment adapter evidence missing or changed')
    policy.require(json.loads((ROOT/'host-validation/report.json').read_bytes())['status']=='passed',
                   'Host validation missing')
    policy.require(json.loads((ROOT/'unit-validation-summary.json').read_bytes())['status']=='passed',
                   'Critical unit validation missing')
    return dict(status='passed',adapter_sha256=adapter_hash,filesystem='Ada /mnt/nfs_share export',
                nas_validated=False,production_work_launched=False)


def seal():
    proof=gates()
    config=json.loads((ROOT/'config.json').read_bytes())
    policy.require(config['ledger_claim_sha256']=='DRAFT' and not Path(config['output']).exists(),
                   'Claimed or launched release cannot be regenerated')
    service=subprocess.check_output(['systemctl','--user','show',ORIGINAL_SERVICE,
                                     '--property=ActiveState,MainPID'],text=True,timeout=5)
    policy.require('ActiveState=inactive' in service and 'MainPID=0' in service,
                   'Original search must already be cleanly stopped')
    report_path=PREFLIGHT/'final-audit/20261106T230428Z-prefix-audit.json'
    audit=json.loads(report_path.read_bytes())
    checkpoint_raw=(OLD/'run/checkpoint.json').read_bytes();checkpoint=json.loads(checkpoint_raw)
    status_raw=(OLD/'run/status.json').read_bytes();status=json.loads(status_raw)
    policy.require(audit['status']=='passed' and audit['final_checkpoint'] is True and
                   audit['uncommitted_trailing_bytes']==0 and
                   audit['captured_checkpoint_sha256']==hashlib.sha256(checkpoint_raw).hexdigest() and
                   status['status']=='stopped' and status['error'] is None,
                   'Verified final parent checkpoint is missing')
    config.update(parent_checkpoint_sha256=hashlib.sha256(checkpoint_raw).hexdigest(),
                  parent_journal_sha256=checkpoint['journal_sha256'],
                  parent_journal_offset=checkpoint['journal_offset'],
                  parent_status_sha256=hashlib.sha256(status_raw).hexdigest(),
                  initial_patch=checkpoint['next_patch'],
                  parent_selected_patches=62966016+checkpoint['patches'])
    policy.require(config['parent_selected_patches']==config['initial_patch']-3750000000,
                   'Prior selected lineage totals do not join')
    policy.require(policy.digest(ROOT/'bin/scaling_gpu')==policy.digest(OLD/'bin/scaling_gpu'),
                   'Validated native GPU binary changed')
    write(ROOT/'config.json',config);write(ROOT/'base-config.json',config)
    subprocess.run([sys.executable,'-B',str(ROOT/'refresh_release.py')],check=True,timeout=30)
    config=json.loads((ROOT/'config.json').read_bytes())
    segments=[]
    for relative in ('fifth-lattice-gpu/overnight-runs/20261105T231850Z-bxr6mn4c',
                     'fifth-afternoon-runs/20261106T191039Z/run',
                     'fifth-afternoon-runs/20261106T193915Z/run',
                     'fifth-weekend-runs/20261106T230428Z/run'):
        run=Path('/home/pnord')/relative
        cp=json.loads((run/'checkpoint.json').read_bytes())
        first=cp['window']['first'] if 'window' in cp else cp['region_initial_patch']
        segments.append(dict(run=str(run),first=first,last=cp['next_patch'],patches=cp['patches'],
                             checkpoint_sha256=policy.digest(run/'checkpoint.json'),
                             journal_offset=cp['journal_offset'],journal_chain_sha256=cp['journal_sha256']))
    cursor=3750000000
    for segment in segments:
        policy.require(segment['first']==cursor and segment['patches']==segment['last']-cursor,
                       'Historical lineage has a gap or duplicate')
        cursor=segment['last']
    policy.require(cursor==config['initial_patch'],'Final lineage cursor mismatch')
    coverage=dict(status='verified_receipts',final_checkpoint=True,sealed_utc=policy.utc(),
                  grid=dict(cmin=100000000001,cmax=200000000000,width=8,cap=42,count=11250000001),
                  next_patch=cursor,parent_checkpoint_sha256=config['parent_checkpoint_sha256'],
                  parent_journal_sha256=config['parent_journal_sha256'],
                  parent_journal_raw_sha256=audit['committed_raw_sha256'],
                  parent_journal_committed_bytes=checkpoint['journal_offset'],
                  covered_intervals=[[3750000000,cursor]],
                  remaining_intervals=[[0,3750000000],[cursor,11250000001]],
                  unsupported_uncovered_patches=[dict(patch=0,reason='Original integer-transform guard; never completed or silently skipped')],
                  segments=segments,selected_patches=cursor-3750000000,completed_bound=None,
                  independent_oracle_verified_through=0,successor_geometry_policy='adaptive',
                  successor_executor='persistent_gpu',successor_manifest_sha256=config['manifest_sha256'],
                  audit_report_sha256=policy.digest(report_path),
                  limitation='Verified committed receipts and lineage; historical coefficients were not all recomputed. Selected coverage only.')
    write(ROOT/'final-coverage.json',coverage)
    config['coverage_sha256']=policy.digest(ROOT/'final-coverage.json')
    audit=dict(audit,files_before={
        'checkpoint.json':dict(size=len(checkpoint_raw),sha256=config['parent_checkpoint_sha256']),
        'coverage.jsonl':dict(size=checkpoint['journal_offset'],sha256=audit['committed_raw_sha256'])})
    write(ROOT/'parent-audit.json',audit)
    config['ledger_root']=str(SHARED/'TEST_ONLY_ada_export_adapter_20261107_ada'/
                              ('gpu-ledger-'+config['manifest_sha256'][:12]))
    config['ledger_job']=config['run_id']+'-validation'
    config['output']=str(Path(config['ledger_root'])/'jobs'/config['ledger_job']/'run')
    store=ada_export_store.Store(config['ledger_root'])
    config['ledger_device']=store.device
    linked=dict(sha256=config['coverage_sha256'],manifest=coverage)
    history=store.reserve('verified-history-20261107',3750000000,cursor,config['coverage_sha256'],linked)
    claim=store.reserve(config['ledger_job'],cursor,config['range_end'],config['manifest_sha256'],linked)
    config['ledger_claim_sha256']=claim['sha256']
    write(ROOT/'config.json',config);write(ROOT/'base-config.json',config)
    policy.load_config(ROOT/'config.json')
    record=dict(status='sealed_awaiting_gpu_validation',sealed_utc=policy.utc(),
                parent_cursor=cursor,manifest_sha256=config['manifest_sha256'],
                config_sha256=policy.digest(ROOT/'config.json'),coverage_sha256=config['coverage_sha256'],
                history_claim_sha256=history['sha256'],test_claim_sha256=claim['sha256'],
                test_ledger=config['ledger_root'],production_claims_created=False,storage_gate=proof)
    write(ROOT/'sealed-handoff.json',record)
    print(json.dumps(record,indent=2))


def ready():
    config=policy.load_config(ROOT/'config.json')
    gpu=json.loads((ROOT/'gpu-validation-report.json').read_bytes())
    policy.require(gpu['status']=='passed' and gpu['speedup']>1.1 and gpu['signal_stop_passed'] and
                   gpu['absolute_deadline_stop_passed'],'GPU validation incomplete')
    policy.require(not Path(config['output']).exists(),'Production output already exists')
    production=SHARED/'fifth42-shared-20261107'
    linked=dict(sha256=config['coverage_sha256'],manifest=json.loads((ROOT/'final-coverage.json').read_bytes()))
    store=ada_export_store.Store(production)
    history=store.reserve('verified-history-20261107',3750000000,config['initial_patch'],config['coverage_sha256'],linked)
    claim=store.reserve(config['run_id'],config['initial_patch'],config['range_end'],config['manifest_sha256'],linked)
    config.update(ledger_root=str(production),ledger_job=config['run_id'],ledger_device=store.device,
                  ledger_claim_sha256=claim['sha256'],output=str(production/'jobs'/config['run_id']/'run'))
    write(ROOT/'config.json',config);write(ROOT/'base-config.json',config)
    policy.load_config(ROOT/'config.json')
    report=dict(status='ready',prepared_utc=policy.utc(),manifest_sha256=config['manifest_sha256'],
                config_sha256=policy.digest(ROOT/'config.json'),storage_gate=gates(),
                host_validation_sha256=policy.digest(ROOT/'host-validation/report.json'),
                gpu_validation_sha256=policy.digest(ROOT/'gpu-validation-report.json'),
                unit_validation_sha256=policy.digest(ROOT/'unit-validation-summary.json'),
                coverage_sha256=config['coverage_sha256'],gpu_speedup=gpu['speedup'],
                history_claim_sha256=history['sha256'],production_claim_sha256=claim['sha256'],
                stop_local=config['stop_local'],automatic_resume=False,production_work_launched=False)
    write(ROOT/'preparation-report.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('check-gates','seal','ready'))
    action=parser.parse_args().action
    if action=='check-gates':print(json.dumps(gates(),indent=2))
    elif action=='seal':seal()
    else:ready()
