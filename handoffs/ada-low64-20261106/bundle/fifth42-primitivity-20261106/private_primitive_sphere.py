# Derived isolated test only. Requires injected l, Q, math, scale_allowed.
"""Optional exact target filters; independent of the production/reference path.

Covers bounded positive target searches and, only for target42, the existing
proved full signed reduction. Modular conditions are necessary, never
sufficient: exact residual equality is retained.
"""
from dataclasses import dataclass, asdict
from fractions import Fraction as Q
from math import isqrt
from time import perf_counter
import lattice5 as l


@dataclass
class FilterStats:
    residue_candidates: int = 0
    modular_rejects: int = 0
    norm_tests: int = 0
    cache_entries: int = 0
    interval_rejects: int = 0
    integer_intervals: int = 0
    primitive_rejects: int = 0
    gcd_calls: int = 0


class TargetFilter:
    def __init__(self, u, targets, moduli=(25, 31, 61)):
        self.targets = frozenset(targets)
        self.moduli = tuple(moduli)
        if not self.targets or any(type(t) is not int for t in self.targets):
            raise ValueError('nonempty integer targets required')
        if any(type(m) is not int or m < 2 for m in self.moduli):
            raise ValueError('integer moduli >= 2 required')
        self.u = u
        self.powers = {m: tuple(pow(x, 5, m) for x in range(m)) for m in self.moduli}
        self.residues = {m: {t % m for t in self.targets} for m in self.moduli}
        self.cache = {}

    def accepts_original(self, c, a, b):
        return all((self.powers[m][a % m] + self.powers[m][b % m]
                    - self.powers[m][c % m]) % m in self.residues[m]
                   for m in self.moduli)

    def allowed_first(self, m, n1, n2):
        """All n0 residues for a fixed suffix; integer row map (c,a,b)=nU."""
        key = (m, n1 % m, n2 % m)
        if key not in self.cache:
            base = [(n1*self.u[1][j]+n2*self.u[2][j]) % m for j in range(3)]
            p, wanted = self.powers[m], self.residues[m]
            self.cache[key] = frozenset(n for n in range(m)
                if (p[(base[1]+n*self.u[0][1]) % m]
                    + p[(base[2]+n*self.u[0][2]) % m]
                    - p[(base[0]+n*self.u[0][0]) % m]) % m in wanted)
        return self.cache[key]


def filtered_sphere(b, filt, stats, budget, fs, progressions=False, exact_interval=False):
    """Exact reference recursion, rejecting modular failures before k=0 norm work.

    Counts every outward-bound integer against the original node budget, even
    when filtered. This deliberately does not pretend to reduce visited nodes.
    """
    mu, norms = l.gram_schmidt(b)
    ns = [0, 0, 0]
    def walk(k, remaining):
        if k < 0:
            stats.sphere_points += 1
            yield tuple(ns)
            return
        center = sum((mu[j][k]*ns[j] for j in range(k+1, 3)), Q(0))
        rad2 = remaining/norms[k]
        radius = isqrt(rad2.numerator//rad2.denominator)
        if radius*radius < rad2:
            radius += 1
        lo, hi = l.ceil(-center-radius), l.floor(-center+radius)
        allowed = [(m, filt.allowed_first(m, ns[1], ns[2])) for m in filt.moduli] if k == 0 else []
        candidates = range(lo, hi+1)
        skipping = k == 0 and (exact_interval or (progressions and bool(allowed)))
        if skipping:
            # Count the same outward interval as the unskipped recursion, so
            # skipping cannot evade the reference work guard.
            count = max(0, hi-lo+1)
            stats.enumeration_nodes += count
            budget.check(stats)
            if exact_interval:
                # center=A/B, norm=C/D, remaining=E/F. The norm inequality
                # is equivalent to (n*B+A)^2 <= floor(E*B^2*D/(F*C)).
                A,B = center.numerator, center.denominator
                C,D = norms[k].numerator, norms[k].denominator
                E,F = remaining.numerator, remaining.denominator
                root = isqrt((E*B*B*D)//(F*C))
                lo,hi = max(lo, -((root+A)//B)), min(hi, (root-A)//B)
                tight_count = max(0,hi-lo+1)
                fs.interval_rejects += count-tight_count
                fs.integer_intervals += 1
                count = tight_count
            fs.residue_candidates += count
            if not allowed:
                allowed = [(1, frozenset([0]))]
            modulus, residues = min(allowed, key=lambda pair: Q(len(pair[1]),pair[0]))
            candidates = sorted(n for r in residues
                for n in range(lo+(r-lo)%modulus, hi+1, modulus)
                if all(n % m in rs for m,rs in allowed))
            fs.modular_rejects += count-len(candidates)
        suffix_gcd = math.gcd(ns[1],ns[2]) if k == 0 else 1
        primitive_only = filt.targets <= {-42,42}
        for n in candidates:
            if not skipping:
                stats.enumeration_nodes += 1
            if stats.enumeration_nodes % 256 == 0:
                budget.check(stats)
            if k == 0 and suffix_gcd != 1:
                fs.gcd_calls += 1
                g = math.gcd(n,suffix_gcd)
                if (g != 1 if primitive_only else not scale_allowed(g,filt.targets)):
                    fs.primitive_rejects += 1
                    continue
            if k == 0 and not skipping:
                fs.residue_candidates += 1
                if any(n % m not in residues for m, residues in allowed):
                    fs.modular_rejects += 1
                    continue
            if k == 0 and exact_interval:
                ns[k] = n
                stats.sphere_points += 1
                yield tuple(ns)
                continue
            fs.norm_tests += 1
            used = (Q(n)+center)**2*norms[k]
            if used <= remaining:
                ns[k] = n
                yield from walk(k-1, remaining-used)
    yield from walk(2, Q(3))
    fs.cache_entries = len(filt.cache)
    budget.check(stats)


def search_patch(p, targets, mode='post', moduli=(25, 31, 61), backend='reference', budget=None):
    """Bounded target-specific patch comparison: none, post, or prune mode."""
    moduli = tuple(moduli)
    if mode not in ('none', 'post', 'prune', 'progression', 'interval'):
        raise ValueError('unknown filter mode')
    targets = frozenset(targets)
    if not targets or any(type(t) is not int for t in targets) or max(map(abs, targets)) > p.residual_cap:
        raise ValueError('patch cap must cover all nonempty integer targets')
    start = perf_counter()
    stats, fs = l.Stats(patches=1), FilterStats()
    budget = budget or l.Budget(start=start)
    budget.check(stats)
    b, u = l.reduce_basis(p.basis(), backend)
    budget.check(stats)
    filt = TargetFilter(u, targets, moduli)
    candidates = (filtered_sphere(b, filt, stats, budget, fs, mode in ('progression','interval'), mode == 'interval') if mode in ('prune','progression','interval')
                  else l.sphere_coefficients(b, stats, budget))
    hits = set()
    for n in candidates:
        c, a, b = [sum(n[k]*u[k][j] for k in range(3)) for j in range(3)]
        if not (1 <= a <= b < c and p.contains(a,b,c)):
            continue
        stats.box_points += 1
        if mode == 'post':
            fs.residue_candidates += 1
            if not filt.accepts_original(c,a,b):
                fs.modular_rejects += 1
                continue
        stats.exact_tests += 1
        r = a**5+b**5-c**5
        if r in targets:
            hits.add((a,b,c,r))
    budget.check(stats)
    stats.seconds = perf_counter()-start
    return {'hits': sorted(hits), 'stats': asdict(stats), 'filter_stats': asdict(fs),
            'complete': True, 'scope': 'this positive canonical patch only', 'mode': mode,
            'moduli': list(moduli), 'targets': sorted(targets), 'backend': backend}


def search_targets_positive(bound, targets, mode='post', moduli=(25,31,61),
                            backend='reference', width=2, bits=48,
                            max_nodes=2_000_000, max_patches=20_000, max_seconds=180):
    """Complete bounded positive canonical domain for a finite residual target set.

    Uses exactly the reference constant-cap shell planner and fallback criterion.
    Does not assert a full signed reduction for arbitrary targets.
    """
    moduli = tuple(moduli)
    targets = frozenset(targets)
    if bound < 1 or width <= 0 or not targets or any(type(t) is not int for t in targets):
        raise ValueError('invalid target search arguments')
    if mode not in ('none','post','prune','progression','interval'):
        raise ValueError('unknown filter mode')
    if backend not in ('reference','sympy','fpylll'):
        raise ValueError('unknown backend')
    cap = max(map(abs,targets))
    # Validate moduli even if all shells take the direct fallback.
    TargetFilter([[1,0,0],[0,1,0],[0,0,1]],targets,moduli)
    start = perf_counter()
    stats, fs = l.Stats(), FilterStats()
    budget = l.Budget(max_nodes,max_patches,max_seconds,start)
    hits, shells = set(), []
    cmin = 1
    while cmin <= bound:
        cmax = min(2*cmin-1,bound)
        if Q(cap,cmin**5) > Q(9049,50000):
            hits |= l.direct_positive(cmin,cmax,lambda c:cap,lambda r,c:r in targets,stats,budget)
            shells.append(dict(cmin=cmin,cmax=cmax,method='direct-small-shell'))
        else:
            count = max(1,l.ceil(Q(9*cmin,10*width)))
            for i in range(count):
                p = l.make_patch(cmin,cmax,Q(9*i,10*count),Q(9*(i+1),10*count),cap,bits)
                remaining_budget = l.Budget(max_nodes-stats.enumeration_nodes,
                    max_patches-stats.patches,max_seconds,start)
                result = search_patch(p,targets,mode,moduli,backend,remaining_budget)
                hits.update(map(tuple,result['hits']))
                for key,value in result['stats'].items():
                    if key != 'seconds':
                        setattr(stats,key,getattr(stats,key)+value)
                for key,value in result['filter_stats'].items():
                    setattr(fs,key,getattr(fs,key)+value)
                budget.check(stats)
            shells.append(dict(cmin=cmin,cmax=cmax,method='lattice',patches=count))
        budget.check(stats)
        cmin *= 2
    stats.seconds = perf_counter()-start
    return dict(complete=True,domain='1 <= a <= b < c <= bound',bound=bound,
                targets=sorted(targets),hits=sorted(hits),stats=asdict(stats),
                filter_stats=asdict(fs),shells=shells,mode=mode,moduli=list(moduli),backend=backend)


def signed42_filtered(bound, **kwargs):
    """Only target42 uses the already-proved full-signed reduction."""
    result = search_targets_positive(bound,[-42,42],**kwargs)
    hits = set(l.signed_reference(min(bound,2),42))
    for a,b,c,r in result['hits']:
        hits.add(tuple(sorted((a,b,-c) if r==42 else (-a,-b,c))))
    result.update(target=42,signed_hits=sorted(hits),
                  signed_domain=f'all x,y,z in [-{bound},{bound}], modulo permutations')
    return result
