"""Prepare identity-pinned r4 reporting only after the old Ada binding is retired.

No service, native process or network operation is launched here. Existing
collector/publisher logic is reused; new evidence describes the r4 continuation
without importing an analytic-tail wrapper or relabelling old validation.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import time

ROOT = Path(__file__).resolve().parent
BASE = Path('/home/pnord/fifth42-deadline-extension-r5-20261112')
SHARE = Path('/mnt/nfs_share/ada-preparation-publishing-20261110')
CUTOVER = 1794526200
# Legacy fixture value; reporting admits the frozen plan/grant deadline.
DEADLINE = 1794582000
# deadline-authority-v2
SOURCES = {
    'collector': (
        Path('/home/pnord/ada-memory-r2-20261111/stages-v2/ada-memory-r2-job-60-20261111/collector.py'),
        'ce7345b5accc4522a9f724752d0929de84518d23583e493bd7b146538ef1326f'),
    'publisher': (
        Path('/home/pnord/ada-preparation-release-20261110/publish_buffered.py'),
        'edad33289b556b3e10a8adee7106fe3ed12a6cf3e816b4e45884c3ea31c18da5'),
    'bridge': (
        Path('/home/pnord/ada-bulk-reporting-20261108/bridge_base.py'),
        '7a2d572cc4a895e725034866cadb85fac62a9125395d4eb52b0f511039e7305a'),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def atomic(path, raw):
    path = Path(path)
    temporary = path.with_name(path.name + '.' + str(os.getpid()) + '.tmp')
    with temporary.open('wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def json_bytes(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def private_transport(source):
    """The reviewed stage60 substitutions; deadline comes from the private spec."""
    old = 'while time.time()<1794236400+1800:'
    assert source.count(old) == 1, 'Unexpected baseline bridge deadline loop'
    source = source.replace(old, "while time.time()<json.loads((ROOT/'publication-spec.json').read_text())['stop_epoch']+1800:")
    old = "old=json.loads((SHARE/'ada-publication-receipt.json').read_text());next_push=datetime.fromisoformat(old['published_utc']).timestamp()+900;previous_phase=old.get('phase')"
    assert source.count(old) == 1, 'Unexpected baseline startup receipt gate'
    new = "old=json.loads((SHARE/'ada-publication-receipt.json').read_text())\n   if old.get('run_id')==json.loads((ROOT/'publication-spec.json').read_text())['run_id']:\n    next_push=datetime.fromisoformat(old['published_utc']).timestamp()+900;previous_phase=old.get('phase')"
    source = source.replace(old, new)
    source = source.replace('Boole lattice runner', 'Ada lattice runner').replace('boole-lattice@', 'ada-lattice@')
    source = source.replace("previous_phase in ('admitted_not_started','awaiting_collector')",
                            "previous_phase in ('admitted_not_started','awaiting_collector','validating')")
    return source.replace('Update Boole precision search: ', 'Update Ada extended search: ')


def generic_publisher(source):
    # This is a descriptive paragraph only. Keep the generic snapshot checks,
    # exact readback,15-minute cadence and terminal lifecycle logic unchanged.
    old = ('The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. '
           'A separate coordinator holds the original parent lease while child searches run.')
    new = ('This run covers its assigned sealed r4 suffix under an unchanged original child claim. '
           'The predecessor journal is provenance; only this run\'s native interval advances here. '
           'The renewed coordinator holds the original parent lease until the new cutoff.')
    assert source.count(old) == 1, 'Unexpected generic publisher description'
    return source.replace(old, new)


def prepare(stage_root, config, plan):
    """Return the standard queue spec after preparing a fresh stage's reporter.

    Call only after the previous Ada terminal publication has been remotely read
    back and its collector/publisher have been retired. This is additionally
    gated to the17:30 cutover; no live shared binding can be changed beforehand.
    """
    assert time.time() >= CUTOVER, 'r4 reporting cannot rebind live Ada reporting before17:30'
    stage = Path(stage_root)
    worker = stage / 'worker'
    path = worker / 'config.json'
    raw = path.read_bytes()
    cfg = json.loads(raw)
    expected = read(config) if isinstance(config, (str, Path)) else config
    assert cfg == expected, 'Prepared configuration differs from the frozen stage'
    assert cfg['TEST_ONLY'] is False and cfg['allocation_role'] == 'ada'
    frozen_grant = read(Path(cfg['suballocation_grant_file']))
    deadline = plan.get('stop_epoch', frozen_grant['stop_epoch'])
    assert type(deadline) is int and cfg['stop_epoch'] == deadline
    parsed = datetime.fromisoformat(cfg['stop_local'])
    assert parsed.tzinfo is not None and parsed.timestamp() == deadline
    assert cfg['initial_patch'] < cfg['range_end']
    if Path(cfg['output']).exists() or Path(cfg['replica_output']).exists():
        assert plan.get('adopt_running_run_id') == cfg['run_id'], 'Existing output requires exact running adoption'
        local = Path(cfg['output'])
        assert (local/'run-config.json').read_bytes() == raw, 'Running output configuration differs'
        identity = dict(trial=cfg['run_id'], source_identity=sha(json.dumps(
            dict(manifest_sha256=cfg['manifest_sha256'],config=cfg),
            sort_keys=True,separators=(',',':')).encode()))
        assert read(local/'checkpoint.json')['identity'] == identity, 'Running native identity differs'
    manifest_path = Path(cfg['manifest'])
    manifest_raw = manifest_path.read_bytes()
    assert manifest_path == worker / 'release-manifest.json'
    assert sha(manifest_raw) == cfg['manifest_sha256']
    for name, digest in json.loads(manifest_raw)['files'].items():
        assert sha((worker / name).read_bytes()) == digest, 'Stage source mismatch: ' + name
    claim_raw = Path(cfg['origin_claim_file']).read_bytes()
    claim = json.loads(claim_raw)
    assert sha(claim_raw) == cfg['origin_claim_file_sha256']
    assert claim['sha256'] == cfg['ledger_claim_sha256']
    assert claim['first'] <= cfg['initial_patch'] < cfg['range_end'] == claim['last']
    assert sha(Path(cfg['parent_audit_file']).read_bytes()) == cfg['parent_audit_sha256']
    assert sha(Path(cfg['parent_archive_receipt']).read_bytes()) == cfg['parent_archive_receipt_sha256']
    grant_path = Path(cfg['suballocation_grant_file'])
    assert sha(grant_path.read_bytes()) == cfg['suballocation_grant_sha256']
    assert read(grant_path)['stop_epoch'] == deadline
    inventory = Path(plan.get('inventory_file', ROOT / 'INVENTORY.json'))
    assert sha(inventory.read_bytes()) == cfg['extension_inventory_sha256']

    sources = {
        'delegation-grant.json': grant_path,
        'extension-inventory.json': inventory,
        'extension-plan.json': Path(plan.get('plan_file', ROOT / 'PLAN.json')),
        'extension-parent.py': BASE / 'parent_extension.py',
        'extension-guard.py': ROOT / 'sharing_guard.py',
        'extension-controller.py': ROOT / 'queue_controller.py',
        'source-review.json': ROOT / 'SOURCE-REVIEW.json',
        'configuration.json': path,
        'source-manifest.json': manifest_path,
        'parent-audit.json': Path(cfg['parent_audit_file']),
        'parent-archive-receipt.json': Path(cfg['parent_archive_receipt']),
        'original-claim.json': Path(cfg['origin_claim_file']),
        'report-stage.py': Path(__file__).resolve(),
    }
    # Read and validate all input before any shared binding/evidence is changed.
    evidence_raw = {name: source.read_bytes() for name, source in sources.items()}
    inherited = {}
    for label, (source, digest) in SOURCES.items():
        source_raw = source.read_bytes()
        assert sha(source_raw) == digest, 'Reviewed reporting source changed: ' + label
        inherited[label] = source_raw.decode()
    collector = inherited['collector']
    publisher = generic_publisher(inherited['publisher'])
    transport = private_transport(inherited['bridge'])
    for label, source in [('collector', collector), ('publisher', publisher), ('transport', transport)]:
        compile(source, str(stage / 'reporting' / (label + '.py')), 'exec')
    assert 'analytic_tail' not in publisher

    reporter = stage / 'reporting'
    reporter.mkdir(mode=0o700, exist_ok=False)
    SHARE.mkdir(mode=0o700, parents=True, exist_ok=True)
    evidence = SHARE / 'evidence'
    evidence.mkdir(mode=0o700, exist_ok=True)
    hashes = {}
    for name, data in evidence_raw.items():
        atomic(evidence / name, data)
        hashes[name] = sha(data)
    fingerprint = sha(json.dumps(dict(manifest_sha256=cfg['manifest_sha256'], config=cfg),
                                 sort_keys=True, separators=(',', ':')).encode())
    public = dict(run_id=cfg['run_id'], manifest_sha256=cfg['manifest_sha256'],
                  config_sha256=sha(raw), source_identity=fingerprint,
                  ledger_claim_sha256=claim['sha256'], evidence=hashes)
    public_raw = json_bytes(public)
    private = dict(public, host='ada', collector_spec_sha256=sha(public_raw),
                   reserved_interval=[cfg['initial_patch'], cfg['range_end']],
                   original_reserved_interval=[claim['first'], claim['last']],
                   collector_reserved_interval=[cfg['initial_patch'], cfg['range_end']],
                   stop_epoch=cfg['stop_epoch'], parent_selected_patches=cfg['parent_selected_patches'],
                   parent_committed_interval=[cfg['initial_patch']-cfg['parent_selected_patches'], cfg['initial_patch']],
                   parent_audit_sha256=cfg['parent_audit_sha256'],
                   **{key: cfg[key] for key in ('workers', 'backend', 'geometry_policy',
                                                'journal_limit_bytes', 'minimum_free_disk_bytes')})
    for name, value in [('collector.py', collector), ('publish_bulk_worker.py', publisher), ('bridge_base.py', transport)]:
        atomic(reporter / name, value.encode())
    publisher_name = cfg['run_id'] + '-publisher.service'
    collector_name = cfg['run_id'] + '-collector.service'
    settings = dict(host='ada', share=str(SHARE), repository='paulnord/fifth42',
                    branch='handoff/fifth-lattice-optimizations-20261105',
                    publication_path='ada_validation/weekend-20261106',
                    service_name=publisher_name, interval_seconds=900,
                    bridge_base_sha256=sha(transport.encode()))
    collector_settings = dict(host='ada', config=str(path), manifest=str(manifest_path),
                              config_sha256=sha(raw), manifest_sha256=cfg['manifest_sha256'],
                              supervisor_report=str(worker / 'supervisor-report.json'),
                              output=str(SHARE), stop_epoch=cfg['stop_epoch'])
    binding = dict(status='verified', verified_utc=datetime.now(timezone.utc).isoformat(),
                   run_id=cfg['run_id'], manifest_sha256=cfg['manifest_sha256'], config_sha256=sha(raw),
                   inherited_claim_sha256=claim['sha256'], parent_raw_sha256=cfg['parent_journal_raw_sha256'],
                   reporting_only=True, native_validation='Inherited unchanged native arithmetic; launch runs fresh controls',
                   collector_source_sha256=SOURCES['collector'][1],
                   generic_publisher_source_sha256=SOURCES['publisher'][1],
                   baseline_bridge_sha256=SOURCES['bridge'][1])
    for name, value in [('publication-spec.json', private), ('publisher-settings.json', settings),
                        ('collector-settings.json', collector_settings), ('binding.json', binding)]:
        atomic(reporter / name, json_bytes(value))
    atomic(SHARE / 'publication-spec.json', public_raw)
    result = dict(root=str(stage), worker=str(worker), config=str(path), reporter=str(reporter),
                  run_id=cfg['run_id'], first=cfg['initial_patch'], last=cfg['range_end'],
                  service=cfg['service_name'], collector=collector_name, publisher=publisher_name,
                  config_sha256=sha(raw), manifest_sha256=cfg['manifest_sha256'])
    atomic(reporter / 'reporter-preparation.json', json_bytes(dict(
        status='reporter_prepared', prepared_utc=binding['verified_utc'],
        spec=result, source_identity=fingerprint, evidence=hashes,
        automatic_compute_started=False, old_validation_relabelled=False)))
    return result
