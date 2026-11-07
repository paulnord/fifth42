"""Exact geometric coverage, not a count of lattice points or certificates.

A rectangle is {cmin, cmax, left: [numerator, denominator], right: [...]}.
Denominator rows are inclusive integers. Ratio intervals are closed; difference
returns closures of positive-width components (removed endpoints are immaterial
for these measures). Use exact_difference and exact_intersection for endpoint
membership: boundary points can contain integer solutions despite zero area.
All calculations use Fraction, never floats. Work scales with rectangle count,
not the numerical length of the denominator range.

Callers must supply only certified, successfully committed rectangles in
``previous`` and ``committed``. This module does not validate certificates.
"""
from fractions import Fraction
from collections.abc import Mapping

MAX_DENOMINATOR = 200_000_000_000
MAX_RATIO = Fraction(9, 10)


def _integer(value):
    if type(value) is not int:
        raise ValueError('coordinates must be exact integers (not bools)')
    return value


def _fraction(pair):
    if not isinstance(pair, (list, tuple)) or len(pair) != 2:
        raise ValueError('ratio must be an integer numerator/denominator pair')
    n, d = map(_integer, pair)
    if d <= 0:
        raise ValueError('ratio denominator must be positive')
    return Fraction(n, d)


def _pair(value):
    return [value.numerator, value.denominator]


def rectangle(cmin, cmax, left, right):
    """Validate a rectangle and return normalized, JSON-compatible coordinates."""
    lo, hi = _integer(cmin), _integer(cmax)
    a, b = _fraction(left), _fraction(right)
    if not 1 <= lo <= hi <= MAX_DENOMINATOR:
        raise ValueError('denominator rows must satisfy 1 <= cmin <= cmax <= 2e11')
    if not 0 <= a < b <= MAX_RATIO:
        raise ValueError('ratios must satisfy 0 <= left < right <= 9/10')
    return dict(cmin=lo, cmax=hi, left=_pair(a), right=_pair(b))


def _parse(regions):
    result = []
    for region in regions:
        if not isinstance(region, Mapping):
            raise ValueError('each region must be a rectangle mapping')
        for key in ('left_closed', 'right_closed'):
            if key in region and region[key] is not True:
                raise ValueError('inputs must be closed rectangles; open components are report-only')
        try:
            r = rectangle(*(region[k] for k in ('cmin', 'cmax', 'left', 'right')))
        except KeyError as exc:
            raise ValueError('rectangle missing coordinate: ' + str(exc)) from exc
        result.append((r['cmin'], r['cmax'], _fraction(r['left']), _fraction(r['right'])))
    return result


def _merge(intervals):
    result = []
    for a, b in sorted(intervals):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return result


def _subtract(intervals, removed):
    result = []
    for a, b in intervals:
        cursor = a
        for x, y in removed:
            if y <= cursor:
                continue
            if x >= b:
                break
            if x > cursor:
                result.append((cursor, x))
            cursor = max(cursor, y)
            if cursor >= b:
                break
        if cursor < b:
            result.append((cursor, b))
    return result


def _combine(first, second, operation):
    a, b = _parse(first), _parse(second)
    boundaries = sorted({c for lo, hi, _, _ in a + b for c in (lo, hi + 1)})
    slabs = []
    for lo, stop in zip(boundaries, boundaries[1:]):
        ai = _merge((x, y) for start, end, x, y in a if start <= lo <= end)
        bi = _merge((x, y) for start, end, x, y in b if start <= lo <= end)
        if operation == 'union':
            intervals = _merge(ai + bi)
        elif operation == 'difference':
            intervals = _subtract(ai, bi)
        else:
            intervals = _merge((max(x, u), min(y, v)) for x, y in ai
                               for u, v in bi if max(x, u) < min(y, v))
        if not intervals:
            continue
        if slabs and slabs[-1][1] + 1 == lo and slabs[-1][2] == intervals:
            slabs[-1] = (slabs[-1][0], stop - 1, intervals)
        else:
            slabs.append((lo, stop - 1, intervals))
    return [dict(cmin=lo, cmax=hi, left=_pair(x), right=_pair(y))
            for lo, hi, intervals in slabs for x, y in intervals]


def canonical_union(regions):
    """Disjoint denominator slabs, with merged and sorted ratio intervals."""
    return _combine(regions, (), 'union')


def difference(regions, subtract):
    """Positive-width difference components, represented by their closures."""
    return _combine(regions, subtract, 'difference')


def intersection(regions, other):
    """Positive-width intersection; isolated boundary points are omitted."""
    return _combine(regions, other, 'intersection')


def _exact_combine(first, second, operation):
    a, b = _parse(first), _parse(second)
    boundaries = sorted({c for lo, hi, _, _ in a + b for c in (lo, hi + 1)})
    slabs = []
    for lo, stop in zip(boundaries, boundaries[1:]):
        ar = [(x, y) for start, end, x, y in a if start <= lo <= end]
        br = [(x, y) for start, end, x, y in b if start <= lo <= end]
        ai, bi = _merge(ar), _merge(br)
        if operation == 'difference':
            components = [(x, y, not any(u <= x <= v for u, v in bi),
                           not any(u <= y <= v for u, v in bi))
                          for x, y in _subtract(ai, bi)]
        elif operation == 'record_boundaries':
            # Pairwise boundary-only overlaps, even when a third record covers
            # a surrounding positive-width interval. Preserve that duplication.
            points = sorted({max(x, u) for i, (x, y) in enumerate(ar)
                             for u, v in ar[i + 1:] if max(x, u) == min(y, v)})
            components = [(x, x, True, True) for x in points]
        else:
            intervals = _merge((max(x, u), min(y, v)) for x, y in ai
                               for u, v in bi if max(x, u) <= min(y, v))
            components = [(x, y, True, True) for x, y in intervals
                          if operation == 'intersection' or x == y]
        if not components:
            continue
        if slabs and slabs[-1][1] + 1 == lo and slabs[-1][2] == components:
            slabs[-1] = (slabs[-1][0], stop - 1, components)
        else:
            slabs.append((lo, stop - 1, components))
    return [dict(cmin=lo, cmax=hi, left=_pair(x), right=_pair(y),
                 left_closed=lc, right_closed=rc)
            for lo, hi, components in slabs for x, y, lc, rc in components]


def exact_difference(regions, subtract):
    """Exact closed-union difference, with explicit endpoint membership.

    Inputs must be positive-width closed rectangles. Their difference cannot
    contain isolated points. Output components may be open or half-open and
    are report-only, not valid closed-rectangle inputs to the other operations.
    """
    return _exact_combine(regions, subtract, 'difference')


def exact_intersection(regions, other):
    """Exact intersection including singleton ratio components (left == right)."""
    return _exact_combine(regions, other, 'intersection')


def boundary_intersection(regions, other):
    """Isolated zero-width components of the intersection of two closed unions."""
    return _exact_combine(regions, other, 'boundaries')


def boundary_overlaps(regions):
    """Shared endpoint slices for pairs of records whose ratio overlap is a point.

    Positive-width duplicate overlaps are covered by the usual union accounting.
    Returned slices are deduplicated, not a multiplicity count.
    """
    return _exact_combine(regions, (), 'record_boundaries')


def measure(regions, weighted=False):
    """Union measure sum(width) per integer row; optionally sum(c * width)."""
    return _raw_measure(_parse(canonical_union(regions)), weighted)


def _raw_measure(parsed, weighted=False):
    total = Fraction(0)
    for lo, hi, a, b in parsed:
        rows = hi - lo + 1
        factor = (lo + hi) * rows // 2 if weighted else rows
        total += factor * (b - a)
    return total


def coverage_report(planned, previous=(), committed=(), guarded=(), incomplete=()):
    """JSON report; guarded/incomplete attempts cannot contribute coverage.

    Duplicate area is multiplicity excess: sum of record measures minus their
    union. Prior overlap is counted once. Planned gaps exclude all committed
    coverage, including previous runs; coverage outside the plan is explicit.
    """
    raw = {name: list(values) for name, values in (
        ('planned', planned), ('previous', previous), ('committed', committed),
        ('guarded', guarded), ('incomplete', incomplete))}
    unions = {name: canonical_union(values) for name, values in raw.items()}
    total = canonical_union(unions['previous'] + unions['committed'])
    unions.update(
        total_covered=total,
        newly_covered=difference(unions['committed'], unions['previous']),
        prior_overlap=intersection(unions['committed'], unions['previous']),
        planned_gaps=difference(unions['planned'], total),
        covered_within_plan=intersection(total, unions['planned']),
        covered_outside_plan=difference(total, unions['planned']))
    metrics = {}
    for weighted, label in ((False, 'row_ratio_area'), (True, 'c_weighted_geometric_area')):
        metrics[label] = {name: _pair(measure(regions, weighted))
                          for name, regions in unions.items()}
        for name in ('previous', 'committed'):
            excess = _raw_measure(_parse(raw[name]), weighted) - measure(unions[name], weighted)
            metrics[label][name + '_duplicate_excess'] = _pair(excess)
        metrics[label]['committed_non_novel_excess'] = _pair(
            _raw_measure(_parse(raw['committed']), weighted)
            - measure(unions['newly_covered'], weighted))
    exact = dict(newly_covered=exact_difference(unions['committed'], unions['previous']),
                 planned_gaps=exact_difference(unions['planned'], total),
                 prior_overlap=exact_intersection(unions['committed'], unions['previous']),
                 covered_outside_plan=exact_difference(total, unions['planned']))
    boundaries = dict(prior=boundary_intersection(unions['committed'], unions['previous']),
                      previous_records=boundary_overlaps(raw['previous']),
                      committed_records=boundary_overlaps(raw['committed']),
                      all_records=boundary_overlaps(raw['previous'] + raw['committed']))
    return dict(schema_version=2, metric_kind='geometric_not_lattice_point_count',
                boundary_convention=('regions are positive-width closures for geometric metrics and '
                                     'conservative scheduling; exact_regions preserve endpoint membership; '
                                     'boundary_overlaps disclose zero-area shared endpoint slices'),
                exact_regions=exact, boundary_overlaps=boundaries,
                record_counts={name: len(values) for name, values in raw.items()},
                regions=unions, measures=metrics)
