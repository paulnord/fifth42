"""Isolated exact host arithmetic candidates; no production module edits.

B = U A and A is the explicit triangular tangent-patch basis. Since U is
unimodular, B^-1 = A^-1 U^-1. Constructing that inverse from the patch avoids
large rational cofactors of B. The original exact B * B^-1 == I check remains.
"""
import hashlib
from math import prod
import time

import overnight_search as night
import scaling_core as core

_MODE = None
MODES = ('reference', 'roots', 'inverse', 'combined')


def initialize(source, cpus=(), mode='reference'):
    global _MODE
    if mode not in MODES:
        raise ValueError('Unknown exact host arithmetic candidate')
    if _MODE is not None and _MODE != mode:
        raise RuntimeError('Do not change arithmetic mode inside a worker')
    if mode in ('roots', 'combined'):
        import exact_root_opt
        exact_root_opt.initialize(source, cpus)
    else:
        core.initialize(source, cpus)
    core.MAX_BOUND = night.MAX_BASE
    _MODE = mode


def coefficient_bounds_from_patch(patch, reduced, transform):
    l = core.lattice()
    determinant = l.det3(transform)
    if determinant not in (-1, 1):
        raise ValueError('Transform is not unimodular')
    inverse_u = [[(transform[(j+1)%3][(i+1)%3]*transform[(j+2)%3][(i+2)%3]
                  - transform[(j+1)%3][(i+2)%3]*transform[(j+2)%3][(i+1)%3]) // determinant
                  for j in range(3)] for i in range(3)]
    d, h = patch.cmax, (patch.right-patch.left)/2
    inverse = [
        [d*(inverse_u[0][j] + patch.p*inverse_u[1][j] + patch.q*inverse_u[2][j]) for j in range(3)],
        [d*h*(inverse_u[1][j] + patch.m*inverse_u[2][j]) for j in range(3)],
        [d*patch.eps*inverse_u[2][j] for j in range(3)],
    ]
    if l.matmul(reduced, inverse) != [[int(i == j) for j in range(3)] for i in range(3)]:
        raise ValueError('Exact inverse certificate failed')
    return tuple(core.ceil_sqrt(3*sum(inverse[i][j]**2 for i in range(3))) for j in range(3))


def bounds(patch, reduced, transform):
    if _MODE in ('inverse', 'combined'):
        return coefficient_bounds_from_patch(patch, reduced, transform)
    return core.coefficient_bounds(reduced)


def prepare_task(spec):
    ident, lo, hi, left, right, cap, bits = spec
    l = core.lattice()
    patch = l.make_patch(lo, hi, l.Q(*left), l.Q(*right), cap, bits)
    a = patch.basis()
    b, u = l.reduce_basis(a, 'fpylll')
    j = bounds(patch, b, u)
    return core.Task(ident, lo, hi, left, right, cap, bits,
                     tuple(tuple(int(x) for x in row) for row in u),
                     j, prod(2*x+1 for x in j), core.wire(a), core.wire(b))


def certify_task(task):
    # These are the same independent guards/reconstructions as scaling_core.
    l = core.lattice()
    if not 1 <= task.cmin <= task.cmax <= core.MAX_BOUND:
        raise ValueError('Invalid certified denominator interval')
    if len(task.U) != 3 or any(len(row) != 3 for row in task.U):
        raise ValueError('Invalid transform shape')
    if len(task.J) != 3 or any(type(j) != int or not 0 <= j <= core.MAX_I64//2 for j in task.J):
        raise ValueError('Invalid coefficient bounds')
    if any(type(x) != int or abs(x) > core.MAX_I64 for row in task.U for x in row):
        raise ValueError('Invalid integer transform')
    for col in range(3):
        if sum(task.J[i]*abs(task.U[i][col]) for i in range(3)) > core.MAX_I64:
            raise ValueError('Integer transform can overflow')
    points = prod(2*x+1 for x in task.J)
    if points != task.points or points > core.MAX_PATCH_POINTS:
        raise ValueError('Patch point allowance mismatch')
    a, b = core.read(task.A), core.read(task.B)
    # Rebuild independently, rather than reusing the preparation patch or inverse.
    patch = l.make_patch(task.cmin, task.cmax, l.Q(*task.left), l.Q(*task.right), task.cap, task.bits)
    if a != patch.basis() or abs(l.det3(task.U)) != 1 or l.matmul(task.U, a) != b:
        raise ValueError('Exact reduction certificate mismatch')
    if bounds(patch, b, task.U) != task.J:
        raise ValueError('Coefficient enclosure mismatch')
    return core.task_digest(task)


def prepare_certified(spec):
    start, cpu = time.perf_counter(), time.process_time()
    task = prepare_task(spec)
    prepare_wall, prepare_cpu = time.perf_counter()-start, time.process_time()-cpu
    if not night.native_safe(task):
        raise ValueError(f'Patch {task.id} needs sphere fallback; no benchmark coverage')
    start, cpu = time.perf_counter(), time.process_time()
    token = certify_task(task)
    return task, token, (prepare_wall, prepare_cpu, time.perf_counter()-start, time.process_time()-cpu)
