"""Prepare identity-pinned reporting for Ada's root-reuse release."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / 'worker'
REPORTER = Path('/home/pnord/ada-preparation-reporting-20261110')
SHARE = Path('/mnt/nfs_share/ada-preparation-publishing-20261110')
OLD = Path('/home/pnord/ada-bulk-reporting-20261108')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def write(path, row):
    path.write_text(json.dumps(row, indent=2) + '\n')


def main():
    cfg_raw = (WORKER / 'config.json').read_bytes()
    cfg = json.loads(cfg_raw)
    manifest_raw = (WORKER / 'release-manifest.json').read_bytes()
    assert sha(manifest_raw) == cfg['manifest_sha256']
    assert cfg['run_id'] == 'ada-preparation-20261110' and cfg['TEST_ONLY'] is False
    runtime = read(ROOT / 'runtime-validation.json')
    assert runtime['status'] == 'passed' and runtime['manifest_sha256'] == cfg['manifest_sha256']
    for file in ('unit-validation.json', 'gpu-validation.json'):
        assert read(ROOT / file)['status'] == 'passed'
    parent = Path(cfg['parent_run'])
    assert sha((parent / 'ARCHIVE_RECEIPT.json').read_bytes()) == cfg['parent_archive_receipt_sha256']
    claim = read(cfg['origin_claim_file'])
    assert claim['sha256'] == cfg['ledger_claim_sha256'] and cfg['initial_patch'] < cfg['range_end'] == claim['last']
    REPORTER.mkdir(mode=0o700, exist_ok=True)
    evidence = SHARE / 'evidence'
    evidence.mkdir(mode=0o700, parents=True, exist_ok=True)
    sources = {
        'delegation-grant.json': Path(cfg['suballocation_grant_file']),
        'parent-coordinator.py': ROOT/'parent_coordinator.py',
        'configuration.json': WORKER / 'config.json',
        'source-manifest.json': WORKER / 'release-manifest.json',
        'parent-audit.json': ROOT / 'parent-audit.json',
        'parent-archive-receipt.json': parent / 'ARCHIVE_RECEIPT.json',
        'original-claim.json': Path(cfg['origin_claim_file']),
        'runtime-validation.json': ROOT / 'runtime-validation.json',
        'gpu-validation.json': ROOT / 'gpu-validation.json',
        'unit-validation.json': ROOT / 'unit-validation.json',
        'selection-results.json': ROOT/'selection-results.json',
        'group-comparison.json': ROOT/'selection-results.json',
        'buffering-tests.json': ROOT/'unit-validation.json',
    }
    hashes = {}
    for name, source in sources.items():
        raw = source.read_bytes()
        (evidence / name).write_bytes(raw)
        hashes[name] = sha(raw)
    fingerprint = sha(json.dumps(dict(manifest_sha256=cfg['manifest_sha256'], config=cfg), sort_keys=True, separators=(',', ':')).encode())
    spec = dict(run_id=cfg['run_id'], manifest_sha256=cfg['manifest_sha256'], config_sha256=sha(cfg_raw),
                source_identity=fingerprint, ledger_claim_sha256=claim['sha256'], evidence=hashes)
    write(SHARE / 'publication-spec.json', spec)
    spec.update(host='ada', collector_spec_sha256=sha((SHARE / 'publication-spec.json').read_bytes()),
                reserved_interval=[cfg['initial_patch'], cfg['range_end']],
                original_reserved_interval=[claim['first'], claim['last']],
                collector_reserved_interval=[cfg['initial_patch'], cfg['range_end']],
                stop_epoch=cfg['stop_epoch'], parent_selected_patches=cfg['parent_selected_patches'],
                parent_committed_interval=[cfg['initial_patch'] - cfg['parent_selected_patches'], cfg['initial_patch']],
                parent_audit_sha256=cfg['parent_audit_sha256'],
                **{k: cfg[k] for k in ('workers', 'backend', 'geometry_policy', 'journal_limit_bytes', 'minimum_free_disk_bytes')})
    write(REPORTER / 'publication-spec.json', spec)
    collector=(ROOT/'collector.py').read_text()
    (REPORTER/'collector.py').write_text(collector)
    transport = (OLD / 'bridge_base.py').read_text()
    assert transport.count('while time.time()<1794236400+1800:') == 1
    transport = transport.replace('while time.time()<1794236400+1800:', "while time.time()<json.loads((ROOT/'publication-spec.json').read_text())['stop_epoch']+1800:")
    transport = transport.replace('Boole lattice runner', 'Ada lattice runner').replace('boole-lattice@', 'ada-lattice@')
    transport = transport.replace('Update Boole precision search: ', 'Update Ada buffered search: ')
    (REPORTER / 'bridge_base.py').write_text(transport)
    publisher=(ROOT/'publish_buffered.py').read_text()
    (REPORTER/'publish_bulk_worker.py').write_text(publisher)
    write(REPORTER / 'publisher-settings.json', dict(host='ada', share=str(SHARE), repository='paulnord/fifth42',
          branch='handoff/fifth-lattice-optimizations-20261105', publication_path='ada_validation/weekend-20261106',
          service_name='ada-preparation-publisher-20261110.service', interval_seconds=900,
          bridge_base_sha256=sha((REPORTER / 'bridge_base.py').read_bytes())))
    write(REPORTER / 'collector-settings.json', dict(host='ada', config=str(WORKER / 'config.json'),
          manifest=str(WORKER / 'release-manifest.json'), config_sha256=sha(cfg_raw), manifest_sha256=cfg['manifest_sha256'],
          supervisor_report=str(WORKER / 'supervisor-report.json'), output=str(SHARE), stop_epoch=cfg['stop_epoch']))
    write(REPORTER / 'binding.json', dict(status='verified', verified_utc=datetime.now(timezone.utc).isoformat(),
          run_id=cfg['run_id'], manifest_sha256=cfg['manifest_sha256'], config_sha256=sha(cfg_raw),
          inherited_claim_sha256=claim['sha256'], root_reuse_enabled=True,
          unchanged_native_binary=True, parent_raw_sha256=cfg['parent_journal_raw_sha256']))
    for file in ('collector.py', 'bridge_base.py', 'publish_bulk_worker.py'):
        compile((REPORTER / file).read_text(), str(REPORTER / file), 'exec')
    print(json.dumps(dict(status='reporter_prepared', root=str(REPORTER), share=str(SHARE), source_identity=fingerprint), indent=2))


if __name__ == '__main__':
    main()
