"""Rebatch contiguous prepared windows without executing or committing coverage.

Native packet limits remain unchanged. A source chunk may span multiple output
packets and a packet may span multiple source chunks. Callers must verify every
routed task before committing its original chunk, in original chunk order. This
module never changes coverage, sends packets, or changes the overnight launcher.
"""
from dataclasses import dataclass
import hashlib

import coordinator_pipeline as pipeline
import overnight_search as night
import packing_opt
import scaling_core as core

MAX_PACKET_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class PatchRoute:
    """Position in its route tuple is the packet-local native task ID."""
    chunk_index: int
    window: pipeline.Window
    patch_id: int
    certificate_sha256: str
    points: int


@dataclass(frozen=True)
class ChunkIdentity:
    window: pipeline.Window
    geometry_sha256: str
    certificate_sha256: str
    patch_count: int
    points: int


@dataclass(frozen=True)
class AggregatedPlan:
    batches: tuple
    routes: tuple
    chunks: tuple
    points: int


def aggregate_batches(chunks, *, max_tasks=core.MAX_TASKS,
                      max_points=core.MAX_POINTS,
                      max_packet_bytes=MAX_PACKET_BYTES):
    """Return ordered packets and immutable routing metadata for exact chunks.

    Limits may tighten, never enlarge, the existing native descriptor, point,
    and EngineSession packet-payload byte limits. Frame headers are outside the
    payload allowance, matching EngineSession.run. No padding or task splitting
    is performed. Input must be nonempty, contiguous, and share shell/settings.
    Trial/coordinator identity remains the caller's responsibility. Retaining
    this plan does not mean any original chunk has completed. This function
    materializes its input; callers must supply a finite, bounded ready window.
    """
    for name, value, ceiling in (('max_tasks', max_tasks, core.MAX_TASKS),
                                 ('max_points', max_points, core.MAX_POINTS),
                                 ('max_packet_bytes', max_packet_bytes, MAX_PACKET_BYTES)):
        if type(value) is not int or not 1 <= value <= ceiling:
            raise ValueError(f'{name} must be an integer in [1, {ceiling}]')
    chunks = tuple(chunks)
    if not chunks:
        raise ValueError('At least one prepared chunk is required')
    first, last = chunks[0].window, chunks[-1].window
    combined = pipeline.Window(first.lo, first.hi, first.first, last.last,
                               first.width, first.bits, first.cap)
    pipeline.verify_partition(combined, tuple(chunk.window for chunk in chunks))
    batches, routes, identities = [], [], []
    pending, pending_routes, pending_points = [], [], 0

    def flush():
        # Encode once in the usual case. A small configured byte cap uses a
        # monotonic prefix search, avoiding quadratic per-descriptor encoding.
        offset = 0
        while offset < len(pending):
            remaining = pending[offset:]
            batch = core.encode_batch(remaining, first.cap)
            count = len(remaining)
            if len(batch.packet.encode()) > max_packet_bytes:
                single = core.encode_batch(remaining[:1], first.cap)
                if len(single.packet.encode()) > max_packet_bytes:
                    raise ValueError('Single task exceeds packet byte limit')
                low, high, batch = 1, count - 1, single
                while low < high:
                    middle = (low + high + 1) // 2
                    candidate = core.encode_batch(remaining[:middle], first.cap)
                    if len(candidate.packet.encode()) <= max_packet_bytes:
                        low, batch = middle, candidate
                    else:
                        high = middle - 1
                count = low
            batches.append(batch)
            routes.append(tuple(pending_routes[offset:offset + count]))
            offset += count

    for chunk_index, chunk in enumerate(chunks):
        pipeline.validate_chunk(chunk)
        if (chunk.plan.bound, chunk.plan.cap) != (chunk.window.hi, chunk.window.cap):
            raise ValueError('Prepared plan bound/cap differs from source window')
        geometry = hashlib.sha256()
        payload_bytes = 0
        certificates = []
        for batch in chunk.plan.batches:
            for task in batch.tasks:
                payload = packing_opt.task_payload(task)
                geometry.update(payload)
                geometry.update(b'\n')
                payload_bytes += len(payload) + 1
                certificates.append(hashlib.sha256(payload).hexdigest())
                if type(task.points) is not int or task.points < 1 or not night.native_safe(task):
                    raise ValueError('Task violates unchanged native patch guards')
                if task.points > max_points:
                    raise ValueError('Single task exceeds configured point limit')
                if pending and (len(pending) == max_tasks or pending_points + task.points > max_points):
                    flush()
                    pending, pending_routes, pending_points = [], [], 0
                pending.append(task)
                pending_routes.append(PatchRoute(chunk_index, chunk.window, task.id,
                                                 certificates[-1], task.points))
                pending_points += task.points
        payload_bytes += sum(len(batch.packet.encode()) for batch in chunk.plan.batches)
        certificate = hashlib.sha256(('\n'.join(certificates) + '\n').encode()).hexdigest()
        if (geometry.hexdigest() != chunk.geometry_sha256 or
                certificate != chunk.plan.certificate_sha256 or payload_bytes != chunk.payload_bytes):
            raise ValueError('Prepared geometry/certificate/byte manifest was changed')
        identities.append(ChunkIdentity(chunk.window, chunk.geometry_sha256,
                                        certificate, len(certificates), chunk.plan.points))
    flush()
    return AggregatedPlan(tuple(batches), tuple(routes), tuple(identities),
                          sum(chunk.points for chunk in identities))
