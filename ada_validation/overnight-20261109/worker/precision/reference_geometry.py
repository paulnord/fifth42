#!/usr/bin/env python3
"""Exact tangent-patch search. Python standard library only; see COVERAGE.md."""
from __future__ import annotations
import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction as Q
from math import isqrt
from time import perf_counter
from typing import Callable


class BudgetExceeded(RuntimeError):
    """No complete coverage result is returned after this exception."""


def floor(x: Q) -> int:
    return x.numerator // x.denominator


def ceil(x: Q) -> int:
    return -floor(-x)


def iroot(n: int, k: int = 5) -> int:
    """Floor nonnegative integer kth root, using integers only."""
    if n < 0 or k < 1:
        raise ValueError("nonnegative radicand and positive degree required")
    if n < 2:
        return n
    lo, hi = 0, 1 << ((n.bit_length() + k - 1) // k)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**k <= n:
            lo = mid
        else:
            hi = mid
    return lo


def root_bracket(x: Q, bits: int = 48) -> tuple[Q, Q]:
    """Outward dyadic bounds for a nonnegative fifth root."""
    if x < 0 or bits < 1:
        raise ValueError("invalid root enclosure input")
    d = 1 << bits
    n = iroot((x.numerator * d**5) // x.denominator)
    lo = Q(n, d)
    hi = lo if lo**5 == x else Q(n + 1, d)
    assert lo**5 <= x <= hi**5
    return lo, hi


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def gram_schmidt(b):
    star, norm = [], []
    mu = [[Q(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        v = list(b[i])
        for j in range(i):
            mu[i][j] = dot(b[i], star[j])/norm[j]
            v = [x-mu[i][j]*y for x, y in zip(v, star[j])]
        star.append(v)
        norm.append(dot(v, v))
        if norm[-1] == 0:
            raise ValueError("singular lattice basis")
    return mu, norm


def lll(basis):
    """Exact rational row-basis LLL, delta=3/4, with integer U: B=U*A."""
    b = [[Q(x) for x in r] for r in basis]
    u = [[int(i == j) for j in range(3)] for i in range(3)]
    k, steps = 1, 0
    while k < 3:
        steps += 1
        if steps > 10000:
            raise BudgetExceeded("LLL iteration guard; no coverage")
        for j in range(k-1, -1, -1):
            mu, norms = gram_schmidt(b)
            n = floor(mu[k][j]+Q(1, 2))
            if n:
                b[k] = [x-n*y for x, y in zip(b[k], b[j])]
                u[k] = [x-n*y for x, y in zip(u[k], u[j])]
        mu, norms = gram_schmidt(b)
        if norms[k] >= (Q(3, 4)-mu[k][k-1]**2)*norms[k-1]:
            k += 1
        else:
            b[k], b[k-1] = b[k-1], b[k]
            u[k], u[k-1] = u[k-1], u[k]
            k = max(k-1, 1)
    assert abs(det3(u)) == 1
    assert matmul(u, basis) == b
    return b, u


@dataclass
class Stats:
    patches: int = 0
    enumeration_nodes: int = 0
    sphere_points: int = 0
    box_points: int = 0
    exact_tests: int = 0
    direct_pairs: int = 0
    direct_candidates: int = 0
    seconds: float = 0.0


@dataclass
class Budget:
    max_nodes: int = 2_000_000
    max_patches: int = 20_000
    max_seconds: float = 180.0
    start: float = 0.0

    def check(self, stats: Stats):
        if stats.enumeration_nodes > self.max_nodes:
            raise BudgetExceeded("lattice enumeration node limit; no complete coverage")
        if stats.direct_pairs + stats.direct_candidates > self.max_nodes:
            raise BudgetExceeded("direct fallback work limit; no complete coverage")
        if stats.patches > self.max_patches:
            raise BudgetExceeded("patch limit; no complete coverage")
        if self.start and perf_counter()-self.start > self.max_seconds:
            raise BudgetExceeded("time limit; no complete coverage")


def sphere_coefficients(b, stats: Stats, budget: Budget):
    """All n in Z^3 with ||nB||^2<=3, via exact Gram-Schmidt bounds."""
    mu, norms = gram_schmidt(b)
    ns = [0, 0, 0]

    def walk(k, remaining):
        if k < 0:
            stats.sphere_points += 1
            yield tuple(ns)
            return
        center = sum((mu[j][k]*ns[j] for j in range(k+1, 3)), Q(0))
        rad2 = remaining/norms[k]
        # ceil(sqrt(rad2)) is deliberately outward; the exact test below tightens it.
        radius = isqrt(rad2.numerator//rad2.denominator)
        if radius*radius < rad2:
            radius += 1
        lo, hi = ceil(-center-radius), floor(-center+radius)
        for n in range(lo, hi+1):
            stats.enumeration_nodes += 1
            if stats.enumeration_nodes % 256 == 0:
                budget.check(stats)
            used = (Q(n)+center)**2*norms[k]
            if used <= remaining:
                ns[k] = n
                yield from walk(k-1, remaining-used)
    yield from walk(2, Q(3))
    budget.check(stats)


@dataclass(frozen=True)
class Patch:
    cmin: int
    cmax: int
    left: Q
    right: Q
    p: Q
    q: Q
    m: Q
    eps: Q
    residual_cap: int

    def basis(self):
        # Row lattice: (c,a,b) * A is the normalized physical vector.
        d, h = self.cmax, (self.right-self.left)/2
        return [[Q(1,d), -self.p/(d*h), -(self.q-self.m*self.p)/(d*self.eps)],
                [Q(0), Q(1)/(d*h), -self.m/(d*self.eps)],
                [Q(0), Q(0), Q(1)/(d*self.eps)]]

    def contains(self, a, b, c):
        h = (self.right-self.left)/2
        return (self.cmin <= c <= self.cmax
                and self.left*c <= a <= self.right*c
                and abs(a-self.p*c) <= self.cmax*h
                and abs(b-self.m*a-(self.q-self.m*self.p)*c) <= self.cmax*self.eps)


def make_patch(cmin: int, cmax: int, left: Q, right: Q, cap: int, bits: int = 48):
    left, right = Q(left), Q(right)
    if not (1 <= cmin <= cmax and 0 <= left < right < 1 and cap >= 0):
        raise ValueError("invalid patch domain")
    eta = Q(cap, cmin**5)
    if 1-right**5-eta <= 0:
        raise ValueError("patch reaches singular root region")
    p, h = (left+right)/2, (right-left)/2
    qlo, qhi = root_bracket(1-p**5, bits)
    vlo, _ = root_bracket(1-right**5, bits)
    vmin, _ = root_bracket(1-right**5-eta, bits)
    if min(qlo, vlo, vmin) <= 0:
        raise ValueError("root precision too low; increase bits")
    q = (qlo+qhi)/2
    ml, mh = -p**4/qlo**4, -p**4/qhi**4
    m = (ml+mh)/2
    eps = ((qhi-qlo)/2 + (mh-ml)*h/2
           + 2*right**3*h*h/vlo**9 + eta/(5*vmin**4))
    if eps <= 0:
        raise ValueError("zero patch thickness")
    return Patch(cmin, cmax, left, right, p, q, m, eps, cap)


def patch_search(p: Patch, accept: Callable[[int,int], bool], stats=None, budget=None):
    stats, budget = stats or Stats(), budget or Budget(start=perf_counter())
    stats.patches += 1
    budget.check(stats)
    reduced, u = lll(p.basis())
    hits = set()
    for ns in sphere_coefficients(reduced, stats, budget):
        c, a, b = [sum(ns[k]*u[k][j] for k in range(3)) for j in range(3)]
        if not (1 <= a <= b < c and p.contains(a, b, c)):
            continue
        stats.box_points += 1
        stats.exact_tests += 1
        r = a**5+b**5-c**5
        if abs(r) <= p.residual_cap and accept(r, c):
            hits.add((a,b,c,r))
    return hits


def direct_positive(cmin, cmax, cap_at, accept, stats=None, budget=None):
    """Independent monotonic fifth-root search, enumerating every (a,c)."""
    hits = set()
    for c in range(cmin, cmax+1):
        cap = cap_at(c)
        for a in range(1, c):
            if stats is not None:
                stats.direct_pairs += 1
                if budget and stats.direct_pairs % 256 == 0:
                    budget.check(stats)
            lo = max(a, iroot(max(0,c**5-a**5-cap)))
            # floor lower root may include one extra integer; exact filtering removes it.
            hi = min(c-1, iroot(max(0,c**5-a**5+cap)))
            for b in range(lo, hi+1):
                if stats is not None:
                    stats.direct_candidates += 1
                    if budget and stats.direct_candidates % 256 == 0:
                        budget.check(stats)
                r = a**5+b**5-c**5
                if abs(r) <= cap and accept(r, c):
                    hits.add((a,b,c,r))
    return hits


def search_positive(bound: int, mode="constant", cap=42, width=2, bits=48,
                    max_nodes=2_000_000, max_patches=20_000, max_seconds=180):
    """All 1<=a<=b<c<=bound with |r|<=cap, or |r|<=5*c^2 in healy mode."""
    if bound < 1 or cap < 0 or mode not in ("constant", "healy") or width <= 0:
        raise ValueError("invalid search arguments")
    stats = Stats()
    budget = Budget(max_nodes,max_patches,max_seconds,perf_counter())
    cap_at = (lambda c: cap) if mode == "constant" else (lambda c: 5*c*c)
    accept = lambda r,c: abs(r) <= cap_at(c)
    hits, shells = set(), []
    cmin = 1
    while cmin <= bound:
        cmax = min(2*cmin-1,bound)
        rmax = cap_at(cmax)
        # Proves u=a/c<=9/10 and also keeps all root arguments positive.
        if Q(rmax,cmin**5) > Q(9049,50000):
            hits |= direct_positive(cmin,cmax,cap_at,accept,stats,budget)
            shells.append({"cmin":cmin,"cmax":cmax,"method":"direct-small-shell"})
        else:
            count = max(1,ceil(Q(9*cmin,10*width)))
            first_patch = stats.patches
            for i in range(count):
                left, right = Q(9*i,10*count), Q(9*(i+1),10*count)
                patch = make_patch(cmin,cmax,left,right,rmax,bits)
                hits |= patch_search(patch,accept,stats,budget)
            shells.append({"cmin":cmin,"cmax":cmax,"method":"lattice",
                           "patches":stats.patches-first_patch})
        budget.check(stats)
        cmin *= 2
    stats.seconds = perf_counter()-budget.start
    return {"complete":True,"domain":"1 <= a <= b < c <= bound","bound":bound,
            "mode":mode,"constant_cap":cap if mode=="constant" else None,
            "residual_convention":"a^5+b^5-c^5","hits":sorted(hits),
            "stats":asdict(stats),"shells":shells}


def signed_reference(bound: int, target: int):
    """Independent signed-box dictionary oracle, canonical sorted triples."""
    fifths = {n**5:n for n in range(-bound,bound+1)}
    hits = set()
    for x in range(-bound,bound+1):
        for y in range(x,bound+1):
            z = fifths.get(target-x**5-y**5)
            if z is not None and z >= y:
                hits.add((x,y,z))
    return hits


def signed42(bound: int, **kwargs):
    """Full signed box for target42, using the reduction proved in COVERAGE.md."""
    result = search_positive(bound,mode="constant",cap=42,**kwargs)
    hits = set()
    for a,b,c,r in result["hits"]:
        if r == 42:
            hits.add(tuple(sorted((a,b,-c))))
        elif r == -42:
            hits.add(tuple(sorted((-a,-b,c))))
    # Explicit finite same-sign/c<=b/zero exceptions are all inside [-2,2]^3.
    hits |= signed_reference(min(bound,2),42)
    result["signed_hits"] = sorted(hits)
    result["signed_domain"] = f"all x,y,z in [-{bound},{bound}], modulo permutations"
    result["target"] = 42
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bound",type=int,default=100)
    p.add_argument("--mode",choices=["constant","healy","signed42"],default="signed42")
    p.add_argument("--cap",type=int,default=42)
    p.add_argument("--width",type=int,default=2)
    p.add_argument("--bits",type=int,default=48)
    p.add_argument("--max-nodes",type=int,default=2_000_000)
    p.add_argument("--max-patches",type=int,default=20_000)
    p.add_argument("--max-seconds",type=float,default=180)
    args = vars(p.parse_args())
    try:
        mode=args.pop("mode")
        if mode == "signed42":
            args.pop("cap")
            result=signed42(**args)
        else:
            result=search_positive(mode=mode,**args)
        print(json.dumps(result,indent=2))
    except BudgetExceeded as e:
        print(json.dumps({"complete":False,"error":str(e)}))
        raise SystemExit(2)

if __name__ == "__main__":
    main()

