#!/usr/bin/env python3
"""Small independent reference: Python integers, no congruence filter.

Enumerate a <= b and use a dictionary of all fifth powers to find c >= b.
The production CPU/GPU staircase and their arithmetic are not used here.
"""
import argparse
import json


def reference(bound, target=42):
    if not 0 <= bound <= 500:
        raise ValueError('reference bound must be in [0,500]')
    powers = {n**5: n for n in range(-bound, bound + 1)}
    result = []
    for a in range(-bound, bound + 1):
        for b in range(a, bound + 1):
            c = powers.get(target - a**5 - b**5)
            if c is not None and c >= b:
                result.append([a, b, c])
    return result


def verify(hit, bound, target):
    if (len(hit) != 3 or any(type(n) is not int for n in hit)
            or any(abs(n) > bound for n in hit)):
        raise ValueError(f'invalid candidate: {hit}')
    if sum(n**5 for n in hit) != target:
        raise ValueError(f'candidate failed Python arbitrary-precision verification: {hit}')
    return tuple(sorted(hit))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound', type=int, required=True)
    ap.add_argument('--target', type=int, default=42)
    args = ap.parse_args()
    print(json.dumps({'bound': args.bound, 'target': args.target,
                      'hits': reference(args.bound, args.target)}))
