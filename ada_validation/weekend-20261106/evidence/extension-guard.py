"""Exact child delegations under the unchanged already-owned R5 parent.

Copy these identical bytes as Ada suballocation_guard.py or peer
allocation_guard.py. There is no parent acquisition or ownership mutation.
"""
from datetime import datetime
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
import importlib.util

SCHEMA = 'fifth42-overnight-child-delegation-v1'
OWNERSHIP_SCHEMA = 'fifth42-overnight-ownership-v1'
GENERATION = 'shared-deadline-distributed-r1-r-sharing'
PARENT_SHA = '10719404786b8fec2b3f3d2eb866befeffe9845d25fc9b8e7a8921d1c6610ce9'
INVENTORY_SHA = '426e193d99e99486493ae7ca9e48dfef70bc66fa66b6ca655a44ccdee4e88ae7'
OWNERS = {f'boole-delegated-20261109-{n}': h for n, h in
          ((30, 'ada'), (31, 'ada'), (32, 'boole'), (33, 'cabbage'), (34, 'ada'))}
PROFILE_KEYS = ('backend','bits','cap','chunk_patches','dispatch_chunksize','geometry_policy',
    'gmp_audit_period','gpu_request_windows','group_limit','journal_buffer_bytes',
    'journal_buffer_max_age_seconds','journal_buffer_records','journal_limit_bytes',
    'maximum_replica_lag_seconds','minimum_free_disk_bytes','ownership_grid_cap',
    'physical_cpus','prep_load_ceiling','preparation_backend','preparation_batch_bytes',
    'preparation_gpu_capacity','preparation_require_lll','preparation_windows','ready_queue_limit',
    'replica_interval_seconds','running_load_limit','shell_hi','shell_lo','width','workers','automatic_resume')
_PARENTS = set()
_HELPERS = {}


def require(ok, message):
    if not ok: raise RuntimeError(message)


def read(path): return json.loads(Path(path).read_bytes())


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda: stream.read(4 * 1024 ** 2), b''): value.update(data)
    return value.hexdigest()


def exact(a, b):
    return json.dumps(a, sort_keys=True, separators=(',', ':'), allow_nan=False) == json.dumps(b, sort_keys=True, separators=(',', ':'), allow_nan=False)


def checked(row, key):
    path = Path(row[key + '_file'])
    require(path.is_absolute() and '..' not in path.parts and sha(path) == row[key + '_sha256'], 'Changed immutable sharing input: ' + key)
    return read(path)


def claim(ledger, job):
    fd = os.open(Path(ledger) / 'reservations.jsonl', os.O_RDWR | os.O_NOFOLLOW)
    try:
        until = time.monotonic() + 5
        while True:
            try: fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB); break
            except BlockingIOError:
                if time.monotonic() >= until: raise
                time.sleep(.02)
        raw = b''
        while True:
            data = os.read(fd, 1024 ** 2)
            if not data: break
            raw += data; require(len(raw) <= 16 * 1024 ** 2, 'Unexpected reservation size')
        require(raw.endswith(b'\n'), 'Incomplete reservation log')
        rows = [json.loads(line) for line in raw.splitlines()]
        for row in rows:
            body = {k: v for k, v in row.items() if k != 'sha256'}
            require(hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',', ':')).encode()).hexdigest() == row['sha256'], 'Original claim checksum changed')
        found = [row for row in rows if row['job'] == job]
        require(len(found) == 1, 'Missing or duplicate original claim'); return found[0]
    finally: os.close(fd)


def locked(path):
    fd = os.open(path, os.O_RDWR | os.O_NOFOLLOW)
    try:
        try: fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in (errno.EAGAIN, errno.EACCES): return True
            raise
        fcntl.lockf(fd, fcntl.LOCK_UN); return False
    finally: os.close(fd)


def _mount():
    row = json.loads(subprocess.check_output(['findmnt','-J','-T','/mnt/nfs_share','-o','TARGET,SOURCE,FSTYPE,OPTIONS'], text=True, timeout=5))['filesystems'][0]
    host = os.uname().nodename.split('.')[0]
    if host == 'ada': require(row['fstype'] in ('ext4','xfs','btrfs','zfs'), 'Actual Ada export filesystem required')
    else:
        require(host in ('boole','cabbage') and row['target'] == '/mnt/nfs_share' and row['source'] == 'ada:/mnt/nfs_share' and row['fstype'] == 'nfs4', 'Actual Ada NFSv4 mount required')
        require(not set(row['options'].split(',')) & {'nolock','local_lock=all','local_lock=posix'}, 'Coherent NFS POSIX locking required')


def _ownership(path, pin, test=False):
    require(sha(path) == pin, 'Ownership manifest changed'); m = read(path)
    require(m.get('schema') == OWNERSHIP_SCHEMA and m.get('status') == 'admitted' and m.get('TEST_ONLY') is test, 'Ownership is not admitted')
    require(m.get('executors') == OWNERS, 'Unexpected sharing ownership map')
    require(m.get('guard_source_sha256') == sha(__file__), 'Sharing guard source differs')
    parent = checked(m, 'parent_grant'); inventory = checked(m, 'parent_inventory')
    require(test or (m['parent_grant_sha256'] == PARENT_SHA and m['parent_inventory_sha256'] == INVENTORY_SHA), 'Unexpected original R5 parent admission')
    require(parent.get('TEST_ONLY') is test and parent['coverage_claimed'] is False and inventory['status'] == 'verified_sealed_inventory', 'Parent/inventory scope changed')
    require(exact(m['tasks'], inventory['tasks']) and {t['ledger_job'] for t in m['tasks']} == set(OWNERS), 'Sharing tasks differ from exact sealed R5 gaps')
    require(type(m['stop_epoch']) is int and m['stop_epoch'] == parent['stop_epoch'] and m['stop_local'] == parent['stop_local'], 'Ownership changed original parent deadline')
    authorization = checked(m, 'deadline_authorization')
    require(authorization['stop_epoch'] == parent['stop_epoch'] and m['deadline_authorization_sha256'] == parent['deadline_authorization_sha256'], 'Ownership deadline authorization differs')
    require(sha(m['parent_source_export_file']) == m['parent_source_export_sha256'] == m['parent_source_sha256'] == parent['coordinator_source_sha256']
            and sha(m['parent_guard_export_file']) == m['parent_guard_export_sha256'] == parent['guard_source_sha256'], 'Pinned parent source/guard export differs')
    for host in ('ada','boole','cabbage'):
        baseline = m['baseline_configs'][host]; require(sha(baseline['file']) == baseline['sha256'], 'Baseline config changed')
        cfg = read(baseline['file']); profile = {k: cfg[k] for k in PROFILE_KEYS if k in cfg}
        require(exact(profile, m['profiles'][host]), 'Profile differs from actual frozen baseline')
        require(profile['workers'] == 16 and profile['physical_cpus'] == list(range(16)) and profile['chunk_patches'] == 256
                and profile['gmp_audit_period'] == 128 and profile['automatic_resume'] is False
                and profile['group_limit'] == (4 if host == 'boole' else 2) and profile['cap'] == (100 if host == 'cabbage' else 42)
                and (profile['shell_lo'],profile['shell_hi'],profile['width'],profile['bits']) == (100000000001,200000000000,8,222), 'Frozen host arithmetic/resources changed')
    retirement = checked(m, 'retirement')
    require(retirement.get('schema') == 'fifth42-compute-admission-retirement-v1' and retirement.get('status') == 'verified_all_r5_compute_launch_paths_retired'
            and retirement.get('TEST_ONLY') is test and retirement.get('old_grant_unchanged_sha256') == m['parent_grant_sha256']
            and all(retirement.get(k) is True for k in ('old_controller_masked','old_watcher_masked','old_runtime_removed_from_admitted_path','failed_stage_guard_revoked','failed_stage_no_native_outputs')), 'Original competing R5 compute is not retired')
    probes = retirement.get('all_five_original_r5_worker_start_probes_rejected', [])
    require(len(probes) == 5 and all(type(row.get('exit_code')) is int and row['exit_code'] != 0 for row in probes), 'Missing actual old-worker rejection probes')
    require(all(row.get('ActiveState') == 'inactive' and row.get('MainPID') == '0' and row.get('LoadState') == 'masked' for row in retirement['units'].values()), 'Old execution unit remains admitted')
    return m, parent


def verify_historical_grant(path, pin, test=False):
    require(sha(path) == pin, 'Child delegation changed'); g = read(path)
    require(g.get('schema') == SCHEMA and g.get('generation') == GENERATION and g.get('TEST_ONLY') is test, 'Wrong sharing child schema/scope')
    m, parent = _ownership(g['ownership_manifest_file'], g['ownership_manifest_sha256'], test)
    job, role = g['ledger_job'], g['executor']; require(m['executors'].get(job) == role, 'Child is assigned to another executor')
    tasks = [t for t in m['tasks'] if t['ledger_job'] == job]; require(len(tasks) == 1, 'Child has no unique sealed task')
    task = tasks[0]; require((g['initial_patch'],g['range_end']) == (task['initial_patch'],task['range_end']), 'Child changed exact sealed cursor/bounds')
    assignments = [r for r in parent['assignments'] if r['job'] == job]
    require(len(assignments) == 1 and g['original_assignment'] == assignments[0] and g['claim'] == task['claim'], 'Original parent assignment/claim changed')
    require(claim(parent['child_ledger'],job) == task['claim'], 'Original reservation changed')
    for key in ('parent_ledger','parent_job','parent_claim_sha256','parent_first','parent_last','child_ledger','original_claim_identity','native_binaries'):
        require(g.get(key) == parent[key], 'Parent compatibility identity changed: ' + key)
    deadline = checked(g,'deadline_authorization')
    require(type(g['stop_epoch']) is int and g['stop_epoch'] <= parent['stop_epoch'] and deadline['stop_epoch'] == g['stop_epoch']
            and deadline['stop_local'] == g['stop_local'] and datetime.fromisoformat(g['stop_local']).timestamp() == g['stop_epoch'], 'Child deadline exceeds parent authorization')
    require(g['worker_guard_sha256'] == sha(__file__), 'Worker guard differs from source')
    require(type(g['runtime_source_files']) is dict and type(g['runtime_external_files']) is dict, 'Missing complete source maps')
    return g


def _unit(name):
    raw = subprocess.check_output(['systemctl','--user','show',name,'-p','ActiveState','-p','MainPID','-p','LoadState'],text=True,timeout=5)
    return dict(line.split('=',1) for line in raw.splitlines() if '=' in line)


def _parent_local(m):
    require(os.uname().nodename.split('.')[0] == 'ada', 'Parent proof belongs on actual Ada')
    require(os.getpid() != m['parent_pid'], 'Never run worker admission in the parent owner process')
    require(_unit(m['parent_unit']).get('MainPID') == str(m['parent_pid']) and _unit(m['parent_unit']).get('ActiveState') == 'active', 'Actual parent unit/PID mismatch')
    args = [s.decode() for s in Path('/proc',str(m['parent_pid']),'cmdline').read_bytes().split(b'\0') if s]
    def arg(key):
        require(args.count(key) == 1 and args.index(key)+1 < len(args), 'Parent CLI option mismatch'); return args[args.index(key)+1]
    require(args.count(m['parent_source_file']) == 1 and arg('--grant') == m['parent_grant_file']
            and arg('--grant-sha256') == m['parent_grant_sha256'] and arg('--inventory-sha256') == m['parent_inventory_sha256'], 'Actual parent source/grant/inventory arguments differ')
    parent = read(m['parent_grant_file'])
    require(sha(m['parent_source_file']) == m['parent_source_sha256']
            and sha(Path(m['parent_source_file']).parent/'extension_guard.py') == parent['guard_source_sha256']
            and sha(parent['inventory_file']) == m['parent_inventory_sha256'], 'Actual parent source/guard/inventory differs')
    retired = read(m['retirement_file'])
    for name in retired['units']:
        state = _unit(name); require(state.get('ActiveState') == 'inactive' and state.get('MainPID') == '0' and state.get('LoadState') == 'masked', 'Old R5 execution unit was restored')
    require(not (Path(m['parent_source_file']).parent/'runtime').exists(), 'Old R5 runtime launch path restored')
    return dict(status='verified_actual_parent_process',parent_pid=m['parent_pid'],TEST_ONLY=m['TEST_ONLY'])


def _parent_proof(m, path, pin, force=False):
    key = (pin,m['parent_pid'])
    if key in _PARENTS and not force: return
    if os.uname().nodename.split('.')[0] == 'ada': _parent_local(m)
    else:
        require(sha(m['guard_source_file']) == m['guard_source_sha256'], 'Shared parent-proof helper changed')
        args = ['python3','-B',m['guard_source_file'],'--parent-proof',str(path),'--sha256',pin]
        result = subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=5','ada',shlex.join(args)],capture_output=True,text=True,timeout=20)
        require(result.returncode == 0, 'Actual Ada parent SSH proof failed: ' + result.stderr[-1500:])
        proof = json.loads(result.stdout); require(proof.get('status') == 'verified_actual_parent_process' and proof.get('parent_pid') == m['parent_pid'], 'Wrong actual parent SSH readback')
    _PARENTS.add(key)


def _live(m, parent):
    require(os.getpid() != m['parent_pid'], 'Never probe parent from its owning process')
    folder = Path(m['parent_grant_file']).parent; state = read(folder/parent['state_file']); active = read(folder/parent['active_file'])
    for row in (state, active):
        require(row['grant_sha256'] == m['parent_grant_sha256'] and row['inventory_sha256'] == m['parent_inventory_sha256'] and row['stop_epoch'] == m['stop_epoch'] and row['coordinator_pid'] == m['parent_pid'], 'Parent heartbeat/activation binding changed')
    require(state['status'] == 'active' and active['status'] == 'active_allocation_ready' and -5 <= time.time()-state['updated_epoch'] <= 10, 'Parent heartbeat is inactive/stale')
    lease = Path(parent['parent_ledger'])/'jobs'/parent['parent_job']/'journal.jsonl'
    require(locked(lease), 'Canonical exclusive original parent POSIX lease absent')


def check(config, force=False, observer_role=None):
    role = config['allocation_role']; host = os.uname().nodename.split('.')[0]
    require(role in ('ada','boole','cabbage') and observer_role in (None,role) and (host == role or (host == 'ada' and observer_role == role)), 'Wrong actual worker/observer host')
    g = verify_historical_grant(config['suballocation_grant_file'],config['suballocation_grant_sha256'],config.get('TEST_ONLY') is True)
    m, parent = _ownership(g['ownership_manifest_file'],g['ownership_manifest_sha256'],config.get('TEST_ONLY') is True)
    require(g['executor'] == role and all(config[k] == g[k] for k in ('ledger_job','initial_patch','range_end','stop_epoch','stop_local')), 'Worker differs from exact child delegation')
    require(config['ledger_root'] == parent['child_ledger'] and config['ledger_claim_sha256'] == g['claim']['sha256'] and config['reservation_manifest_sha256'] == g['claim']['identity'] and config['reservation_initial_patch'] == g['claim']['first'], 'Worker changed original claim')
    require(all(exact(config.get(k),v) for k,v in m['profiles'][role].items()), 'Frozen host math/resource/GMP profile changed')
    worker = Path(config['manifest']).parent; require(sha(config['manifest']) == config['manifest_sha256'], 'Worker manifest changed'); mf = read(config['manifest'])
    require(mf['files'] == g['runtime_source_files'] and mf.get('external_files',{}) == g['runtime_external_files'], 'Worker source maps differ from delegation')
    for name, pin in mf['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts and sha(worker/name) == pin, 'Actual native/runtime source changed: ' + name)
    for name,pin in mf.get('external_files',{}).items(): require(Path(name).is_absolute() and sha(name) == pin, 'External runtime helper changed')
    for name,pin in parent['native_binaries'][role].items(): require(mf['files'].get(name) == pin, 'Original native executable changed')
    guard_name = 'suballocation_guard.py' if role == 'ada' else 'allocation_guard.py'
    require(mf['files'].get(guard_name) == g['worker_guard_sha256'], 'Worker uses another admission guard')
    settings = read(config['deadline_settings_file']); authorization = read(g['deadline_authorization_file'])
    require(sha(config['deadline_settings_file']) == authorization['setting_sha256'] and set(settings) == {'stop_at'} and datetime.fromisoformat(settings['stop_at']).timestamp() == g['stop_epoch'], 'Worker private effective deadline differs')
    if observer_role is not None: return g
    require(time.time() < g['stop_epoch'], 'Fresh child compute admission expired')
    _mount()
    boundary = worker/'boundary_settings.py'
    if boundary.exists():
        require(mf['files'].get('boundary_settings.py') == sha(boundary), 'Boundary helper changed')
        key = (str(boundary),sha(boundary))
        if key not in _HELPERS:
            spec = importlib.util.spec_from_file_location('_sharing_boundary_'+key[1],boundary); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); _HELPERS[key] = module
        require(_HELPERS[key].read_drain_ack(config) is None, 'Old child ACK fences fresh admission')
    _parent_proof(m,g['ownership_manifest_file'],g['ownership_manifest_sha256'],force)
    _live(m,parent)
    return g


def verify_before_acquire(config, force=False): return check(config,force=force)


def deadline_snapshot(config):
    g = verify_historical_grant(config['suballocation_grant_file'],config['suballocation_grant_sha256'],config.get('TEST_ONLY') is True)
    require(config['stop_epoch'] == g['stop_epoch'], 'Worker changed child cutoff')
    return read(g['deadline_authorization_file'])


if __name__ == '__main__':
    require(len(sys.argv) == 5 and sys.argv[1] == '--parent-proof' and sys.argv[3] == '--sha256', 'Only read-only parent proof CLI is supported')
    manifest = read(sys.argv[2]); m, _ = _ownership(sys.argv[2],sys.argv[4],manifest.get('TEST_ONLY') is True)
    print(json.dumps(_parent_local(m)))
