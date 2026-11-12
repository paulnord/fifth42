"""One Ada claim31 delegation under the still-owned original r3 parent.

This module never acquires, replaces, renews or releases that parent. Historical
verification is explicit and grants no new admission. Install as a fresh
worker/suballocation_guard.py; no original source or reservation is edited.
"""
from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import time

SCHEMA = 'fifth42-interim-child-delegation-v1'
GENERATION = 'ada-early-claim31-20261112'
JOB = 'boole-delegated-20261109-31'
ORIGINAL_SHA = '14cd2aca8cafafc80799473cb9497e9c86be4b6f866a8b72c4d6b67a1c696df9'
FALLBACK_SHA = '89af32f2df8b79c8f0f481d2d6484910248e79c3360b94762c7f553e24c59e44'
FALLBACK_PLAN_SHA = 'b3bab30c1c2c882291b01a6de983f54c99859b231042b794371d3c919b12157c'
FALLBACK_UNIT = 'ada-deadline-extension-r4-20261112.service'
FALLBACK_LAUNCH = '/mnt/nfs_share/fifth42-integration-20261109/combined/deadline-extension-r4-20261112/GRANT-r4.json'
RETIRED_UNITS = {FALLBACK_UNIT, 'ada-search-settings-control-20261112.service',
                 'ada-extension-r4-global-deadline-20261112.timer'}
PHASE_CAP = 1794524400
PROFILE = dict(group_limit=2, chunk_patches=256, cap=42, width=8, bits=222,
    shell_lo=100000000001, shell_hi=200000000000, workers=16,
    physical_cpus=list(range(16)), dispatch_chunksize=4, preparation_windows=16,
    preparation_batch_bytes=134217728, gpu_request_windows=1,
    preparation_backend='cpu', backend='gpu', geometry_policy='adaptive',
    ready_queue_limit=1, journal_buffer_records=8, journal_buffer_bytes=8388608,
    journal_buffer_max_age_seconds=.25, replica_interval_seconds=60,
    maximum_replica_lag_seconds=300, journal_limit_bytes=34359738368,
    minimum_free_disk_bytes=17179869184, prep_load_ceiling=17.0,
    running_load_limit=20.0, gmp_audit_period=128, automatic_resume=False)
REVIEWED = {
    'policy.py': 'facddc4bd9f6f94a469e7dd440301bf0ce3f1245ae8a1509b249262edad8c4cf',
    'packed_worker.py': 'eee00a3316b9ae7475284842b5133b9f9eb1efd6c2d0b23cd650249489f24b43',
    'search_supervisor.py': '88f9617dff81fdcc3b6dd9977b92218d30526077f17f0c012a5aa50a9e1c9634',
    'launch_weekend.py': '369a84c4a44a320fcd08cd812646516e00cb656c11ee443780eaa71ec2a6099e',
}
_MODULES = {}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda: stream.read(4 * 1024 ** 2), b''):
            digest.update(data)
    return digest.hexdigest()


def digest(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def exact(left, right):
    return json.dumps(left, sort_keys=True, separators=(',', ':'), allow_nan=False) == \
           json.dumps(right, sort_keys=True, separators=(',', ':'), allow_nan=False)


def checked(row, name):
    path = Path(row[name + '_file'])
    require(path.is_absolute() and '..' not in path.parts
            and digest(row[name + '_sha256']) and sha(path) == row[name + '_sha256'],
            'Changed immutable early delegation input: ' + name)
    return read(path)


def artifacts(row):
    files = row.get('source_artifacts')
    require(type(files) is list and files, 'Missing retained admission proof artifacts')
    seen = set()
    for entry in files:
        path = Path(entry['file'])
        require(path.is_absolute() and '..' not in path.parts and str(path) not in seen
                and digest(entry['sha256']) and sha(path) == entry['sha256'],
                'Changed retained admission proof artifact')
        seen.add(str(path))


def _legacy(g):
    path, expected = Path(g['original_guard_file']), g['original_guard_sha256']
    require(path.is_absolute() and sha(path) == expected, 'Original r3 guard source changed')
    key = (str(path), expected)
    if key not in _MODULES:
        spec = importlib.util.spec_from_file_location('_early_original_r3_' + expected, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        require(sha(path) == expected, 'Original r3 guard moved during import')
        _MODULES[key] = module
    return _MODULES[key]


def _boundary(config, g):
    path = Path(config['manifest']).parent / 'boundary_settings.py'
    expected = g['runtime_source_files'].get('boundary_settings.py')
    require(digest(expected) and sha(path) == expected, 'Pinned worker boundary helper changed')
    key = ('boundary', str(path), expected)
    if key not in _MODULES:
        spec = importlib.util.spec_from_file_location('_early_boundary_' + expected, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        require(sha(path) == expected, 'Pinned worker boundary helper moved during import')
        _MODULES[key] = module
    return _MODULES[key]


def _unit(name):
    result = subprocess.run(['systemctl', '--user', 'show', name, '-p', 'ActiveState', '-p', 'MainPID'],
                            capture_output=True, text=True, check=True, timeout=5)
    return dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)


def _process_args(pid):
    raw = Path('/proc', str(pid), 'cmdline').read_bytes()
    return [part.decode() for part in raw.split(b'\0') if part]


def _inactive(name, row):
    return row.get('ActiveState') == 'inactive' and (
        row.get('MainPID') == '0' or (name.endswith('.timer') and row.get('MainPID') is None))


def _argument(args, option):
    require(args.count(option) == 1 and args.index(option) + 1 < len(args),
            'Original parent argument missing or ambiguous: ' + option)
    return args[args.index(option) + 1]


def _epoch(local):
    require(type(local) is str and all(not any(c != '0' for c in part)
            for part in re.findall(r'[.,]([0-9]+)', local)), 'Cutoff must use exact whole seconds')
    parsed = datetime.fromisoformat(local.replace('Z', '+00:00'))
    require(parsed.utcoffset() is not None and parsed.microsecond == 0,
            'Cutoff must be an aware whole second')
    return parsed.timestamp()


def _snapshot(g, name):
    value = checked(g, name)
    epoch, local = value.get('stop_epoch'), value.get('stop_local')
    require(value.get('schema') == 'fifth42-deadline-authorization-v1'
            and type(epoch) is int and type(local) is str and digest(value.get('setting_sha256')),
            'Invalid immutable early deadline snapshot')
    require(_epoch(local) == epoch,
            'Early snapshot is not an exact aware whole-second cutoff')
    return value


def verify_historical_grant(path, expected, test=False):
    """Verify frozen evidence only; an expired grant never permits computation."""
    require(digest(expected) and sha(path) == expected, 'Immutable early delegation changed')
    g = read(path)
    require(g.get('schema') == SCHEMA and g.get('generation') == GENERATION
            and g.get('status') == 'admitted' and g.get('TEST_ONLY') is test
            and g.get('executor') == 'ada', 'Wrong early delegation schema/scope/executor')
    require(type(g.get('execution_request_id')) is str and g['execution_request_id'],
            'Missing coordinated early execution request')
    require(test or g['execution_request_id'] == 'ada-early31-20261112-r1',
            'Unknown production early execution request')
    old = checked(g, 'original_parent_grant')
    require(test or g['original_parent_grant_sha256'] == ORIGINAL_SHA, 'Unexpected original production r3 grant')
    legacy = _legacy(g)
    require(old.get('schema') == legacy.SCHEMA and old.get('generation') == 'range-extension-r3-20261111'
            and old.get('TEST_ONLY') is test and old.get('grid') == legacy.GRID,
            'Original r3 scope changed')
    # Deliberately validate the FROZEN historical grant at its own admitted
    # instant. This is not a live clock substitution or a startup permission.
    legacy.validate_grant(old, test, now=old['stop_epoch'] - 1)
    require(g['original_guard_sha256'] == old['guard_source_sha256']
            and g['original_parent_source_sha256'] == old['coordinator_source_sha256']
            and Path(g['original_parent_source_file']).is_absolute()
            and sha(g['original_parent_source_file']) == old['coordinator_source_sha256'],
            'Original parent/guard source identity changed')
    assignment = g['original_assignment']
    originals = [row for row in old['assignments'] if row['job'] == JOB]
    require(len(originals) == 1 and assignment == originals[0] and assignment['owner'] == 'boole',
            'Early delegation changed original claim31 assignment')
    claim = legacy.claim(old['child_ledger'], JOB)
    require((claim['first'], claim['last'], claim['sha256'], claim['identity']) ==
            (assignment['first'], assignment['last'], assignment['claim_sha256'], assignment['claim_identity']),
            'Early delegation changed original claim31 reservation')
    require(type(g.get('initial_patch')) is int and type(g.get('range_end')) is int
            and assignment['first'] <= g['initial_patch'] < g['range_end'] == assignment['last'],
            'Early delegation is not an exact original-claim suffix')
    phase, desired = _snapshot(g, 'phase_deadline_authorization'), _snapshot(g, 'desired_deadline_authorization')
    cap = g.get('phase_not_after_epoch')
    require(type(cap) is int and cap == old['stop_epoch'] and (test or cap == PHASE_CAP)
            and type(g.get('stop_epoch')) is int and g['stop_epoch'] == min(cap, desired['stop_epoch'])
            and phase['stop_epoch'] == g['stop_epoch'] and phase['stop_local'] == g['stop_local'],
            'Early compute deadline exceeds original admission or desired cutoff')
    require(exact(g.get('runtime_profile'), PROFILE), 'Ada arithmetic/resource/GMP profile changed')
    require(g.get('native_binaries') == old['native_binaries']['ada'], 'Original Ada native binary pins changed')
    sources, external = g.get('runtime_source_files'), g.get('runtime_external_files')
    require(type(sources) is dict and type(external) is dict and sources,
            'Missing exact reviewed runtime source maps')
    require(sources.get('suballocation_guard.py') == g.get('worker_guard_sha256') == sha(__file__),
            'Early worker guard differs from reviewed source')
    for name, expected_source in dict(REVIEWED, **g['native_binaries']).items():
        require(sources.get(name) == expected_source, 'Unreviewed native/runtime/timer source: ' + name)
    require(all(type(name) is str and not Path(name).is_absolute() and '..' not in Path(name).parts
                and digest(pin) for name, pin in sources.items())
            and all(Path(name).is_absolute() and '..' not in Path(name).parts and digest(pin)
                    for name, pin in external.items()), 'Invalid reviewed source map')
    fence = checked(g, 'fence_ack')
    require(fence.get('schema') == 'fifth42-child-execution-fence-v1'
            and fence.get('status') == 'verified_future_child_admission_revoked'
            and fence.get('TEST_ONLY') is test and fence.get('host') == 'boole'
            and fence.get('job') == JOB and fence.get('executor') == 'ada'
            and fence.get('execution_request_id') == g['execution_request_id']
            and fence.get('original_parent_grant_sha256') == g['original_parent_grant_sha256']
            and fence.get('claim_sha256') == assignment['claim_sha256']
            and fence.get('future_admission_revoked') is True
            and fence.get('current_other_child_untouched') is True,
            'Missing or mismatched actual Boole future31 fence acknowledgment')
    artifacts(fence)
    retired = checked(g, 'fallback_retirement')
    require(retired.get('schema') == 'fifth42-fallback-retirement-v1'
            and retired.get('status') == 'verified_fallback_retired' and retired.get('TEST_ONLY') is test
            and retired.get('execution_request_id') == g['execution_request_id']
            and type(retired.get('old_controller_main_pid')) is int and retired['old_controller_main_pid'] == 0
            and retired.get('old_launch_path_revoked') is True and retired.get('old_admission_retired') is True,
            'Overlapping waiting fallback remains admitted')
    for name in ('old_grant_preserved', 'old_plan_preserved'):
        checked(retired, name)
    require(test or (retired['old_controller_unit'] == FALLBACK_UNIT
            and retired['old_grant_preserved_sha256'] == FALLBACK_SHA
            and retired['old_plan_preserved_sha256'] == FALLBACK_PLAN_SHA
            and retired['revoked_launch_file'] == FALLBACK_LAUNCH),
            'Retirement does not identify the actual overlapping fallback')
    require(digest(retired.get('revoked_launch_sha256'))
            and Path(retired['revoked_launch_file']).is_absolute(), 'Missing revoked fallback launch identity')
    artifacts(retired)
    require(type(retired.get('retired_units')) is list and retired['retired_units']
            and all(type(row.get('unit')) is str and row['unit'].endswith(('.service', '.timer'))
                    and row.get('MainPID') in (0, '0') and row.get('ActiveState') == 'inactive'
                    for row in retired['retired_units']), 'Incomplete fallback unit retirement receipt')
    require(test or RETIRED_UNITS <= {row['unit'] for row in retired['retired_units']},
            'Fallback watcher/controller/global timer was not retired')
    require(type(g.get('original_parent_pid')) is int and g['original_parent_pid'] > 0
            and type(g.get('original_parent_unit')) is str and g['original_parent_unit'].endswith('.service'),
            'Missing actual original parent process identity')
    require(sha(path) == expected, 'Early delegation moved during frozen verification')
    return g


def _config_binding(config, g):
    old = read(g['original_parent_grant_file'])
    require(config.get('allocation_role') == 'ada' and config.get('ledger_job') == JOB
            and config.get('ledger_root') == old['child_ledger']
            and config.get('ledger_claim_sha256') == g['original_assignment']['claim_sha256']
            and config.get('reservation_manifest_sha256') == g['original_assignment']['claim_identity']
            and config.get('reservation_initial_patch') == g['original_assignment']['first']
            and config.get('initial_patch') == g['initial_patch'] and config.get('range_end') == g['range_end']
            and config.get('stop_epoch') == g['stop_epoch'] and config.get('stop_local') == g['stop_local'],
            'Worker changed exact early original-claim suffix/deadline')
    fresh = g['initial_patch'] == g['original_assignment']['first']
    require(config.get('parent_reference_only') is fresh and config.get('parent_selected_patches') == 0
            and (fresh or config.get('reference_parent_cursor') == g['initial_patch']),
            'Early worker imports or skips an inherited native prefix')
    for key, expected in PROFILE.items():
        require(exact(config.get(key), expected),
                'Early worker profile changed: ' + key)
    phase = _snapshot(g, 'phase_deadline_authorization')
    require(sha(config['deadline_settings_file']) == phase['setting_sha256'],
            'Worker does not use the private capped admission settings snapshot')
    settings = read(config['deadline_settings_file'])
    require(type(settings) is dict and set(settings) == {'stop_at'}
            and type(settings['stop_at']) is str, 'Invalid private phase admission settings')
    require(_epoch(settings['stop_at']) == g['stop_epoch'],
            'Private phase settings differ from immutable admission cutoff')
    worker = Path(config['manifest']).parent
    require(sha(config['manifest']) == config['manifest_sha256'], 'Worker source manifest changed')
    manifest = read(config['manifest'])
    require(manifest['files'] == g['runtime_source_files']
            and manifest.get('external_files', {}) == g['runtime_external_files'],
            'Worker source manifest is not the exact reviewed runtime source maps')
    for name, expected in g['runtime_source_files'].items():
        require(sha(worker / name) == expected, 'Actual early runtime source changed: ' + name)
    for name, expected in g['runtime_external_files'].items():
        require(sha(name) == expected, 'Actual early external helper changed: ' + name)


def check(config, force=False, observer_role=None):
    """Fresh actual Ada admission, or explicit read-only frozen observation."""
    require(os.uname().nodename.split('.')[0] == 'ada', 'Early delegation executes only on physical Ada')
    require(observer_role in (None, 'ada'), 'Wrong early delegation observer')
    require(type(config.get('TEST_ONLY')) is bool, 'Worker test scope must be explicit')
    path, expected = config['suballocation_grant_file'], config['suballocation_grant_sha256']
    g = verify_historical_grant(path, expected, config.get('TEST_ONLY') is True)
    _config_binding(config, g)
    if observer_role == 'ada':
        return g
    require(time.time() < g['stop_epoch'], 'Early compute admission has expired')
    require(_boundary(config, g).read_drain_ack(config) is None,
            'Early grant has a drain acknowledgment; fresh admission fenced')
    require(os.getpid() != g['original_parent_pid'], 'Admission must not run in the original parent owner process')
    owner = _unit(g['original_parent_unit'])
    require(owner.get('ActiveState') == 'active' and owner.get('MainPID') == str(g['original_parent_pid']),
            'Actual original parent unit/PID differs')
    args = _process_args(g['original_parent_pid'])
    require(args.count(g['original_parent_source_file']) == 1
            and _argument(args, '--grant') == g['original_parent_grant_file']
            and _argument(args, '--grant-sha256') == g['original_parent_grant_sha256'],
            'Actual original parent command/source/grant identity differs')
    retired = read(g['fallback_retirement_file'])
    require(sha(retired['revoked_launch_file']) == retired['revoked_launch_sha256'],
            'Retired fallback launch path was restored or changed')
    for row in retired['retired_units']:
        actual = _unit(row['unit'])
        require(_inactive(row['unit'], actual),
                'Retired fallback unit became active: ' + row['unit'])
    controller = _unit(retired['old_controller_unit'])
    require(_inactive(retired['old_controller_unit'], controller),
            'Overlapping old fallback controller is active')
    # Explicit historical-owner observation checks the unchanged original r3
    # parent; only THIS independently admitted delegation authorizes Ada compute.
    provenance = dict(config, suballocation_grant_file=g['original_parent_grant_file'],
                      suballocation_grant_sha256=g['original_parent_grant_sha256'], allocation_role='boole',
                      stop_epoch=read(g['original_parent_grant_file'])['stop_epoch'])
    legacy = _legacy(g)
    original = legacy.check(provenance, force=force, observer_role='boole')
    state = legacy.read(Path(g['original_parent_grant_file']).parent / original['state_file'])
    active = legacy.read(Path(g['original_parent_grant_file']).parent / original['active_file'])
    require(state.get('coordinator_pid') == active.get('coordinator_pid') == g['original_parent_pid'],
            'Original parent heartbeat/activation PID differs')
    return g


def verify_before_acquire(config, force=False):
    """Preflight admission only; acquire no original-parent ownership handle."""
    return check(config, force=force)


def deadline_snapshot(config):
    g = verify_historical_grant(config['suballocation_grant_file'],
            config['suballocation_grant_sha256'], config.get('TEST_ONLY') is True)
    require(config['stop_epoch'] == g['stop_epoch'] and config['stop_local'] == g['stop_local'],
            'Config differs from immutable capped phase deadline')
    return _snapshot(g, 'phase_deadline_authorization')
