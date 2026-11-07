# Cabbage/Boole handoff: precision and coefficient-box improvements

These are isolated, tested candidates for a bounded benchmark on Cabbage or Boole.
They do not modify the active weekend search, its checkpoint, timer, publisher,
the main branch, or the existing handoff branch. No new full-box bound is claimed.
Base snapshot: `9a1ccf86eb8c8adae2e00e3cecbbb358345a0a45`.

## Findings

1. **Reduce unnecessary root-geometry precision.** In six selected patches in
   the real 100–200 billion denominator range, exact outward root enclosures at
   adaptively chosen 88–96 bits replaced 222 bits. Four production-style cap-42
   patches had identical coefficient box sizes and exact hit sets. Preparation
   was 4.60–5.36x faster in three alternating paired cloud Fraction/LLL trials.
   Two nonempty, enlarged-cap controls at 110.3 and 122.4 billion also passed.
   This is a preparation microbenchmark, not an ADA or CUDA speedup.
   See [precision details, proof, and reproduction](precision/PRECISION.md).

2. **Enumerate the cube, not an enclosing sphere's box.** An exact inequality
   replaces each coefficient radius with floor(sum of absolute values of the
   corresponding inverse-basis column). On the complete bound1000/cap42 test,
   coefficient points fell from 4,483,388 to 1,887,678 (57.9%). All requested
   mathematical hits were preserved against independent oracles. Native CPU
   emulation was 2.12x faster for the engine alone in five paired cloud trials.
   This is not full-pipeline or ADA throughput. See
   [cube implementation, proof, test coverage, and limits](cube/README.md).

The changes were tested separately, not as a combined production pipeline.
Do not multiply their speed ratios. Neither result supports interrupting the
current search or extrapolating a new completion date.

## Reproduce first

From this directory:

    sha256sum -c PACKAGE_SHA256SUMS
    (cd precision && python3 -m unittest -v test_precision_policy.py)
    (cd precision && python3 precision_validate.py --repeats 3 --output local_precision_results.json)
    (cd cube && sh reproduce.sh)

The cube script compiles source locally, including UBSan; no binaries are
published. Original cloud results are archived, so use a fresh copy for reruns
or preserve them before invoking scripts that rewrite output files.

## Smallest useful next step on Cabbage or Boole

Use a separate worktree on Cabbage or Boole, and leave Ada searching untouched.
Check local CPU and GPU usage before testing. Do not pause or resume any Ada
service, timer, checkpoint, or publisher from this handoff. Use an existing pinned
Python environment when one is available; otherwise run the standard-library
checks first and report what dependency setup remains. Run the precision
harness with `--ada-source /absolute/path/to/lattice_prototype`. Then apply
`cube/scaling_core_cube.patch` to a separate copy of `lattice_gpu/scaling_core.py`.
Test each change separately before combining them. Keep the production source
identity and active run untouched.

Benchmark a few recorded 256-patch chunks around the current ratio cursor,
plus widely separated ratio patches, boundary cases, full small domains, and
the existing nonempty device controls. Retain every exact geometry certificate,
overflow guard, count check, GMP check and exact candidate reconstruction.
Report native preparation, certification, packing, engine, and total wall time
for five alternating repeats. Distinguish cold and persistent timings.

The precision controls' deliberately enlarged constant caps are host-only and
must not be passed into the current native 64-bit constant-cap field. The real
cap-42 cases are suitable for the existing packet format. Use the supported
original nonempty native controls for device validation.

Adoption needs a new source identity and provenance. Do not resume the frozen
weekend journal with altered precision or coefficient bounds. The cube change
preserves the symmetric packet ABI but changes its mathematically sufficient
enclosure from the whole sphere to the original cube; update any copied
coverage description accordingly. `cube/COVERAGE.md` is the archived upstream
description, not the candidate's revised proof.

## Historical timing correction

The published 500-MHz result was Elkies's GP search below 2^23, about 8.4
million, taking most of a week across exponents 4–20. His paper forecast about
a month for a faster C implementation through 10^9. Healy's 2023 extension
through 10^11 does not publish a corresponding CPU-day runtime. These are not
like-for-like timing baselines for the current high shell.

- [Elkies table and measured time](https://people.math.harvard.edu/~elkies/ferm.html)
- [Elkies paper, section 3.1](https://arxiv.org/html/math/0005139v1#S3.SS1)
- [Healy algorithm sketch](https://aleph0.blog/2023/02/26/lattices-and-fermat-near-misses/)

## Optional RTX 3060 CUDA correctness check

The repository Makefile already targets sm_86. This optional GPU path is
provided for Cabbage/Boole and has **not been executed by the cloud experiment**.
It tests the unchanged GPU kernel with old and new cube-derived packets.
It does not test higher-range cap42 GPU execution or end-to-end native prep.

Set repo and pkg to the absolute paths of this new checkout and this package.
Use an existing compatible CUDA compiler. If nvcc or the pinned dependencies
are unavailable, report the blocker rather than changing an active environment.

    repo=/absolute/path/to/fifth42-test-checkout
    pkg="$repo/speed_experiments/precision-cube-20261107"
    nvidia-smi
    (cd "$pkg/cube" && sh reproduce.sh)
    make -C "$repo/lattice_gpu" -j1 all NVCC="$(command -v nvcc)"
    (cd "$pkg" && CUDA_VISIBLE_DEVICES=0 timeout 600 python3 cuda_probe.py --binary "$repo/lattice_gpu/bin/cuda" --output cabbage_or_boole_cuda_results.json)

The GPU probe refuses an already active compute process, checks complete small
domains against a separate fifth-power-table oracle and native CPU emulation,
and verifies every packet count and reconstructed result. Prefer a bounded
interactive session, not a background service. It writes only its report.
Different CPUs and RTX3060 hardware make its timings non-transferable to Ada.

For production-engine preparation, scaling_core.initialize requires Python3.12
and the already pinned sympy1.14.0, fpylll0.6.4, cysignals1.12.5, numpy2.3.5, and
gmpy2 2.2.2. No package installation or hardware configuration is performed by
this handoff. Record actual versions, GPU and CPU models with results.
