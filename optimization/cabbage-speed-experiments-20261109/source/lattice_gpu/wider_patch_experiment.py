#!/usr/bin/env python3
"""Local wider-box experiments; never changes the selected production width.

High-range comparisons use exactly [3/10, 3/10 + 2048/100000000001].
Widths 8,16,32,64,128 divide this same closed union into 256,128,64,32,16
patches. Here width means EXACT (right-left)*cmin, unlike the ordinary
rounded full-shell grid, whose count is ceil(.9*cmin/width). Adjacent closed
patches overlap only at their shared boundary; decoded hits are deduplicated.
A guard stops the entire trial, not just the offending patch. Geometry-only
success is not a coverage or performance claim. Timings require a separate,
exclusive run; this module does not acquire a benchmark resource lease.
"""
import argparse
from contextlib import contextmanager
from fractions import Fraction
import json
import os
from pathlib import Path
import time

import scaling_core as core
import packing_opt

WIDTHS = (8, 16, 32, 64, 128)
HIGH_LO = 100_000_000_001
HIGH_HI = 200_000_000_000
SPAN = 2048
LEFT = Fraction(3, 10)
RIGHT = LEFT + Fraction(SPAN, HIGH_LO)
GUARDS = frozenset((
    'Patch point allowance mismatch', 'Full-domain coefficient allowance exhausted',
    'Single task cannot fit a packet', 'Integer transform can overflow',
    'Invalid integer transform', 'Invalid coefficient bounds',
    'Full-domain task allowance exhausted', 'Packet task allowance exceeded',
    'Packet point allowance exceeded', 'Packet frame exceeds the finite byte allowance',
))


def pair(value):
    return value.numerator, value.denominator


def shared_specs(width, bits=None):
    """Exact nested partitions; no floating-point endpoints or rounded grids."""
    if type(width) is not int or width not in WIDTHS:
        raise ValueError('Unsupported shared-union width')
    bits = max(48, 5 * HIGH_HI.bit_length() + 32) if bits is None else bits
    if type(bits) is not int or bits < 48:
        raise ValueError('Invalid precision')
    return [(i, HIGH_LO, HIGH_HI, pair(LEFT + Fraction(i * width, HIGH_LO)),
             pair(LEFT + Fraction((i + 1) * width, HIGH_LO)), 42, bits)
            for i in range(SPAN // width)]


@contextmanager
def arithmetic_range(high=False):
    """Reuse the validated overnight denominator cap, restoring it afterwards.

    No native, coefficient, point, frame, transform or other guard is changed.
    Intended for sequential isolated experiment processes, not concurrent threads.
    """
    previous = core.MAX_BOUND
    core.MAX_BOUND = HIGH_HI if high else 32000
    try:
        yield
    finally:
        core.MAX_BOUND = previous


def prepare_trial(width, bound=100, cap=42, high=False):
    """Return (JSON-ready geometry report, complete certified plan or None)."""
    report = dict(width=width, regime='shared-high-union' if high else 'full-small-domain',
                  bound=HIGH_HI if high else bound, cap=42 if high else cap,
                  complete=False, coverage_complete=False, status='preparing')
    tasks = []
    try:
        with arithmetic_range(high):
            specifications, direct = (shared_specs(width), []) if high else core.specs(bound, cap, width)
            report['requested_patches'] = len(specifications)
            if high:
                report.update(cmin=HIGH_LO, left=pair(LEFT), right=pair(RIGHT),
                              width_definition='exact ratio width multiplied by cmin',
                              not_full_shell=True, bits=specifications[0][-1])
            tokens = []
            for spec in specifications:
                task = core.prepare_task(spec)
                tasks.append(task)
                tokens.append(core.certify_task(task))
            plan = packing_opt.assemble(report['bound'], report['cap'], specifications,
                                        direct, tasks, tokens)
            for batch in plan.batches:
                if len(batch.packet.encode()) > 16 * 1024 * 1024:
                    raise ValueError('Packet frame exceeds the finite byte allowance')
            report.update(status='geometry_certified', complete=True, points=plan.points,
                          patches=plan.tasks, batches=len(plan.batches),
                          largest_patch_points=max((t.points for t in tasks), default=0),
                          certificate_sha256=plan.certificate_sha256)
            return report, plan
    except ValueError as error:
        if str(error) not in GUARDS:
            raise
        report.update(status='incomplete_guard', error=str(error),
                      prepared_patches=len(tasks),
                      prepared_points=sum(t.points for t in tasks),
                      guarded_patch_id=tasks[-1].id if tasks else None)
        return report, None


def independent_oracle(bound, cap):
    """Independent exhaustive Python integer oracle, deliberately small only."""
    if type(bound) is not int or not 1 <= bound <= 200:
        raise ValueError('Independent brute-force oracle bound outside [1,200]')
    if type(cap) is not int or not 0 <= cap <= 1_000_000:
        raise ValueError('Invalid oracle cap')
    powers = [x ** 5 for x in range(bound + 1)]
    return {(a, b, c, powers[a] + powers[b] - powers[c])
            for c in range(1, bound + 1) for b in range(1, c) for a in range(1, b + 1)
            if abs(powers[a] + powers[b] - powers[c]) <= cap}


def execute_trial(report, plan, session, expected=None):
    """Execute all batches, retaining EngineSession's frame/deadline guards.

    High-range equality across widths is a consistency check, not an independent
    full-domain oracle. Caller must provide the validated max-2e11 native engine.
    """
    result = dict(report, complete=False, coverage_complete=False)
    if plan is None:
        return result
    hits = set(plan.direct_hits)
    try:
        for batch in plan.batches:
            raw, _ = session.run(batch.packet)
            hits.update(core.decode_batch(batch, raw, session.backend))
    except (TimeoutError, ValueError) as error:
        if isinstance(error, ValueError) and str(error) not in GUARDS:
            raise
        result.update(status='incomplete_guard', error=str(error))
        return result
    if expected is not None and hits != expected:
        raise RuntimeError('Complete exact result differs from independent oracle')
    result.update(status='passed', complete=True, coverage_complete=True,
                  hits=sorted(hits), oracle_equal=None if expected is None else True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--high', action='store_true')
    parser.add_argument('--bound', type=int, default=100)
    parser.add_argument('--cap', type=int, default=42)
    parser.add_argument('--widths', type=int, nargs='+', default=list(WIDTHS))
    parser.add_argument('--execute-cpu', type=Path,
                        help='Opt-in execution; high union needs the validated 2e11 overlay binary')
    args = parser.parse_args()
    if __import__('sys').flags.optimize:
        parser.error('Exact checks require ordinary Python')
    source = Path(os.environ.get('SCALING_LATTICE_SOURCE',
                                 str(Path(__file__).resolve().parents[1] / 'lattice_prototype')))
    core.initialize(source)
    expected = None if args.high or not args.execute_cpu else independent_oracle(args.bound, args.cap)
    session = None
    try:
        if args.execute_cpu:
            from engine_session import EngineSession
            session = EngineSession([str(args.execute_cpu.resolve()), '--threads', '1'],
                                    'emulated', time.monotonic() + 300)
        rows = []
        for width in args.widths:
            report, plan = prepare_trial(width, args.bound, args.cap, args.high)
            if session:
                report = execute_trial(report, plan, session, expected)
            rows.append(report)
        if args.high and session:
            completed = [row for row in rows if row['coverage_complete']]
            if completed and any(row['hits'] != completed[0]['hits'] for row in completed):
                raise RuntimeError('Shared-union width results disagree')
        print(json.dumps(dict(trials=rows, all_complete=all(r['complete'] for r in rows),
                              timing_claim=False), indent=2))
        return 0 if all(r['complete'] for r in rows) else 2
    finally:
        if session:
            session.close()


if __name__ == '__main__':
    raise SystemExit(main())
