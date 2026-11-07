#!/usr/bin/env python3
"""CPU-local 1x4 / 2x2 analog, not an ADA or GPU performance result."""
import argparse
import hashlib
import json
import multiprocessing as mp
from multiprocessing.connection import wait
import os
from pathlib import Path
import statistics
import sys
import time
import uuid

import coordinator_benchmark as helpers
import coordinator_pipeline as pipe
from engine_session import EngineSession
import exact_host_opt
import host_optimization_benchmark as host
import overnight_search as night
import scaling_core as core

WINDOW = pipe.Window(100000000001, 200000000000, 3751385984, 3751387008, bits=222)
MAX_CHUNK_BYTES = 8 * 1024 * 1024


def leaf_initialize(source, cpus):
    # Preserve core's parent-lifetime guard and dependency pins, but do not use
    # its outer-process identity for nested Pool worker affinity.
    exact_host_opt.initialize(source, (), 'combined')
    identity = mp.current_process()._identity
    if not identity or not cpus:
        raise RuntimeError('Expected a fresh leaf worker with assigned CPUs')
    os.sched_setaffinity(0, {cpus[(identity[-1] - 1) % len(cpus)]})


def identity(trial, coordinator, window, batch):
    return dict(trial=trial, coordinator=coordinator, window=window.identity(), batch=batch)


def check_identity(actual, expected):
    # JSON equality alone admits bool/int substitutions.
    if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError('Stale, reordered or mismatched broker identity')


def receive(connection, deadline):
    if not connection.poll(max(0., deadline - time.monotonic())):
        raise TimeoutError('Coordinator broker deadline')
    return connection.recv()


class RemoteEngine:
    backend = 'emulated'

    def __init__(self, connection, trial, coordinator, chunk, deadline):
        self.connection, self.trial, self.coordinator = connection, trial, coordinator
        self.chunk, self.deadline, self.index = chunk, deadline, 0

    def run(self, packet, timeout=60):
        i = self.index
        expected = identity(self.trial, self.coordinator, self.chunk.window, i)
        batch = self.chunk.plan.batches[i]
        if packet != batch.packet:
            raise ValueError('Remote packet changed')
        self.connection.send(dict(kind='batch', identity=expected, batch=batch,
                                  batches=len(self.chunk.plan.batches)))
        response = receive(self.connection, min(self.deadline, time.monotonic() + timeout))
        check_identity(response['identity'], expected)
        if response['kind'] != 'result':
            raise ValueError('Unexpected broker response')
        self.index += 1
        return response['response'], response['rpc_seconds']


def coordinator(connection, args, trial, number, window, cpus, deadline):
    os.sched_setaffinity(0, set(cpus))
    night.initialize(args.source)  # guards and exact decoder, no worker pinning
    pool = mp.get_context('spawn').Pool(len(cpus), initializer=leaf_initialize,
                                        initargs=(args.source, cpus))
    try:
        limited = helpers.DeadlinePool(pool, deadline)
        warmed = {}
        while len(warmed) < len(cpus):
            warmed.update(limited.map(core.worker_identity, range(len(cpus) * 4), 1))
        if sorted(a[0] for a in warmed.values()) != sorted(cpus) or any(len(a) != 1 for a in warmed.values()):
            raise RuntimeError('Leaf workers do not occupy the assigned disjoint CPU subset')
        control = identity(trial, number, window, -1)
        connection.send(dict(kind='ready', identity=control, workers=warmed,
                             affinity=sorted(os.sched_getaffinity(0))))
        message = receive(connection, deadline)
        check_identity(message['identity'], control)
        if message['kind'] != 'start':
            raise ValueError('Unexpected start message')
        rows = []
        with pipe.TrialJournal(args.output / trial / str(number),
                               dict(trial=trial, coordinator=number, source_identity=args.fingerprint), window) as journal:
            for part in helpers.chunks(window, 256):
                plan, info, durations = host.preparation(limited, part.specifications(), part.hi, part.cap)
                if info['payload_bytes'] > MAX_CHUNK_BYTES:
                    raise ValueError('Chunk byte bound exceeded')
                chunk = pipe.PreparedChunk(part, plan, info['patches'], info['geometry_sha256'],
                                           info['payload_bytes'], {}, durations)
                engine = RemoteEngine(connection, trial, number, chunk, deadline)
                result = pipe.execute_chunk(chunk, engine, trial=trial, coordinator=number,
                                            timeout=max(.001, deadline-time.monotonic()))
                journal.commit(result)
                rows.append(dict(record=result, preparation=info,
                                 packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in plan.batches]))
        connection.send(dict(kind='done', identity=control, rows=rows))
        pool.close()
        pool.join()
    finally:
        pool.terminate()
        pool.join()
        connection.close()


class Sequence:
    def __init__(self, trial, number, window):
        self.trial, self.number = trial, number
        self.parts = helpers.chunks(window, 256)
        self.window_index = self.batch_index = 0
        self.batch_count = None

    def accept(self, message):
        if self.window_index >= len(self.parts):
            raise ValueError('Duplicate completed chunk')
        part = self.parts[self.window_index]
        check_identity(message['identity'], identity(self.trial, self.number, part, self.batch_index))
        count = message['batches']
        if type(count) is not int or not 1 <= count <= 256:
            raise ValueError('Invalid bounded batch count')
        if self.batch_count is not None and count != self.batch_count:
            raise ValueError('Batch count changed within chunk')
        self.batch_count = count
        self.batch_index += 1
        if self.batch_index == count:
            self.window_index += 1
            self.batch_index = 0
            self.batch_count = None

    def finished(self):
        return self.window_index == len(self.parts) and self.batch_index == 0


def trial(args, count, repeat):
    began = time.perf_counter()
    deadline = min(time.monotonic() + 60, args.deadline)
    name = f'{count}x{4//count}-{repeat}-{uuid.uuid4().hex}'
    windows = pipe.partition(WINDOW, count)
    pipe.verify_partition(WINDOW, windows)
    processes, connections, ready, rows = [], [], [], []
    session = None
    broker_cpu = native_rpc = 0.
    try:
        for number, window in enumerate(windows):
            parent, child = mp.get_context('spawn').Pipe()
            cpus = args.cpus[number * (4//count):(number+1) * (4//count)]
            process = mp.get_context('spawn').Process(target=coordinator,
                args=(child, args, name, number, window, cpus, deadline))
            process.start()
            child.close()
            processes.append(process)
            connections.append(parent)
        for number, connection in enumerate(connections):
            message = receive(connection, deadline)
            check_identity(message['identity'], identity(name, number, windows[number], -1))
            if message['kind'] != 'ready':
                raise ValueError('Missing ready barrier')
            ready.append(message)
        session = EngineSession([str(args.engine), '--threads', '1'], 'emulated', deadline)
        engine = pipe.OwnedEngine(session)
        engine_affinity = sorted(os.sched_getaffinity(session.process.pid))
        if engine_affinity != list(args.cpus):
            raise RuntimeError('Native engine escaped shared CPU budget')
        startup = time.perf_counter() - began
        started = time.perf_counter()
        for number, connection in enumerate(connections):
            connection.send(dict(kind='start', identity=identity(name, number, windows[number], -1)))
        active = set(connections)
        sequences = [Sequence(name, n, w) for n, w in enumerate(windows)]
        while active:
            available = wait(active, timeout=max(0., deadline-time.monotonic()))
            if not available:
                raise TimeoutError('Broker trial deadline')
            for connection in available:
                cpu = time.process_time()
                message = connection.recv()
                number = connections.index(connection)
                if message['kind'] == 'done':
                    check_identity(message['identity'], identity(name, number, windows[number], -1))
                    if not sequences[number].finished():
                        raise ValueError('Premature completion')
                    rows.extend(message['rows'])
                    active.remove(connection)
                elif message['kind'] == 'batch':
                    sequences[number].accept(message)
                    batch = message['batch']
                    if core.encode_batch(batch.tasks, WINDOW.cap) != batch:
                        raise ValueError('Broker packet integrity check failed')
                    response, rpc = engine.run(batch.packet, timeout=max(.001, deadline-time.monotonic()))
                    native_rpc += rpc
                    connection.send(dict(kind='result', identity=message['identity'], response=response, rpc_seconds=rpc))
                else:
                    raise ValueError('Unexpected broker request')
                broker_cpu += time.process_time()-cpu
        steady = time.perf_counter()-started
        for process in processes:
            process.join(timeout=max(0., deadline-time.monotonic()))
            if process.exitcode != 0:
                raise RuntimeError('Coordinator failed or did not terminate')
        session.close()
        session = None
        rows.sort(key=lambda r: r['record']['window']['first'])
        pipe.verify_partition(WINDOW, [pipe.Window(**r['record']['window']) for r in rows])
        return dict(trial=name, coordinators=count, repeat=repeat, startup_seconds=startup,
                    steady_seconds=steady, total_seconds=time.perf_counter()-began,
                    broker_control_cpu_seconds=broker_cpu, native_rpc_wall_seconds=native_rpc,
                    cpus=args.cpus, engine_affinity=engine_affinity, ready=ready, rows=rows,
                    signature=[dict(window=r['record']['window'], patches=r['record']['patches'],
                        geometry=r['record']['geometry_sha256'], certificate=r['record']['certificate_sha256'],
                        hits=r['record']['hits'], packets=r['packets']) for r in rows],
                    points=sum(r['record']['points'] for r in rows), cuda_executed=False,
                    coverage_claim='Selected 1024 patches only; no full-box bound')
    finally:
        if session:
            session.close()
        for process in processes:
            if process.is_alive():
                process.terminate()
            process.join()
        for connection in connections:
            connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent.parent/'lattice_prototype')
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=5)
    args = parser.parse_args()
    if sys.flags.optimize or not 1 <= args.repeats <= 5:
        parser.error('Ordinary Python and 1..5 repeats required')
    args.cpus = tuple(sorted(os.sched_getaffinity(0))[:4])
    if len(args.cpus) != 4:
        parser.error('Four allowed CPUs required')
    os.sched_setaffinity(0, set(args.cpus))
    night.initialize(args.source)
    args.fingerprint = helpers.source_identity(args.source, args.engine)
    args.deadline = time.monotonic() + 120
    args.output.mkdir(parents=True, exist_ok=False)
    results, expected = [], None
    for repeat in range(args.repeats):
        for count in ((1, 2) if repeat % 2 == 0 else (2, 1)):
            result = trial(args, count, repeat)
            if expected is None:
                expected = result['signature']
            elif expected != result['signature']:
                raise RuntimeError('Exact original coverage union changed')
            results.append(result)
            night.atomic_json(args.output/f'{repeat}-{count}.json', result)
            print(json.dumps({k: result[k] for k in ('coordinators','repeat','steady_seconds','total_seconds','points')}), flush=True)
    summary = dict(status='passed', cpu_local_analog_only=True, cuda_executed=False,
        exact_union_equal=True, repeats=args.repeats,
        modes={str(count): {key: statistics.median(r[key] for r in results if r['coordinators']==count)
            for key in ('startup_seconds','steady_seconds','total_seconds','broker_control_cpu_seconds','native_rpc_wall_seconds')}
            for count in (1,2)})
    night.atomic_json(args.output/'summary.json', summary)


if __name__ == '__main__':
    main()
