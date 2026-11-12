"""Acquire the original parent only after the admitted r3 generation retires."""
import argparse
import fcntl
import os
from pathlib import Path
import signal
import subprocess
import time

import extension_guard as guard


def unit(name):
    result = subprocess.run(['systemctl', '--user', 'show', name, '-p', 'ActiveState', '-p', 'MainPID'],
                            text=True, capture_output=True, check=True, timeout=5)
    return dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)


class Coordinator:
    def __init__(self, path, expected, inventory_sha256, test=False):
        self.path, self.expected = Path(path), expected
        self.inventory_sha256, self.test = inventory_sha256, test
        self.g = guard.load_grant(path, expected, test)
        guard.require(guard.sha(__file__) == self.g['coordinator_source_sha256'],
                      'Frozen extension coordinator changed')
        self.fd = None

    def predecessor_clear(self):
        g = self.g
        if time.time() < g['cutover_not_before_epoch']:
            raise BlockingIOError('The admitted predecessor cutover has not arrived')
        owner = unit(g['predecessor_parent_service'])
        if owner.get('ActiveState') != 'inactive' or owner.get('MainPID') != '0':
            raise BlockingIOError('Original parent coordinator is still active')
        old = guard.predecessor(g)
        # Probe every predecessor child, including claims not reassigned by r4.
        # This is done before acquiring the parent lease, never from heartbeat.
        for row in old['assignments']:
            original = guard.claim(g['child_ledger'], row['job'])
            guard.require((original['first'], original['last'], original['sha256'], original['identity']) ==
                          (row['first'], row['last'], row['claim_sha256'], row['claim_identity']),
                          'Original predecessor child claim changed: ' + row['job'])
            child = Path(g['child_ledger']) / 'jobs' / row['job'] / 'journal.jsonl'
            if child.exists() and guard.locked_by_other(child):
                raise BlockingIOError('A predecessor child lease remains owned: ' + row['job'])

    def acquire(self):
        guard.require(self.fd is None, 'Parent lease already acquired')
        g = self.g
        guard.verify_mount(g['child_ledger'], self.test)
        self.predecessor_clear()
        inventory = guard.validate_inventory(g, self.inventory_sha256)
        guard.require(inventory['tasks'], 'No remaining work requires a successor parent owner')
        parent = guard.claim(g['parent_ledger'], g['parent_job'])
        guard.require((parent['sha256'], parent['first'], parent['last']) ==
                      (g['parent_claim_sha256'], g['parent_first'], g['parent_last']),
                      'Original parent reservation changed')
        self.reservations = {str(Path(g[key]) / 'reservations.jsonl'):
                             guard.sha(Path(g[key]) / 'reservations.jsonl')
                             for key in ('parent_ledger', 'child_ledger')}
        path = Path(g['parent_ledger']) / 'jobs' / g['parent_job'] / 'journal.jsonl'
        descriptor = os.open(path, os.O_RDWR | os.O_NOFOLLOW)
        try:
            fcntl.lockf(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BaseException:
            os.close(descriptor)
            raise
        self.fd = descriptor
        self.inode = (os.fstat(descriptor).st_dev, os.fstat(descriptor).st_ino)
        try:
            # Recheck source/coordinator quiescence across the acquisition edge.
            self.predecessor_clear()
            self.heartbeat()
            guard.atomic(self.path.parent / g['active_file'], dict(
                status='active_allocation_ready', grant_sha256=self.expected,
                inventory_sha256=self.inventory_sha256, stop_epoch=g['stop_epoch'],
                coordinator_pid=os.getpid(), activated_epoch=time.time(),
                predecessor_parent_service=g['predecessor_parent_service'],
                original_reservation_logs=self.reservations, coverage_claimed=False))
        except BaseException:
            self.close()
            raise

    def heartbeat(self):
        g = self.g
        guard.require(self.fd is not None and guard.sha(self.path) == self.expected,
                      'Frozen grant changed or original parent is not owned')
        guard.require(guard.sha(__file__) == g['coordinator_source_sha256']
                      and guard.sha(guard.__file__) == g['guard_source_sha256'],
                      'Frozen coordinator/guard source changed')
        guard.require(guard.sha(g['inventory_file']) == self.inventory_sha256, 'Sealed inventory changed')
        guard.require(guard.sha(g['predecessor_grant_file']) == g['predecessor_grant_sha256'],
                      'Original r3 grant changed')
        info = (Path(g['parent_ledger']) / 'jobs' / g['parent_job'] / 'journal.jsonl').stat()
        guard.require((info.st_dev, info.st_ino) == self.inode, 'Stable original parent lease inode changed')
        # Never reopen this parent's lease inode: closing another descriptor in
        # this process would release its POSIX record lock.
        for path, expected in self.reservations.items():
            guard.require(guard.sha(path) == expected, 'Original reservation log changed')
        guard.atomic(self.path.parent / g['state_file'], dict(
            status='active', grant_sha256=self.expected, inventory_sha256=self.inventory_sha256,
            stop_epoch=g['stop_epoch'], coordinator_pid=os.getpid(), updated_epoch=time.time(),
            TEST_ONLY=self.test))

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grant', required=True)
    parser.add_argument('--grant-sha256', required=True)
    parser.add_argument('--inventory-sha256', required=True)
    parser.add_argument('--wait', action='store_true')
    parser.add_argument('--test-only', action='store_true')
    args = parser.parse_args()
    guard.require(os.uname().nodename.split('.')[0] == 'ada', 'Extension parent belongs on Ada')
    coordinator = Coordinator(args.grant, args.grant_sha256, args.inventory_sha256, args.test_only)
    stopping = [False]
    signal.signal(signal.SIGTERM, lambda *_: stopping.__setitem__(0, True))
    signal.signal(signal.SIGINT, lambda *_: stopping.__setitem__(0, True))
    try:
        while not stopping[0] and time.time() < coordinator.g['stop_epoch'] - 60:
            try:
                coordinator.acquire()
                break
            except (FileNotFoundError, BlockingIOError) as error:
                if not args.wait:
                    raise
                guard.atomic(Path(args.grant).parent / 'WAITING.json', dict(
                    status='waiting_for_sealed_predecessor_or_original_parent',
                    reason=str(error), compute_started=False, updated_epoch=time.time()))
                time.sleep(2)
        while coordinator.fd is not None and not stopping[0] and time.time() < coordinator.g['stop_epoch'] + 1800:
            coordinator.heartbeat()
            time.sleep(1)
    finally:
        coordinator.close()


if __name__ == '__main__':
    main()
