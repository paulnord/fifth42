# Cabbage root-preparation comparison: completed GPU measurements

**GMP was faster than both GPU implementations at every tested batch size.**
Both libraries passed GPU correctness after isolated build-environment repairs.
Dot's CUDA/Python sources and `SHA256SUMS` remain unchanged at
[`e6979d463aa8c22f627f5d40955750c6472850ee`](https://github.com/paulnord/fifth42/tree/e6979d463aa8c22f627f5d40955750c6472850ee/experiments/gpu-root-prep-20261110).
The earlier failed-build evidence remains intact in `../cabbage-20261110-r1/`.

| Accepted roots | CPU GMP batch median | Best CGBN warm kernel | Best cuPQC warm kernel |
| ---: | ---: | ---: | ---: |
| 252 | 0.325 ms | 1.605 ms (TPI 16) | 1.588 ms (TPI 16) |
| 1,020 | 1.262 ms | 4.157 ms (TPI 16) | 4.055 ms (TPI 16) |
| 4,092 | 4.905 ms | 11.802 ms (TPI 4) | 11.950 ms (TPI 8) |

Requested batches were 256/1024/4096. Four over-width cases per fixture set
were explicitly rejected by the 2048-bit proof and are fully listed in
`UNSUPPORTED_CASES.json`. All accepted GPU outputs equal the GMP roots and
satisfy the exact two integer inequalities; no truncation or guard bypass.

GPU values are the median of kernel repetitions 1–5, choosing the best of
TPI 4/8/16/32 for each library and batch. GMP values are the median of eight
single-batch measurements on the identical inputs, one per GPU variant.
`ANALYSIS.json` retains all variants, all six kernel samples, GMP samples,
first-repeat times, process times, certificate costs and input/output hashes.
`SUMMARY.json` is Dot's original unmodified 24-row summary.
Every GPU variant's warm median was slower than its paired GMP sample.

For the selected variants, first-kernel times (CGBN/cuPQC) were 1.717/1.719 ms,
4.239/4.143 ms and 11.971/12.045 ms at the respective batch sizes. Whole GPU
processes took 224–321 ms, including CUDA startup, file I/O and **six** kernel
repetitions. Those process times must not be compared as equal-work timing
against one GMP batch. Warm kernels alone already lost to GMP, before transfer,
packing and CPU certification costs. No whole-fifth42-pipeline gain is claimed.

These results describe the supplied 2048-bit, division-free, bit-by-bit root
kernels. They do not establish limits of CGBN, cuPQC or a different GPU root
algorithm. There is no evidence here supporting replacement of production GMP.
The small kernels produced short GPU bursts; one-second utilization sampling
can miss them. Raw CUDA-event timings verify the actual device executions.

## Correctness before the timing sweep

The separate gate first passed 41,200 exhaustive CPU rational tests and 424
archived-reference comparisons. CGBN and cuPQC then each passed exact GPU/GMP
checks at all four TPI settings (252 accepted roots per invocation). Sixteen
native malformed/domain/width rejection tests passed. Only then did the
unchanged published `run.sh` execute the 24 timing cases, with every case
certified again. There were 44,928 final GPU root certificates across preflight
and sweep. Inputs and final outputs are byte-identical across all variants
for each batch size. Each invocation repeats the kernel six times and exports
one final output array; the certificate count refers to exported final roots.

## Build setup repaired locally

Both dependency downloads were correct. The CGBN checkout is pinned to
`114601b07ae8c3e4d46b250208ea8d9def7a12f0`; the official cuPQC 0.6.0 archive
matches SHA256 `8026ac00d81130180d2ff0afb3eb9bce852b76cc6a02141f9e45b799a17ae571`.

1. CGBN's host header requires GMP to be included first. The local compiler
   wrapper pre-includes the actual `gmp.h` and links `-lgmp` for `root_cuda.cu`.
   It does not fake a guard macro, disable checks or edit the root source.
2. A standalone CUDA LTO program reproduced the cuPQC build failure without
   using cuPQC. Loader tracing showed `nvlink` seeking
   `nvvm/lib64/libnvvm.so`, while this pip-installed CUDA toolkit stores
   `lib/libnvvm.so.4`. A **separate scratch toolkit layout** copies the existing
   nvcc/profile, links its existing tools/includes/libraries, and supplies the
   expected NVVM path. The original toolkit remains unchanged.

With that layout, standalone CUDA LTO and both upstream GPU addition examples
passed. CGBN's example verified 100,000 1024-bit additions. cuPQC's example
returned 2+3=5 and 10+20=30. The installation logs and source hashes/outputs are
retained, with the full loader trace compressed separately. The cuPQC SDK,
CUDA binaries and proprietary library contents are not redistributed.

Hardware: RTX 3060 (Ampere SM86), Ryzen 9 5950X (16 physical cores/32 threads),
NVIDIA driver 595.99.02, CUDA 13.2.78, g++-13, Python 3.12.16, gmpy2 2.2.2,
GMP 6.3.0. The existing GPU lease was held and the device was idle before
launch. Detailed versions and unrelated activity are recorded in `logs/`.

## Reproduction and complete evidence

Use the unchanged pinned package with a fresh local evidence directory and
the build wrapper in `harness/nvcc-wrapper.sh`. The actual compiler arguments
and commands are in `commands.json` and `run.log`. The wrapper names the
scratch CUDA layout used in this run. To recreate the layout, copy nvcc and
nvcc.profile into a fresh `cuda/bin/`; symlink the remaining bin tools and
include/lib directories to the existing CUDA toolkit; link `cuda/nvvm/bin`
and `cuda/nvvm/libdevice`; and point `cuda/nvvm/lib64/libnvvm.so` to the existing
`lib/libnvvm.so.4`. Select g++-13. Retain the GMP pre-include/link flags for
CGBN. `harness/run_comparison.py` performs both exact preflight gates and then
runs Dot's original runner. Existing pinned CGBN/cuPQC dependencies were reused
without changing their contents; all required hashes were verified again.

`raw-gpu-evidence.tar.gz` contains every fixture, final GPU output, report,
per-kernel timing log and unsupported-input record. Every member is indexed
by size and SHA256 in `RAW_EVIDENCE_MANIFEST.json`. The published file hashes
are in `SHA256SUMS`, and `READY.json` is written last.

Production remains stopped. Its final worker exit was 0 and the final NFS
checkpoint was verified. The earlier controller stop-reporting race is preserved
in the evidence. No production source/configuration was changed or restarted.
