#!/usr/bin/env python3
"""Prepare a bounded distinct-coverage experiment. This program launches no search.

Novelty is relative to explicitly supplied prior certified regions, never a claim
that the available partial overnight evidence is a complete coverage ledger.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

import region_coverage as regions

C_MIN=100_000_000_001
C_MAX=200_000_000_000
BITS=222
SECONDS_PER_METHOD=60
MAX_TOTAL_SECONDS=180
RATIO_SPAN=Fraction(1_048_576,C_MIN)


def pair(value):
    value=Fraction(value)
    return [value.numerator,value.denominator]


def rational(value):
    return Fraction(*value)


def build_plan(previous=(), prior_exhaustive=False):
    methods=[]
    # These disjoint strips make new work the main objective. They are not a
    # controlled comparison of equal-difficulty regions or algorithm speedups.
    for width,left in ((32,Fraction(9,20)),(64,Fraction(11,20)),(128,Fraction(1,5))):
        scope=[regions.rectangle(C_MIN,C_MAX,pair(left),pair(left+RATIO_SPAN))]
        remaining=regions.difference(scope,previous)
        methods.append(dict(name=f'exact-combined-width-{width}',width=width,
            arithmetic='exact GMP roots + independently checked structured inverse',
            packing='one-pass canonical certificate/geometry bytes',
            seconds_budget=SECONDS_PER_METHOD,planned_scope=scope,remaining_scope=remaining,
            prior_overlap=regions.intersection(scope,previous),
            initial_accounting=regions.coverage_report(scope,previous=previous),
            checkpoint_policy='Commit only completely verified contiguous subregions; retain each exact rational endpoint',
            metric='New certified region union per total elapsed budget, not patch count'))
    return dict(schema=1,status='prepared_not_launched',purpose='Explore distinct certified geometric coverage',
        source_scope=dict(cmin=C_MIN,cmax=C_MAX,residual_cap=42,precision_bits=BITS),
        methods=methods,prior_coverage_is_exhaustive=bool(prior_exhaustive),
        novelty_scope='relative to supplied prior region ledger only',
        scheduler_boundary_policy='Prepare closed enclosures conservatively; report exact open/closed novelty boundaries and any endpoint overlap separately',
        prior_coverage=regions.canonical_union(previous),total_seconds_cap=MAX_TOTAL_SECONDS,
        max_cpu_workers=4,physical_core_topology_verified=False,gpu_owners=1,
        small_correctness_controls_only=True,main_budget_repeats_same_coverage=False,
        limits=dict(native_tasks_per_packet=4096,native_points_per_packet=50000000,
                    native_points_per_patch=10000000,native_frame_bytes=16777216,
                    prepared_chunk_patches=8,max_points_per_prepared_chunk=80000000,
                    ready_chunks=2,max_outstanding_chunks_including_active=3,
                    per_ready_chunk_canonical_bytes=8*1024*1024),
        prerequisites=[
            'Do not alter or overlap the live ADA overnight search or its final publisher.',
            'Before ADA execution, verify both have exited and acquire the normal CPU/GPU leases.',
            'Use a fresh scratch source/binary snapshot; validate CUDA and exact nonempty controls.',
            'Export and verify the available committed coverage prefix; subtract it before scheduling.',
            'If prior coverage is incomplete, report novelty only relative to supplied evidence.',
            'Budget includes fresh preparation, certification, encoding, queue waits, engine work, exact verification and durable commits.',
            'Check remaining wall budget before each task; stop incomplete work without advancing coverage.',
            'Record startup/shutdown and actual total time, guards, unfinished regions, overlaps and peak resources.',
        ],scope_warning='Different strips have different costs. Productivity in those strips is not a controlled speedup or a full-box bound.')


def iter_specifications(method, cap=42, bits=BITS):
    """Lazy exact tiling of remaining scope, truncating the last patch at its edge."""
    width=method['width']
    if type(width) is not int or width<1:raise ValueError('Invalid exact width')
    ident=0
    for rectangle in regions.canonical_union(method['remaining_scope']):
        lo,hi=rectangle['cmin'],rectangle['cmax']
        step=Fraction(width,lo)
        left,right=rational(rectangle['left']),rational(rectangle['right'])
        while left<right:
            end=min(left+step,right)
            yield (ident,lo,hi,tuple(pair(left)),tuple(pair(end)),cap,bits)
            ident+=1;left=end


def result_accounting(method, previous, committed, guarded=(), incomplete=(), elapsed_ns=0):
    if type(elapsed_ns) is not int or elapsed_ns<=0:
        raise ValueError('Positive exact elapsed nanoseconds are required')
    if regions.difference(committed,method['planned_scope']):
        raise ValueError('Committed coverage is outside the assigned method scope')
    report=regions.coverage_report(method['planned_scope'],previous,committed,guarded,incomplete)
    new=regions.difference(committed,previous)
    report.update(elapsed_ns=elapsed_ns,
        new_ratio_denominator_measure_per_second=pair(regions.measure(new)*1000000000/elapsed_ns),
        new_c_weighted_measure_per_second=pair(regions.measure(new,weighted=True)*1000000000/elapsed_ns),
        measures_are_geometric_not_integer_solution_counts=True,
        algorithm_speedup_claim=False,no_full_box_claim=True)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prior-regions',type=Path,help='JSON list of validated committed rectangles, never an active checkpoint')
    parser.add_argument('--prior-exhaustive',action='store_true',help='Declare that the supplied ledger is exhaustive for the planned strips')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    previous=json.loads(args.prior_regions.read_text()) if args.prior_regions else []
    if args.prior_exhaustive and not args.prior_regions:parser.error('Exhaustive prior evidence requires a supplied ledger')
    plan=build_plan(previous,args.prior_exhaustive)
    with args.output.open('x') as stream:json.dump(plan,stream,indent=2);stream.write('\n')
    print('Prepared plan only. No search, GPU request, service, or automation was launched.')


if __name__=='__main__':main()
