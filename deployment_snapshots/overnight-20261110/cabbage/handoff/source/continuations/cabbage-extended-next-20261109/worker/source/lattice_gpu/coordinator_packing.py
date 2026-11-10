"""One canonical serialization per task for certificate and geometry hashing.

This is experimental and separate from packing_opt. All its assembly guards,
packet grouping, exact direct work and plan certificate bytes are retained.
"""
import hashlib

import packing_opt
import scaling_core as core


def assemble_with_geometry(bound, cap, specifications, direct, tasks, certificates):
    core.checked_tasks(specifications, tasks)
    if len(certificates) != len(tasks) or any(len(x) != 64 for x in certificates):
        raise ValueError('Missing exact patch certificates')
    geometry = hashlib.sha256()
    payload_bytes = 0
    for task, certificate in zip(tasks, certificates):
        payload = packing_opt.task_payload(task)
        if hashlib.sha256(payload).hexdigest() != certificate:
            raise ValueError('Patch certificates do not identify the prepared immutable tasks')
        geometry.update(payload)
        geometry.update(b'\n')
        payload_bytes += len(payload) + 1
    total = sum(t.points for t in tasks)
    if total > core.MAX_TOTAL_POINTS:
        raise ValueError('Full-domain coefficient allowance exhausted')
    groups, pending, points = [], [], 0
    for task in tasks:
        if task.points > core.MAX_POINTS:
            raise ValueError('Single task cannot fit a packet')
        if pending and (len(pending) == core.MAX_TASKS or points + task.points > core.MAX_POINTS):
            groups.append(core.encode_batch(pending, cap))
            pending, points = [], 0
        pending.append(task)
        points += task.points
    if pending:
        groups.append(core.encode_batch(pending, cap))
    hits = []
    for lo, hi in direct:
        for c in range(lo, hi + 1):
            for b in range(1, c):
                for a in range(1, b + 1):
                    r = a**5 + b**5 - c**5
                    if abs(r) <= cap:
                        hits.append((a, b, c, r))
    digest = hashlib.sha256(('\n'.join(certificates) + '\n').encode()).hexdigest()
    plan = core.VerifiedPlan(bound, cap, tuple(groups), tuple(sorted(set(hits))), len(tasks), total, digest)
    payload_bytes += sum(len(batch.packet.encode()) for batch in plan.batches)
    return plan, geometry.hexdigest(), payload_bytes
