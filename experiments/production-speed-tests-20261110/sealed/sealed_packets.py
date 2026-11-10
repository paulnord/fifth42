"""Experimental process-local seal for canonical packets; never a disk/IPC trust token.

Call seal() only on a prepared chunk registered by buffered_pipeline.prepare_cached.
The existing canonical validator runs once. Subsequent checks bind every scientific
field and the exact immutable native packet. No hashes/encoding are repeated.
This detects ordinary replacement and frozen-dataclass bypass mutation; it is not
a defense against malicious code with access to this process or memory faults.
"""
from dataclasses import fields
import threading
import weakref


def immutable(x):
    if type(x) in (int, str, bytes, bool, type(None)):
        return
    if type(x) is not tuple:
        raise ValueError('Seal contains mutable scientific state')
    for y in x:
        immutable(y)


def snapshot(chunk):
    """Capture values, not references to mutable dataclasses; exclude timing only."""
    w, p = chunk.window, chunk.plan
    window = tuple((f.name, getattr(w, f.name)) for f in fields(w))
    batches = tuple((tuple(tuple(getattr(t, f.name) for f in fields(t))
                           for t in b.tasks), b.packet, b.points)
                    for b in p.batches)
    plan = (p.bound, p.cap, batches, p.direct_hits, p.tasks, p.points,
            p.certificate_sha256)
    result = (window, plan, chunk.patches, chunk.geometry_sha256, chunk.payload_bytes)
    return result


class PacketSeals:
    def __init__(self, canonical_validator):
        self.canonical_validator = canonical_validator
        self._entries = {}
        self._lock = threading.Lock()

    def seal(self, chunk):
        # Canonical validation may be expensive: benchmark this setup separately.
        self.canonical_validator(chunk)
        state = snapshot(chunk)
        immutable(state)
        if chunk.plan.bound != chunk.window.hi or chunk.plan.cap != chunk.window.cap:
            raise ValueError('Plan/window bound or cap mismatch')
        # Check packet type exactly so user-defined equality cannot bypass checks.
        for batch in chunk.plan.batches:
            if type(batch.packet) is not str:
                raise ValueError('Packet is not immutable native text')
        key = id(chunk)
        def cleanup(ref):
            with self._lock:
                entry = self._entries.get(key)
                if entry is not None and entry[0] is ref:
                    del self._entries[key]
        ref = weakref.ref(chunk, cleanup)
        with self._lock:
            self._entries[key] = (ref, state)
        return chunk

    def validate(self, chunk):
        with self._lock:
            entry = self._entries.get(id(chunk))
        if entry is None or entry[0]() is not chunk:
            raise ValueError('No local packet seal; validate/reseal after IPC or disk load')
        if snapshot(chunk) != entry[1]:
            raise ValueError('Scientific state or native packet changed after sealing')

    def __len__(self):
        with self._lock:
            return len(self._entries)
