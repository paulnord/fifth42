# Exact enclosure used by the CUDA prototype

This document describes the intended finite-domain implementation. CUDA build
and device validation are pending. It establishes no new completed search or
speedup. The original reference and its coverage argument are pinned in
`UPSTREAM.json` at commit ddf28f04725b29b2f1d53b5d33c16379b0f66a20.

For each rational tangent patch, the pinned CPU implementation constructs the
row basis A. Every admissible integer point m=(c,a,b) in that patch maps to
x=mA with each coordinate in [-1,1], hence ||x||²<=3. CPU exact LLL returns
B=UA, with integer det(U)=+1 or -1. Thus n=mU^-1 is integral and x=nB.

Let V=B^-1. Then n=xV, so Cauchy-Schwarz gives

    |n_j|² <= 3 sum_i V_ij².

The host computes J_j=ceil(sqrt(3 sum_i V_ij²)) using exact fractions and
integer square roots. The complete integer box -J_j<=n_j<=J_j encloses the
entire sphere, including its boundary. This box can contain substantially
more points than the original sphere walk; that is a performance cost, not
an exclusion. No floating-point value decides coverage or candidate validity.

The GPU visits each coefficient exactly once in disjoint chunks. It recovers
m=nU and checks the positive domain, denominator shell and exact fifth-power
residual. It may return points outside the specific rational patch; Python
reconstructs every returned coefficient and applies the original exact patch
membership test. Patch duplicates are deduplicated by exact tuples.

Before dispatch, Python reconstructs every patch from the expected shell/grid,
checks A against that patch, det(U), B=UA, the inverse, and all J_j. It also
checks that the complete expected grid is present. The fixed-size engine itself
only reports completion of the supplied coefficient boxes; it cannot certify
an arbitrary packet as a complete mathematical domain.

The engine parser independently verifies range and work limits. Each transform
must satisfy sum_i J_i*abs(U_ij)<=2^63-1, which prevents overflow in every
integer multiplication and partial sum during nU reconstruction. Bounds and
transforms outside this range fail explicitly. Full-domain preparation is
limited to N<=1,000; larger arithmetic is exercised only in the two selected
fixture patches, with bases at most 10^11. It never silently truncates a domain.

For |x|<=10^11, 3|x|^5<2^191. Signed 192-bit residual arithmetic therefore has
headroom; fifth powers and all carries are computed with unsigned limbs.
`__umul64hi` supplies the high half of a 64-by-64-bit product as documented by
[NVIDIA](https://docs.nvidia.com/cuda/archive/13.3.1/libdevice-users-guide/__nv_umul64hi.html).
The new fifth64 routine supports these 64-bit bases; the older int-only fifth
function in the frozen header is not used by this kernel.

Per-task visited counts must equal the exact coefficient-box volumes. A device
error, missing count, oversized work packet, unrepresentable transform, or
candidate-buffer overflow fails the whole packet without completion. The caps
are 4,096 tasks, 10 million coefficient points per task, and 50 million per
packet. These are work limits, not search recommendations.

Small shells that fail the original rational enclosure threshold use the pinned
CPU direct search with its guards. The union of those shells and all verified
patches is the stated canonical positive domain. Residual +42/-42 and the tiny
same-sign/zero-coordinate exceptions use the pinned signed reduction. Selected
large-fixture packets remain selected patches, never full-shell coverage.

These are coverage arguments and implementation checks, not formal verification.
Actual device agreement with independent references remains required before
relying on the CUDA implementation.
