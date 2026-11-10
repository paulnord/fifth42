"""Experimental lossless Task transport, never an alternative certificate.

Workers still prepare and independently certify with coordinator_pipeline. The
parent reconstructs the original immutable Task and runs unchanged packed
assembly, specification binding, canonical hashes and packet guards. This is
only an in-process/owned-worker transport, not an authenticated certificate
loader. No pickle is read by this module. Nothing opts a launcher into it.
"""
import struct

import coordinator_pipeline as pipeline
import scaling_core as core

_MAGIC = b'LCT1'
_MAX_BYTES = 1024 * 1024


def encode_task(task):
    """Encode exact integers, sharing equal matrix denominators, not rounding."""
    if (len(task.U) != 3 or any(len(row) != 3 for row in task.U)
            or len(task.J) != 3 or len(task.left) != 2 or len(task.right) != 2
            or any(len(m) != 3 or any(len(row) != 3 for row in m)
                   for m in (task.A, task.B))):
        raise ValueError('Invalid compact task shape')
    values = [task.id, task.cmin, task.cmax, *task.left, *task.right,
              task.cap, task.bits, *(x for row in task.U for x in row),
              *task.J, task.points]
    pairs = [pair for matrix in (task.A, task.B) for row in matrix for pair in row]
    if any(len(pair) != 2 for pair in pairs):
        raise ValueError('Invalid compact rational shape')
    denominators = tuple(dict.fromkeys(pair[1] for pair in pairs))
    if any(type(d) is not int or d <= 0 for d in denominators):
        raise ValueError('Invalid compact denominator')
    values.extend(denominators)
    values.extend(pair[0] for pair in pairs)
    out = bytearray(_MAGIC + bytes([len(denominators)]))
    for value in values:
        if type(value) is not int:
            raise ValueError('Compact task requires exact integers')
        size = (value.bit_length() + 8) // 8
        if size > _MAX_BYTES or len(out) + 4 + size + 18 > _MAX_BYTES:
            raise ValueError('Compact task exceeds transport allowance')
        out.extend(struct.pack('>I', size))
        out.extend(value.to_bytes(size, 'big', signed=True))
    out.extend(denominators.index(pair[1]) for pair in pairs)
    return bytes(out)


def decode_task(blob):
    """Bounded structural decode; assembly must still verify the certificate."""
    if type(blob) is not bytes or not 5 <= len(blob) <= _MAX_BYTES or blob[:4] != _MAGIC:
        raise ValueError('Invalid compact task header')
    count = blob[4]
    if not 1 <= count <= 18:
        raise ValueError('Invalid denominator count')
    offset, values = 5, []
    for _ in range(22 + count + 18):
        if offset + 4 > len(blob):
            raise ValueError('Truncated compact integer length')
        size = struct.unpack_from('>I', blob, offset)[0]
        offset += 4
        if not 1 <= size <= len(blob) - offset:
            raise ValueError('Invalid compact integer size')
        value = int.from_bytes(blob[offset:offset + size], 'big', signed=True)
        if (value.bit_length() + 8) // 8 != size:
            raise ValueError('Noncanonical compact integer')
        values.append(value)
        offset += size
    if len(blob) - offset != 18:
        raise ValueError('Invalid compact task trailer')
    denominators = values[22:22 + count]
    if any(d <= 0 for d in denominators) or len(set(denominators)) != count:
        raise ValueError('Invalid compact denominators')
    indexes = blob[offset:]
    if any(i >= count for i in indexes):
        raise ValueError('Invalid compact denominator index')
    pairs = tuple((n, denominators[i]) for n, i in zip(values[22 + count:], indexes))
    matrices = tuple(tuple(pairs[start + row:start + row + 3] for row in (0, 3, 6))
                     for start in (0, 9))
    task = core.Task(*values[:3], tuple(values[3:5]), tuple(values[5:7]),
                     *values[7:9], tuple(tuple(values[i:i + 3]) for i in (9, 12, 15)),
                     tuple(values[18:21]), values[21], *matrices)
    return task


def prepare_certified_compact(spec):
    task, token, timings = pipeline.prepare_certified(spec)
    return encode_task(task), token, timings


class _CompactPool:
    def __init__(self, pool):
        self.pool = pool

    def map(self, function, specs, chunksize):
        if function is not pipeline.prepare_certified:
            raise ValueError('Compact adapter supports fused preparation only')
        rows = self.pool.map(prepare_certified_compact, specs, chunksize)
        return [(decode_task(blob), token, timings) for blob, token, timings in rows]


def prepare_chunk(pool, window, map_chunksize=8):
    """Opt-in bridge, retaining the existing packed assembler and every guard."""
    return pipeline.prepare_chunk(_CompactPool(pool), window, 'packed', map_chunksize)
