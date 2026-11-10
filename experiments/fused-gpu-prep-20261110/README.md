# Fused GPU roots and geometry experiment

**Isolated research test; no production changes and no GPU speedup claim.**

The previous root-only Cabbage tests found the GPU slower than GMP. This package tests a different boundary: one GPU cooperative group computes a patch's root radicands, two or three exact dyadic fifth-root bounds (including saved-root reuse), and six exact rational geometry terms. Intermediate root powers stay on-device. Both CGBN and cuPQC use the same arithmetic algorithm.

## What is and is not moved

GPU: root radicands, exact bitwise root search, reuse check, powers and numerators/denominators for q, -m, and four epsilon terms.
CPU: integer-domain preflight, independent exact root/geometry certificates, rational normalization and epsilon summation, lattice basis, fpylll reduction, exact unimodularity/basis relation and coefficient inverse/bounds checks.

**Not a complete GPU candidate-preparation or search implementation.** No enumeration, residual screening, GMP hit audit, journal, ledger, publisher, or production integration is performed. No full production throughput or coverage may be claimed. The 4096-bit implementation and 8192-byte output per patch are conservative and could be costly; keeping all geometry on-device has not been shown faster.

## Exactness

Input `<6QI` fields are cmin,cmax,left numerator,right numerator,common denominator,cap,bits. Integers must fit the supported domain: `1<=cmin<=cmax<=2^40`, `0<=L<R<D<=2^40`, `0<=cap<=42`, `1<=bits<=222`; singular adjusted radicands reject before launch. Unsupported packets fail rather than silently omit work. Production adoption would need an explicit CPU fallback.

Use P=L+R, H=R-L, Rg=2R, S=2D. Let T=2^bits, nq/nqh the lower/upper midpoint root integers, nv the right root, na the residual-adjusted lower root. Six returned positive fractions are:

1. q=(nq+nqh)/(2T)
2. -m=P^4 T^4(nq^4+nqh^4)/(2 S^4 nq^4 nqh^4)
3. eps_root=(nqh-nq)/(2T)
4. eps_slope=P^4 T^4(nqh^4-nq^4)H/(2 S^5 nq^4 nqh^4)
5. eps_curve=2 Rg^3 H^2 T^9/(S^5 nv^9)
6. eps_residual=cap T^4/(5 cmin^5 na^4)

CPU verifies each returned root using `k^5 D <= N*2^(5b) < (k+1)^5 D`, checks upper-root exactness, independently reconstructs the original rational formulas, then checks basis/reduction/coefficients. It does not recompute roots in the candidate certificate. Baseline uses GMP iroot with the existing saved-root behavior and rebuilds its patch for the certificate.

All unsigned device intermediates have a conservative bound below 2219 bits within this domain, including trial roots at `T+1`; 4096 bits therefore cannot truncate them. This bounds only these formulas, not subsequent LLL rationals.

## Run on Cabbage

Existing prerequisites: CUDA13.2-capable nvcc, compatible host compiler, NVIDIA driver/device, GMP development headers and library, Python supporting the pinned wheels, git/curl/tar. This runner checks them and stops clearly rather than editing system packages or drivers.

```
timeout --signal=TERM --kill-after=10s 45m bash experiments/fused-gpu-prep-20261110/run.sh "$HOME/fifth42-fused-test-$(date -u +%Y%m%dT%H%M%SZ)"
```

Use a fresh output directory. It creates a local venv and private CUDA layout, fetches pinned CGBN, downloads a hash-pinned cuPQC SDK unless `CUPQC_ROOT` is set, builds both backends at8/16 threads, runs exact smoke checks, then bounded sweeps. Timings use8/16 threads, group4/8,256/4096 patches in Cabbage/Boole-shaped regions. `SUMMARY.json` and logs remain in the output.

Downloading/using cuPQC accepts [NVIDIA Math SDK terms](https://docs.nvidia.com/cuda/cupqc/additional/license.html). SDK bytes are not redistributed. CGBN license retained in its pinned clone.

## Interpretation

`cpu.total_s`: actual patch prep + independent rebuild + warmed LLL/bounds certificate.
`gpu.cold_total_s`: measured subprocess (including2 launch passes, CUDA setup, preflight, serialization) + Python decode/exact certificate + same LLL/bounds.
`warm_component_estimate_NOT_measured_pipeline_s`: final warm kernel + H2D + D2H + decode/cert + LLL. **An additive estimate, not a persistent-pipeline measurement.** Host preflight, packing and allocation costs are omitted here. Report both cold measured and warm estimate; do not promote from kernel-only speed.

CPU timings run before GPU timings within each case, not interleaved; rigorous performance claims require alternating trials and controlling system load. The benchmark's primary gate is correctness and finding whether fusion is worth further development. fpylll imports/initialization are warmed for both paths. Record count, adaptive bits, region, group and transfer bytes. Do not compare selected-grid patches to complete box coverage.

## Local validation

See `validation/` for compiler evidence and CPU tests. Compilation on CUDA13.2/sm86 is not GPU execution. Cabbage must pass the exact-output checks before any performance conclusion. Production directories/services/checkpoints are never opened by the runner.

Evidence storage: require at least5GiB free before setup. Each case retains its first binary GPU output and input plus all logs and output hashes; later identical generated output files are removed after successful exact verification. No existing/user files are deleted. CUDA LTO binaries may be large and are not for Git publication.

CPU baseline uses one process, not the production16-worker pool. A passing single-process comparison does not establish a gain against production concurrency. Candidate certification deliberately recalculates the geometry arithmetic from certified roots; the benchmark includes that cost. Exact geometry validation may erase any offload savings, which is itself a meaningful outcome.

Vendored reference provenance: Cabbage's archived `deployment_snapshots/overnight-20261110/cabbage/handoff/source/worker/source/lattice_prototype/compiled_experiment/lattice5_snapshot.py` at commit `b6ee86ce9b1269ab31cdd51a06fb499d51b7a138`; SHA256 `52c99797f2e950834bc6a4838a3c4cc6a740181ab245d7d7e3c93a14c4797710`. GMP iroot is installed only into this private imported reference, leaving external source untouched. The precision policy is copied from the published wide-groups worker.
