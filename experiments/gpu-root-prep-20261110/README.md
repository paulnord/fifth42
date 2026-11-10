# Isolated GPU root-preparation study

No production edits, no GPU compilation or measurements. Includes CPU-validated mathematical specifications and ready-to-build CUDA source, still awaiting actual GPU validation.

Pinned source examined: fifth42 b6ee86ce9b1269ab31cdd51a06fb499d51b7a138, Boole archived common worker.

## Computation

root_bracket(N/D,b) returns exact outward dyadic fifth-root bounds. Equivalent integer predicate:

    k^5 D <= N 2^(5b)

The returned integer n must satisfy:

    n^5 D <= N 2^(5b) < (n+1)^5 D.

It yields [n/2^b,(n+1)/2^b], or a collapsed interval on equality. No floating approximation decides exclusion.

## Prototypes

`prototype.py` supplies two independent candidate algorithms, executed with Python integers:

* `newton_bracket`: one scaled rational division then descending integer Newton fifth root. Suitable for CGBN's wide integer division. Exact final inequalities required.
* `division_free_bracket`: accept/reject bits from high to low using the predicate above. Uses multiplication/comparison/shifts only, therefore can be implemented with cuPQC warp arithmetic despite its unavailable warp division. It costs b iterations and is not presumed fast.

Both refuse input outside [0,1], bits outside1..222, or a conservative intermediate-width proof. Refusal must dispatch to CPU, never mask/truncate a value. The conservative proof includes the final (n+1)^5 inequality. Fifth42's make_patch roots are inside this domain. Do not generalize to other use without new bounds.

## Validation

424 cases agree with the archived standard-library reference root_bracket: exact powers, adjacent rational values,0/1,tiny fractions, random fractions and production-shaped patches.189 production-shaped roots at b80/128/222 also match in2048 bits. Artificial rational boundary cases require4096, demonstrating why width checks are essential. Explicit undersized-width rejection tests pass. See validation.json.

These are not GMP or CUDA test passes. The production code replaces the reference binary-search root with GMP iroot, so Python timing differences MUST NOT be presented as speedups over production.

## Follow-on GPU benchmark design (not all implemented)

1. Implement bounded add/mul/div/comparison test adapter and root kernels in scratch package, pin CGBN commit114601b and compiler/GMP dependencies. Target SM86 for RTX3060/3080Ti.
2. Record the actual reduced/adaptive precision roots and widths supplied by production preparation, preserving root-reuse decision (many third roots are already avoided).
3. Compare CGBN Newton and cuPQC variants at supported widths and thread counts. For cuPQC, test1024-bit single-thread Newton on accepted small inputs,4096-bit warp division-free candidate on larger inputs; CPU fallback handles unsupported widths.
4. Recent actual-window width sampling by independent design worker found b88 with ~619/802-bit shifted numerators, so1024-bit cuPQC has plausible ordinary-window coverage. Near patch0 b176 needed1059/1242 bits. These are samples, not a universal bound.
5. Include nonempty/boundary controls and compare exact brackets, full patch basis, bounds, visits/hits and GMP audits. Warm/root-reused baseline required.
6. Report prep, certification, packing, transfers, kernel, persistence and whole-pipeline original cells/s on sparse/middle/dense regions. No deployed coverage should be claimed for benchmark windows.

## Limits

Moving roots alone leaves rational slope/error geometry, lattice reduction, exact transform/bounds certification and packing on CPU. Returning roots to CPU can erase savings. Profile those stages and batch transfers. Retain CPU certification until proof and independent GPU arithmetic testing are sufficient.

## Certification integration trap

Current `exact_host_opt.certify_task` reconstructs make_patch and repeats the root work. An offload that leaves this untouched still pays those CPU roots. A separate candidate certification path can independently check returned dyadic n via the two exact integer inequalities (and equality for upper endpoint), then reconstruct rational geometry from certified root intervals. Retain U unimodularity, B=UA, coefficient enclosure and overflow checks. This needs a reviewed trust boundary and tests proving malformed roots cannot enter geometry; do not simply share preparation objects or skip certification. Measure verification cost separately from root-finding.

## Ready-to-run Cabbage experiment (2026-11-10)

`root_cuda.cu` is an implementable CGBN2048 division-free kernel. **Source inspected only: no nvcc or GPU available in the authoring environment.** It is deliberately a correctness-first baseline, not a promised improvement. It searches the dyadic root one bit at a time; Newton/seed refinement may be necessary for useful speed.

`run.sh` clones CGBN at pinned commit114601b07ae8c3e4d46b250208ea8d9def7a12f0, uses existing CUDA/GCC/Python, builds SM86/C++17 with4,8,16,32 threads per integer, tests batches256/1024/4096 with six repeated kernels each. First repeat is cold; repeats1–5 are warm. It does not install packages, change drivers, modify production, stop services, or claim coverage. Missing dependencies cause a clear stop. Choose a quiet period for timings; do not stop production to make it quiet.

Dependencies: CUDA toolkit supporting SM86, compatible host C++ compiler, Git, Python3 standard library. Optional existing gmpy2 enables a true GMP iroot baseline; absent gmpy2 is explicitly null in reports (Python reference timing is NOT the production baseline). The cuPQC SDK is downloaded locally by default under its NVIDIA license terms; set CUPQC_DOWNLOAD=0 to skip.

One invocation from this directory:

```sh
bash run.sh
```

All logs, binaries, fixed-seed fixtures, actual returned integers, exact certificates, CUDA/GPU versions, per-kernel timings, process-wall timings and SUMMARY.json are retained under a fresh `~/fifth42-cgbn-test-<UTC>` directory. If build/runtime validation fails, stop and report the compiler/runtime logs rather than adapting production. No test success can be claimed until Cabbage actually runs this.

CPU local preflight:41,200 exhaustive rational cases (denominators1..100,bits1..8), wrong-root certificate rejections and width-edge checks PASS. The fixture generator produced1,020 admissible records and explicitly rejected4 artificial over-width boundary cases. This fallback is necessary:2048 is not a universal bound for arbitrary input fractions.

## Full-pipeline promotion gate (not implemented in this microbenchmark)

1. Capture the live production input triples (numerator,denominator,bits) and root-reuse/adaptive-width histogram without changing coverage. Compare every returned interval byte-for-byte with the current GMP root path.
2. Replace only root evaluation behind a feature flag; independently verify `D*k^5 <= N*2^(5b) < D*(k+1)^5` on CPU. Preserve all geometry,U/J/unimodularity,range and exact-hit checks. The current independent certification rebuild must consume proved intervals or it will repeat CPU root work and erase the benefit. Never remove certification.
3. Alternate unchanged CPU/GMP and candidate at identical source/config/cursor for30 paired trials, record packing,transfer,kernel,certification,LLL,enumeration and total wall time. Use persistent process too; distinguish cold startup. Require exact bounds,counts,hit sets and journal digest equality; run known-positive and boundary cases, not only empty-hit patches.
4. Publish raw evidence and confidence intervals. Deploy only after end-to-end benefit and independent review; this package does not deploy.

cuPQC comparison source is bundled as `root_cupqc.cu`, implemented against the official 0.6.0 BigInt API, not compiled here. It runs the same fixtures and exact certificates, using 2048-bit cooperative multiplication rather than unavailable cooperative division. Set `CUPQC_ROOT` to an already-authorized 0.6.0 SDK installation; the same runner then builds and tests both libraries. If downloading is disabled and no SDK is supplied, it finishes CGBN and records cuPQC-BLOCKED.txt explicitly. The SDK is proprietary and its license terms apply; the runner downloads it into the isolated evidence directory by default. Set CUPQC_DOWNLOAD=0 to skip downloading. Official requirements: https://docs.nvidia.com/cuda/cupqc/introduction/requirements.html . Download: https://developer.nvidia.com/cupqc-downloads .

Automatic SDK setup: running `bash run.sh` uses NVIDIA's proprietary cuPQC SDK under its included license terms. This downloads the official 0.6.0 x86_64 archive (about189 MB), checks SHA256 `8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571`, and extracts only under the fresh evidence directory. It does not install system-wide. Set `CUPQC_DOWNLOAD=0` to decline the download. CUDA must already be installed. SDK license files are included in the archive; see NVIDIA's download page for terms before running.
