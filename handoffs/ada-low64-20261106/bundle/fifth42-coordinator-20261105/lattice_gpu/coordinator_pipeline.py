"""Opt-in host pipeline experiment. Never imports or changes a live launcher.

Preparation can run ahead, but only exact decoded responses may be journaled.
All native mathematical guards and canonical certificate bytes are unchanged.
This module deliberately rejects sphere/guarded patches: a partial benchmark
window must fail, not be reported as completed coverage.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import fcntl
import hashlib
import json
import re
from pathlib import Path
import threading
import time

import overnight_search as night
import packing_opt
import coordinator_packing
import scaling_core as core


class GuardedPatch(ValueError):
    pass


class Stages:
    """Wall and current-thread CPU seconds; overlapping stages are not additive."""
    def __init__(self):
        self.values = {}

    @contextmanager
    def time(self, name):
        wall, cpu = time.perf_counter(), time.thread_time()
        try:
            yield
        finally:
            value = self.values.setdefault(name, {'wall_seconds': 0., 'thread_cpu_seconds': 0., 'calls': 0})
            value['wall_seconds'] += time.perf_counter() - wall
            value['thread_cpu_seconds'] += time.thread_time() - cpu
            value['calls'] += 1


def _prepare(spec):
    start, cpu = time.perf_counter(), time.process_time()
    task = core.prepare_task(spec)
    return task, time.perf_counter() - start, time.process_time() - cpu


def _certify(task):
    if not night.native_safe(task):
        raise GuardedPatch(f'Patch {task.id} needs the original sphere fallback; window is incomplete')
    start, cpu = time.perf_counter(), time.process_time()
    token = core.certify_task(task)
    return token, time.perf_counter() - start, time.process_time() - cpu


def prepare_certified(spec):
    """One worker round trip, retaining the original independent certification."""
    task, prepare_wall, prepare_cpu = _prepare(spec)
    token, certify_wall, certify_cpu = _certify(task)
    return task, token, (prepare_wall, prepare_cpu, certify_wall, certify_cpu)


@dataclass(frozen=True)
class Window:
    lo: int
    hi: int
    first: int
    last: int
    width: int = 8
    bits: int = 48
    cap: int = 42

    def specifications(self):
        return tuple(night.shell_specs(self.lo, self.hi, self.width, self.bits,
                                       self.first, self.last, self.cap))

    def identity(self):
        return dict(lo=self.lo, hi=self.hi, first=self.first, last=self.last,
                    width=self.width, bits=self.bits, cap=self.cap)


@dataclass(frozen=True)
class PreparedChunk:
    window: Window
    plan: core.VerifiedPlan
    # IDs are shell-relative, so consumers must retain the full window identity.
    patches: tuple
    geometry_sha256: str
    payload_bytes: int
    stages: dict
    worker_seconds: tuple


def prepare_chunk(pool, window, mode='baseline', map_chunksize=8):
    if mode not in ('baseline', 'fused', 'packed'):
        raise ValueError('Unknown preparation mode')
    if type(map_chunksize) is not int or map_chunksize < 1:
        raise ValueError('Invalid pool map chunksize')
    if not window.first < window.last:
        raise ValueError('Empty benchmark chunk')
    stages = Stages()
    with stages.time('specification'):
        specs = window.specifications()
    if mode == 'baseline':
        with stages.time('prepare_pool_map'):
            prepared = pool.map(_prepare, specs, map_chunksize)
        tasks = [row[0] for row in prepared]
        with stages.time('certify_pool_map'):
            certified = pool.map(_certify, tasks, map_chunksize)
        tokens = [row[0] for row in certified]
        durations = tuple((p[1], p[2], c[1], c[2]) for p, c in zip(prepared, certified))
    else:
        with stages.time('fused_pool_map'):
            rows = pool.map(prepare_certified, specs, map_chunksize)
        tasks = [row[0] for row in rows]
        tokens = [row[1] for row in rows]
        durations = tuple(row[2] for row in rows)
    if mode == 'packed':
        with stages.time('one_pass_certificate_geometry_hash_packet_encoding'):
            plan, geometry_digest, payload_bytes = coordinator_packing.assemble_with_geometry(
                window.hi, window.cap, specs, (), tasks, tokens)
    else:
        with stages.time('assembly_certificate_hash_packet_encoding'):
            plan = packing_opt.assemble(window.hi, window.cap, specs, (), tasks, tokens)
        with stages.time('geometry_hashing'):
            geometry = hashlib.sha256()
            payload_bytes = 0
            for task in tasks:
                payload = packing_opt.task_payload(task)
                geometry.update(payload)
                geometry.update(b'\n')
                payload_bytes += len(payload) + 1
            payload_bytes += sum(len(batch.packet.encode()) for batch in plan.batches)
        geometry_digest = geometry.hexdigest()
    return PreparedChunk(window, plan, tuple((t.id, token, t.points) for t, token in zip(tasks, tokens)),
                         geometry_digest, payload_bytes, stages.values, durations)


def partition(window, pieces):
    """Stable exact half-open partitions, never sum coordinator throughput rates."""
    if type(pieces) is not int or not 1 <= pieces <= window.last - window.first:
        raise ValueError('Invalid partition count')
    count = window.last - window.first
    edges = [window.first + count * i // pieces for i in range(pieces + 1)]
    return tuple(Window(window.lo, window.hi, a, b, window.width, window.bits, window.cap)
                 for a, b in zip(edges, edges[1:]))


def verify_partition(window, windows):
    cursor = window.first
    for item in windows:
        if (item.lo, item.hi, item.width, item.bits, item.cap) != (window.lo, window.hi, window.width, window.bits, window.cap):
            raise ValueError('Partition changed the exact geometry settings')
        if item.first != cursor or item.last <= item.first:
            raise ValueError('Partition has a gap, duplicate, or reordered range')
        cursor = item.last
    if cursor != window.last:
        raise ValueError('Partition does not cover the full window')


def audited_patch_ids(window, period=32768):
    """Schedule audits by global (shell, patch) identity, not coordinator counters."""
    if type(period) is not int or period < 1:
        raise ValueError('Invalid audit period')
    return tuple(i for i in range(window.first, window.last) if i % period == 0)


class OwnedEngine:
    """The constructing thread alone owns the existing sequential EngineSession."""
    def __init__(self, session):
        self.session = session
        self.owner = threading.get_ident()
        self.backend = session.backend

    def run(self, packet, timeout=60):
        if threading.get_ident() != self.owner:
            raise RuntimeError('EngineSession may only be used by its single owner')
        return self.session.run(packet, timeout=timeout)


def validate_chunk(chunk):
    tasks = tuple(task for batch in chunk.plan.batches for task in batch.tasks)
    core.checked_tasks(chunk.window.specifications(), tasks)
    expected = tuple((task.id, packing_opt.task_digest(task), task.points) for task in tasks)
    if expected != chunk.patches or chunk.plan.tasks != len(tasks):
        raise ValueError('Prepared plan does not match its per-patch manifest')
    if chunk.plan.points != sum(task.points for task in tasks):
        raise ValueError('Prepared plan total does not match its patches')
    for batch in chunk.plan.batches:
        if core.encode_batch(batch.tasks, chunk.window.cap) != batch:
            raise ValueError('Prepared packet differs from its exact tasks')
    if chunk.plan.direct_hits:
        raise ValueError('Selected windows cannot include unmanifested direct work')


def validate_response_types(response):
    # bool and integral floats compare equal to ints in Python. Native fields
    # must actually be integers before the existing exact/count checks run.
    if not isinstance(response, dict):
        raise ValueError('Engine response is not an object')
    if type(response.get('points_visited')) is not int:
        raise ValueError('Invalid native point count type')
    if not isinstance(response.get('counts'), list) or not isinstance(response.get('hits'), list):
        raise ValueError('Invalid native response arrays')
    for count in response['counts']:
        if not isinstance(count, dict) or any(type(count.get(key)) is not int for key in ('id', 'expected', 'visited')):
            raise ValueError('Invalid native per-patch count types')
    for hit in response['hits']:
        if not isinstance(hit, dict) or any(type(hit.get(key)) is not int for key in ('task', 'linear', 'a', 'b', 'c')):
            raise ValueError('Invalid native candidate types')


def execute_chunk(chunk, engine, *, trial, coordinator, timeout=60):
    """No commit occurs here. Failure of any complete-count/exact check aborts."""
    stages = Stages()
    with stages.time('prepared_plan_consistency'):
        validate_chunk(chunk)
    hits = set(chunk.plan.direct_hits)
    records = []
    for batch_id, batch in enumerate(chunk.plan.batches):
        identity = dict(trial=trial, coordinator=coordinator, window=chunk.window.identity(), batch=batch_id,
                        packet_sha256=hashlib.sha256(batch.packet.encode()).hexdigest())
        with stages.time('engine_rpc'):
            response, rpc_seconds = engine.run(batch.packet, timeout=timeout)
        with stages.time('exact_output_verification'):
            validate_response_types(response)
            hits |= core.decode_batch(batch, response, engine.backend)
        records.append(dict(identity=identity, points=batch.points, patch_ids=[t.id for t in batch.tasks], rpc_seconds=rpc_seconds,
                            response_sha256=hashlib.sha256(json.dumps(response, sort_keys=True,
                                                                    separators=(',', ':')).encode()).hexdigest()))
    return dict(window=chunk.window.identity(), patches=chunk.patches, points=chunk.plan.points,
                geometry_sha256=chunk.geometry_sha256, certificate_sha256=chunk.plan.certificate_sha256,
                hits=sorted(hits), complete=True, batches=records, stages=stages.values)


class TrialJournal:
    """Isolated, single-writer selected-window journal with durable prefix recovery.

    Identity must include a trial ID, exact source/binary hashes and window.
    Ahead-prepared work cannot call commit; only the serial engine owner does.
    No result from this selected-window experiment confers a full-box bound.
    """
    def __init__(self, directory, identity, window):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.lock = (self.directory / 'writer.lock').open('a+')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.poisoned = False
            self.owner = threading.get_ident()
            self.identity = identity
            self.window = window
            self.checkpoint = self.directory / 'checkpoint.json'
            self.journal = self.directory / 'coverage.jsonl'
            if self.checkpoint.exists():
                self.state = json.loads(self.checkpoint.read_text())
                if self.state['identity'] != identity or self.state['window'] != window.identity():
                    raise ValueError('Trial source, binary, configuration, or range changed')
            else:
                self.state = dict(identity=identity, window=window.identity(), next_patch=window.first,
                                  chunks=0, points=0, patches=0, hits=[], journal_offset=0,
                                  journal_sha256='0' * 64, completed_bound=None)
            night.verify_journal(self.journal, self.state)
            cursor = window.first
            points = 0
            hits = set()
            if self.journal.exists():
                for raw in self.journal.read_text().splitlines():
                    row = json.loads(raw)
                    self._validate(row, cursor)
                    cursor = row['window']['last']
                    points += row['points']
                    hits.update(map(tuple, row['hits']))
            if (cursor != self.state['next_patch'] or points != self.state['points'] or
                    self.state['patches'] != cursor - window.first or sorted(hits) != list(map(tuple, self.state['hits'])) or
                    self.state['completed_bound'] is not None):
                raise ValueError('Checkpoint totals or cursor disagree with committed coverage')
        except BaseException:
            self.lock.close()
            raise

    def _validate(self, record, cursor):
        item = Window(**record['window'])
        if (item.lo, item.hi, item.width, item.bits, item.cap) != (self.window.lo, self.window.hi, self.window.width, self.window.bits, self.window.cap):
            raise ValueError('Committed chunk changes window settings')
        if item.first != cursor or not item.first < item.last <= self.window.last:
            raise ValueError('Committed chunk has missing, duplicate, stale, or reordered patches')
        patches = record['patches']
        if any(type(p[0]) is not int for p in patches) or [p[0] for p in patches] != list(range(item.first, item.last)):
            raise ValueError('Per-patch manifest does not match the interval')
        if any(not isinstance(p[1], str) or re.fullmatch('[0-9a-f]{64}', p[1]) is None or type(p[2]) is not int or p[2] < 1 for p in patches):
            raise ValueError('Malformed patch certificate manifest')
        if record.get('complete') is not True or type(record['points']) is not int or record['points'] != sum(p[2] for p in patches):
            raise ValueError('Incomplete chunk cannot advance coverage')
        batches = record.get('batches', [])
        if (sum(b['points'] for b in batches) != record['points'] or
                [ident for b in batches for ident in b['patch_ids']] != [p[0] for p in patches]):
            raise ValueError('Executed batches do not cover the patch manifest')
        for batch_id, batch in enumerate(batches):
            if (batch['identity']['window'] != record['window'] or batch['identity']['batch'] != batch_id or
                    batch['identity']['trial'] != self.identity['trial']):
                raise ValueError('Executed batch has stale trial/range/sequence identity')

    def commit(self, record):
        if self.lock.closed:
            raise RuntimeError('Journal is closed')
        if self.poisoned:
            raise RuntimeError('Failed durable write: close and reopen for recovery before retrying')
        if threading.get_ident() != self.owner:
            raise RuntimeError('Only the journal owner may commit coverage')
        self._validate(record, self.state['next_patch'])
        raw, digest = night.encode_record(self.state['journal_sha256'],
                                         dict(record, sequence=self.state['chunks'] + 1))
        # Any append/replace/fsync failure has an uncertain durable outcome.
        # Never append again from stale in-memory state; reopening reconciles it.
        try:
            with self.journal.open('ab') as stream:
                stream.write(raw)
                stream.flush()
                import os
                os.fsync(stream.fileno())
                offset = stream.tell()
            state = dict(self.state, next_patch=record['window']['last'], chunks=self.state['chunks'] + 1,
                         points=self.state['points'] + record['points'],
                         patches=self.state['patches'] + len(record['patches']),
                         hits=sorted(set(map(tuple, self.state['hits'])) | set(map(tuple, record['hits']))),
                         journal_offset=offset, journal_sha256=digest)
            night.atomic_json(self.checkpoint, state)
        except BaseException:
            self.poisoned = True
            raise
        self.state = state

    def close(self):
        self.lock.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
