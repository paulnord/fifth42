#!/usr/bin/env python3
"""Read the weekend search's saved state and publish bounded GitHub snapshots."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
RUN = Path('/home/pnord/fifth-optimized-20261107/candidate')
RUN_ID = '20261107T213849Z-precision'
BRANCH = 'handoff/fifth-lattice-optimizations-20261105'
REMOTE = 'git@github.com:paulnord/fifth42.git'
PUBLIC = 'ada_validation/weekend-20261106'
LEGACY = 'ada_validation/overnight-20261105/STATUS.md'
SERVICE = 'fifth-precision-weekend-20261107T213849Z-precision.service'
REPORT_SERVICE = 'weekend-precision-report-20261107T213849Z-precision.service'
INTERVAL = 900
FINAL_LIMIT = 1794236400 + 1800
URL = f'https://github.com/paulnord/fifth42/blob/{BRANCH}/{PUBLIC}/STATUS.md'


def utc():
    return datetime.now(timezone.utc).isoformat()


def atomic(path, value):
    temporary = path.with_suffix('.tmp')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def show(unit):
    result = subprocess.run(
        ['systemctl', '--user', 'show', unit,
         '--property=LoadState,ActiveState,SubState,MainPID,NRestarts,NextElapseUSecRealtime,ActiveEnterTimestamp'],
        check=True, capture_output=True, text=True, timeout=5)
    return dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)


def snapshot():
    # Read existing JSON only. No runner imports, journal recovery or search locks.
    config_bytes = (RUN / 'config.json').read_bytes()
    config = json.loads(config_bytes)
    output = Path(config['output'])
    status = json.loads((output / 'status.json').read_text())
    checkpoint = json.loads((output / 'checkpoint.json').read_text())
    supervisor = json.loads((RUN / 'supervisor-report.json').read_text())
    if status['run_id'] != RUN_ID or checkpoint['identity']['trial'] != RUN_ID:
        raise ValueError('Wrong run identity')
    if checkpoint['identity']['source_identity'] != status['source_identity']:
        raise ValueError('Checkpoint/source identity mismatch')
    if hashlib.sha256(config_bytes).hexdigest() != supervisor['config_sha256']:
        raise ValueError('Frozen configuration changed')
    if checkpoint['next_patch'] - config['initial_patch'] != checkpoint['patches']:
        raise ValueError('Checkpoint cursor/totals mismatch')
    service = show(SERVICE)
    timer = show(SERVICE.removesuffix('.service') + '-deadline.timer')
    active = service.get('ActiveState') in ('active', 'activating', 'deactivating', 'reloading')
    alerts = []
    now = time.time()
    for name, row in (('worker', status), ('supervisor', supervisor)):
        age = now - datetime.fromisoformat(row['updated_utc']).timestamp()
        if active and age > 120:
            alerts.append(f'{name} status is {age:.0f} seconds old')
        if row.get('error'):
            alerts.append(f"{name}: {row['error']}")
    if active and status['status'] != 'running':
        alerts.append('Search service is active but worker is ' + status['status'])
    if active and timer.get('ActiveState') != 'active':
        alerts.append('Deadline timer is not active')
    if not active and supervisor['status'] == 'running':
        alerts.append('Search service stopped; supervisor still reports running')
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    resources = dict(load_average=os.getloadavg(), free_disk_bytes=shutil.disk_usage(RUN).free,
                     available_memory_bytes=int(memory['MemAvailable'].split()[0]) * 1024)
    errors = {name: (RUN / name).stat().st_size
              for name in ('worker.stderr.log', 'service.stderr.log')}
    phase = 'running' if active else 'stopped'
    if active and alerts:
        phase = 'attention_required'
    return dict(
        snapshot_utc=utc(), run_id=RUN_ID, phase=phase, search_service=service,
        stop_timer=timer, alerts=alerts, resources=resources, error_log_bytes=errors,
        stop_local=config['stop_local'], stop_epoch=config['stop_epoch'],
        workers=config['workers'], initial_patch=config['initial_patch'],
        geometry_policy=config['geometry_policy'],ledger_root=config['ledger_root'],
        ledger_claim_sha256=config['ledger_claim_sha256'],coverage_sha256=config['coverage_sha256'],
        gpu_validation=json.loads((RUN/'gpu-validation-report.json').read_text()),
        parent_selected_patches=config['parent_selected_patches'],
        combined_selected_patches=config['parent_selected_patches'] + checkpoint['patches'],
        checkpoint=checkpoint,
        worker_metrics={key: status[key] for key in (
            'status', 'updated_utc', 'patches', 'chunks', 'patches_per_second',
            'search_seconds', 'gmp_audited_chunks', 'preparation_pacing_seconds',
            'independent_oracle_verified_through', 'reason', 'error', 'source_identity')},
        supervisor={key: supervisor.get(key) for key in ('status', 'updated_utc', 'error', 'worker_exit_code')},
        config_sha256=supervisor['config_sha256'],
        reporting=dict(service=REPORT_SERVICE, interval_seconds=INTERVAL,
                       publication='separate read-only publisher',
                       terminal_snapshot='published after the search service stops'),
        coverage_scope='Selected patch coverage only; no completed full-box bound.',
        completed_bound=checkpoint['completed_bound'])


def markdown(row):
    cp = row['checkpoint']
    metrics = row['worker_metrics']
    alerts = '; '.join(row['alerts']) or 'None reported'
    total = row['combined_selected_patches']
    hits = len(cp['hits'])
    rates = row['gpu_validation']['median_patches_per_second']
    return f'''# ADA adaptive-precision weekend search

Last GitHub snapshot: **{row['snapshot_utc']}**.
Search state: **{row['phase']}**. Worker status refreshed: **{metrics['updated_utc']}**.

The original weekend search started Friday, November 6, 2026 at 5:19:57 p.m. Central.
This fresh adaptive-precision continuation starts at verified cursor **{row['initial_patch']:,}**.
Current service active since: **{row['search_service'].get('ActiveEnterTimestamp', 'see status.json')}**.
Stop deadline: **Monday, November 9 at 9:00 a.m. Central**.
The independent cleanup timer is **{row['stop_timer'].get('ActiveState', 'unknown')}/{row['stop_timer'].get('SubState', 'unknown')}**;
next firing: **{row['stop_timer'].get('NextElapseUSecRealtime', 'not scheduled')}**.
The search runs as a systemd user service with login linger enabled.
Automatic restart/resume of the search is disabled.

| Measurement | Saved value |
|---|---:|
| New committed patches in this continuation | {cp['patches']:,} |
| New committed chunks in this continuation | {cp['chunks']:,} |
| Next patch cursor | {cp['next_patch']:,} |
| Cumulative selected patches including prior runs | {total:,} |
| Coefficient points in this continuation | {cp['points']:,} |
| Average search throughput at worker status timestamp | {metrics['patches_per_second']:,.1f} patches/s |
| Search elapsed at worker status timestamp | {metrics['search_seconds'] / 3600:.2f} hours |
| Recorded hits | {hits} |
| Periodic independent GMP audits at worker status timestamp | {metrics['gmp_audited_chunks']:,} |
| Preparation pacing | {metrics['preparation_pacing_seconds']:.1f} seconds |

Configuration: 16 workers pinned to physical CPUs 0–15, optimized packed/prefetched
preparation, one CUDA owner and journal writer, width 8, adaptive geometry, cap 42,
denominators in [100000000001, 200000000000]. Geometry uses the validated adaptive
precision policy with 222-bit fallback; actual per-patch precision is recorded in
the journal. Exact certificates, native bounds and residual checks are retained.
First and every 128th chunk receive independent GMP checks. The range reservation
and fresh journal use Ada's shared export. The original journal is preserved.

Matched short Ada tests measured **{rates['baseline']:,.1f} patches/s baseline** and
**{rates['adaptive']:,.1f} adaptive**, a **{row['gpu_validation']['speedup']:.2f}x** ratio,
including pipeline, journal and checkpoint costs. These selected trials do not
guarantee constant weekend throughput. Cube pruning is not enabled.

Coverage is **selected partial patch coverage**. No completed full-box bound is
claimed: `completed_bound` is null and `independent_oracle_verified_through` is 0.
Periodic GMP audits do not constitute an exhaustive oracle of the whole domain.

Alerts: **{alerts}**.
Worker reason: **{metrics['reason']}**. Worker error: **{metrics['error']}**.
Supervisor error: **{row['supervisor']['error']}**.
Worker/service stderr sizes: **{row['error_log_bytes']['worker.stderr.log']} / {row['error_log_bytes']['service.stderr.log']} bytes**.
Free disk: **{row['resources']['free_disk_bytes'] / 2**30:.1f} GiB**;
available memory: **{row['resources']['available_memory_bytes'] / 2**30:.1f} GiB**.

This separate publisher aims to update every 15 minutes and after the search
stops. The timestamp is the freshness indicator. It reads saved JSON and service
state; it does not audit the full coverage journal or certify new mathematics.
Checkpoint totals and the worker's ten-second status counters can differ slightly.
The frozen search's internal publication setting remains disabled; this separate
reporting service performs publication without changing the running search.
See [status.json](status.json) for the captured checkpoint, digest, service state,
audit timestamps, provenance and resource measurements.
The [verified handoff](precision/final-coverage.json),
[GPU validation](precision/gpu-validation-report.json), and
[frozen source manifest](precision/release-manifest.json) describe this continuation.
The [original run's final snapshot](precision/pre-precision-final.json) is preserved.

[Previous overnight run](../overnight-20261105/STATUS.md).
'''


def git(*args, data=None, env=None, check=True):
    environment = dict(os.environ, GIT_TERMINAL_PROMPT='0',
        GIT_AUTHOR_NAME='ADA lattice runner', GIT_COMMITTER_NAME='ADA lattice runner',
        GIT_AUTHOR_EMAIL='ada-lattice@users.noreply.github.com',
        GIT_COMMITTER_EMAIL='ada-lattice@users.noreply.github.com',
        GIT_SSH_COMMAND='ssh -i /home/pnord/.ssh/fifth42_status_20261105 '
        '-o IdentitiesOnly=yes -o IdentityAgent=none -o BatchMode=yes '
        '-o StrictHostKeyChecking=yes -o ConnectTimeout=10 '
        '-o UserKnownHostsFile=/home/pnord/fifth-lattice-gpu/github_known_hosts')
    environment.update(env or {})
    result = subprocess.run(['git', '--git-dir', str(ROOT / 'repository.git'), *args],
                            input=data, capture_output=True, text=True,
                            env=environment, timeout=45)
    if check and result.returncode:
        raise RuntimeError(f'git {args[0]} failed: {result.stderr.strip()}')
    return result


def push_files(files, message):
    if not (ROOT / 'repository.git/HEAD').exists():
        git('init', '--bare', str(ROOT / 'repository.git'))
    # Build each commit on the latest remote tree. There is no search worktree,
    # no reset/rebase of user files, and no force push. Retry concurrent updates.
    for attempt in range(3):
        git('fetch', '--depth=1', REMOTE, 'refs/heads/' + BRANCH)
        parent = git('rev-parse', 'FETCH_HEAD').stdout.strip()
        old = git('show', f'{parent}:{LEGACY}').stdout
        marker = '<!-- current-weekend-search -->'
        candidate = dict(files)
        if marker not in old:
            candidate[LEGACY] = (marker + '\n> **Current search:** '
                '[16-worker weekend continuation](../weekend-20261106/STATUS.md), '
                'with 15-minute updates through Monday, November 9. '
                'The page below is the historical overnight run.\n\n' + old)
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            env = {'GIT_INDEX_FILE': str(Path(temporary) / 'index')}
            git('read-tree', parent, env=env)
            for path, content in candidate.items():
                digest = git('hash-object', '-w', '--stdin', data=content).stdout.strip()
                git('update-index', '--add', '--cacheinfo', '100644', digest, path, env=env)
            tree = git('write-tree', env=env).stdout.strip()
            commit = git('commit-tree', tree, '-p', parent, data=message + '\n').stdout.strip()
        pushed = git('push', '--porcelain', REMOTE,
                     f'{commit}:refs/heads/{BRANCH}', check=False)
        if pushed.returncode == 0:
            return commit
        # Only retry a conflicting branch advance. Preserve transport/auth errors.
        remote = git('ls-remote', REMOTE, 'refs/heads/' + BRANCH).stdout.split()
        if not remote or remote[0] == parent or attempt == 2:
            raise RuntimeError('GitHub push failed: ' + pushed.stderr.strip())
    raise RuntimeError('Concurrent branch updates exhausted publication attempts')


def publish(row):
    files = {PUBLIC + '/STATUS.md': markdown(row),
             PUBLIC + '/status.json': json.dumps(row, indent=2) + '\n'}
    evidence = ROOT / 'published-evidence'
    if evidence.exists():
        for path in sorted(evidence.rglob('*')):
            if path.is_file() and not path.is_symlink():
                files[PUBLIC + '/precision/' + str(path.relative_to(evidence))] = path.read_text()
    commit = push_files(files, 'Update weekend fifth-power search progress: ' + row['snapshot_utc'])
    receipt = dict(status='published', commit=commit, published_utc=utc(),
                   snapshot_utc=row['snapshot_utc'], phase=row['phase'],
                   next_patch=row['checkpoint']['next_patch'], url=URL)
    atomic(ROOT / 'last-push.json', receipt)
    print(json.dumps(receipt), flush=True)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    if args.preview:
        print(markdown(snapshot()))
        return 0
    with (ROOT / 'publisher.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        next_push = 0
        receipt_path = ROOT / 'last-push.json'
        if not args.once and receipt_path.exists():
            receipt = json.loads(receipt_path.read_text())
            next_push = datetime.fromisoformat(receipt['published_utc']).timestamp() + INTERVAL
        terminal_since = None
        while True:
            try:
                row = snapshot()
                terminal = row['phase'] == 'stopped'
                if terminal:
                    terminal_since = terminal_since or time.monotonic()
                else:
                    terminal_since = None
                settled = terminal and time.monotonic() - terminal_since >= 15
                if args.once or settled or (not terminal and time.time() >= next_push):
                    publish(row)
                    if args.once or settled:
                        return 0
                    next_push = time.time() + INTERVAL
            except Exception as error:
                atomic(ROOT / 'last-error.json', dict(utc=utc(), error=str(error)))
                print(json.dumps(dict(error=str(error), utc=utc())), flush=True)
                if args.once:
                    return 1
            if time.time() >= FINAL_LIMIT:
                atomic(ROOT / 'last-error.json', dict(
                    utc=utc(), error='Publisher deadline passed before a final snapshot was confirmed'))
                return 3
            time.sleep(30)


if __name__ == '__main__':
    raise SystemExit(main())
