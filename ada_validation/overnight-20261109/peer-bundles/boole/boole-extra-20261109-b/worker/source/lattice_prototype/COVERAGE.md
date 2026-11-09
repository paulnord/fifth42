# Coverage argument and explicit scope

This is a small, exact-arithmetic implementation inspired by the tangent-patch/lattice idea in [Elkies (2000)](https://arxiv.org/abs/math/0005139). It is not a port or audit of Elkies's or Healy's implementation, not a formally verified proof, and not a search beyond the recorded bounds. Tests and an independent code/mathematics review support the implementation of the following argument.

## 1. Positive canonical domain

The engine enumerates every integer triple

    1 <= a <= b < c <= N,  r = a^5+b^5-c^5,

with either `|r| <= R` (constant mode) or `|r| <= 5*c^2` (Healy reporting-threshold mode). Repeated a=b are allowed. Multiples are not discarded. Endpoints are inclusive. Permutations are represented once. The residual here is the negative of Healy's `z^5-x^5-y^5` convention.

Split denominators into disjoint inclusive shells C <= c <= D, where C runs over powers of two and D=min(2C-1,N). Choose a shell cap R that bounds every requested residual: constant R, or 5D^2. Put eta=R/C^5. If eta > 9049/50000, use the independent exact small-shell search instead of the lattice cover. Otherwise

    (a/c)^5 <= (1+eta)/2 <= (9/10)^5.

Thus u=a/c lies in [0,9/10]. Equal-width rational intervals tile this entire closed interval, including their shared boundaries. Duplicated results are removed by exact tuple equality. No unsearched endpoint or cusp is silently omitted. Small-shell search iterates every (a,c) and encloses every admissible b by exact integer fifth roots; any extra floor-bound candidate is filtered by the exact residual.

## 2. Rational tangent enclosure

Write f(u)=(1-u^5)^(1/5). In each rational interval [L,H], let p=(L+H)/2 and h=(H-L)/2. Dyadic enclosures qlo <= f(p) <= qhi use an integer fifth root of floor(x*2^(5bits)). Their validity is checked by exact fifth powers. Let q=(qlo+qhi)/2. Since

    f'(p) = -p^4/f(p)^4,
    f''(u) = -4u^3/f(u)^9,

we enclose the derivative by ml=-p^4/qlo^4 and mh=-p^4/qhi^4, and set m=(ml+mh)/2. Let vlo be a positive lower bound for f(H), and vmin a positive lower bound for (1-H^5-eta)^(1/5). Define

    eps = (qhi-qlo)/2 + (mh-ml)*h/2
          + 2*H^3*h^2/vlo^9 + eta/(5*vmin^4).

Taylor's theorem bounds the curve approximation by the first three terms. The mean-value theorem for the fifth-root function bounds the perturbation r/c^5 by the last term. In particular, for every requested triple in this patch,

    |b - m*a - (q-m*p)*c| <= c*eps <= D*eps.

All constants, comparisons and powers used for coverage are rational or integer. Low root precision can widen the enclosure, increasing work, but cannot silently narrow it. If a positive lower bound cannot be established, the patch fails explicitly.

## 3. Lattice and complete enumeration

The integer row vector (c,a,b) maps to

    ( c/D, (a-p*c)/(D*h), (b-m*a-(q-m*p)*c)/(D*eps) ).

Every admissible triple maps inside [-1,1]^3, hence inside the Euclidean sphere of squared radius 3. The three images of the integer unit vectors form an invertible rational row basis A. Rational LLL produces B=U*A by integer row additions and swaps. U is checked to have determinant +/-1 and exact B=U*A. This preserves the entire lattice; no claim about candidate validity relies on LLL being optimal.

For Gram-Schmidt coefficients mu and squared norms d, a coefficient vector n has squared norm

    sum_k d[k] * (n[k] + sum_{j>k} mu[j][k]*n[j])^2.

Descending recursion enumerates every integer n[k] consistent with the remaining squared radius. Its square-root bound is rounded outward with integer arithmetic, and each tentative value is tested exactly. This enumerates the whole sphere, not just short basis vectors, a nearest vector, or a fixed neighborhood of coefficients.

Recover (c,a,b)=n*U. Check shell, rational patch membership, strict/non-strict ordering, the actual residual cap and the requested threshold exactly. The superset sphere and tangent bounds may produce false candidates, but exact filtering removes them. Enumeration/time/patch guards raise an error; the CLI emits `complete:false` and exits 2. It never labels a truncated search complete.

## 4. Full signed box for target 42

No global exclusion follows from this prototype. For each tested N it covers all permutations of integer triples in [-N,N]^3 as follows:

* All nonnegative solutions would have every coordinate <=2, since 3^5>42. Directly check [-2,2]^3; it has no solution.
* All nonpositive triples cannot sum to 42.
* With a zero coordinate, a same-sign pair is tiny. An opposite-sign pair with unequal largest magnitude b>=3 differs in fifth powers by at least 3^5-2^5=211>42. Equal magnitudes sum to zero. Thus the finite check suffices.
* With two positive magnitudes a<=b and one negative magnitude c, if c=b then the sum is a^5, not 42. If c<b and b>=3, b^5-c^5>=211, so no solution. If b<=2 the tuple is in the finite check. Otherwise a<=b<c and r=+42.
* With two negative magnitudes a<=b and one positive magnitude c, positivity forces c>b, and r=-42.

Accordingly residual +42 maps to sorted (a,b,-c), and residual -42 maps to sorted (-a,-b,c). The engine searches both signs, plus the explicit finite check. A zero result for positive residual +42 alone would not justify a full signed-box claim.

## 5. Limitations and scaling

The regular grid uses ceil(9C/(10w)) patches per shell for configurable width parameter w (default 2), so patch count grows linearly with N. This is not a proof of linear total running time: exact LLL cost, rational sizes, sphere populations near special tangents, duplicates and small-denominator families matter. Large coefficients require increased root precision for efficiency. Pure-Python Fraction arithmetic is intentionally a transparent correctness baseline, not a production implementation.

The focused large-number controls select one grid patch using a known fixture. They test the ability to recover the fixture through lattice enumeration and arbitrary-precision arithmetic; they do not discover its location blindly, cover its entire denominator shell, or establish a large signed-box exclusion. Neither these controls nor small-N timings justify a run-time estimate beyond 10^11.
