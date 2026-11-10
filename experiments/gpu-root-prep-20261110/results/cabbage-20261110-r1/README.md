# Cabbage GPU root-preparation results — 10 November 2026

**Both GPU backends are blocked at compilation. The timing sweep was not run.**
This is a test of Dot's unchanged package at
[`e6979d463aa8c22f627f5d40955750c6472850ee`](https://github.com/paulnord/fifth42/tree/e6979d463aa8c22f627f5d40955750c6472850ee/experiments/gpu-root-prep-20261110).

| Backend | Actual result | GPU vs GMP comparison |
| --- | --- | --- |
| CGBN, pinned `114601b07ae8c3e4d46b250208ea8d9def7a12f0` | TPI 4 compile fails in `cgbn_cpu.h`: `#error You must use GMP for now` | Unavailable |
| cuPQC 0.6.0, verified official archive | TPI 4 CUDA LTO link fails: `nvlink fatal : elfLink linker library load error` | Unavailable |
| GMP 6.3.0 through gmpy2 2.2.2 | All accepted fixture roots match the independent Python result | CPU samples below |

The first failed build stops that backend. TPI 8/16/32, GPU certificate checks,
first/warm kernel repetitions, whole-process GPU timings and the sweep are
explicitly unexecuted. No CUDA pass or speedup is claimed. The two independent
backend build attempts are both recorded; no failed guard was bypassed.

Before GPU builds, the exact CPU gate passed **41,200 exhaustive rational cases**,
wrong-candidate rejections and width guards. The archived oracle comparison passed
**424 cases** across three implementations, including 189 production-shaped roots.
GMP also agreed on the accepted 2048-bit fixtures. Four over-width cases per
requested batch were rejected explicitly, with full rational inputs, required
bit widths and reasons in `UNSUPPORTED_CASES.json` and the raw archive.

| Requested batch | Accepted roots | GMP preflight batch time |
| ---: | ---: | ---: |
| 256 | 252 | 0.316534 ms |
| 1024 | 1020 | 1.213385 ms |
| 4096 | 4092 | 4.984006 ms |

These are single preflight samples from the unchanged checker, not repeated
performance estimates or a GPU timing comparison.

Hardware: Ryzen 9 5950X (16 physical cores/32 threads), RTX 3060 (SM86),
NVIDIA driver 595.99.02. Compiler: CUDA 13.2.78 with existing g++-13 selected
by a local wrapper. Python 3.12.16, gmpy2 2.2.2, GMP 6.3.0. Detailed hardware,
compiler, CPU activity and version output is retained under `logs/`.
The GPU was idle before testing; its existing exclusive host lease was held.

CGBN and the proprietary NVIDIA cuPQC SDK were installed only inside a fresh
scratch evidence directory. The cuPQC archive matched the handoff's pinned
SHA256. The published CUDA/Python sources and checksum file were unchanged.
The CGBN installation includes its GMP host adapter and its sample explicitly
includes `<gmp.h>` before the CGBN header; this test source does not. The system
GMP header exists, so this is a published-source/include-order build blocker,
not absence of the measured Python GMP backend. The cuPQC linker error is
reported as observed; its underlying cause has not been established.

Production was stopped at the user's explicit instruction before this isolated
experiment, overriding the older handoff's instruction to leave it running.
The active production worker exited 0, released its leases, and its final local
and NFS checkpoints match at **cell 1,538,849,024**. The controller recorded a
stop-reporting race (`KeyError: worker_exit_code`) while the supervisor finished;
that traceback and final supervisor/replica proofs are preserved. Production
source/configuration was not edited and production was not restarted.

## Evidence and reproduction

- `SUMMARY.json`: complete machine-readable outcomes and available GMP samples.
- `run.log`, `logs/`, `commands.json`: full commands, return codes, stdout/stderr.
- `raw-correctness-evidence.tar.gz`: every generated input, raw report and rejected
  case list; `RAW_EVIDENCE_MANIFEST.json` records each member's bytes and SHA256.
- `tested-package.tar.gz`: the unchanged package and archived reference source.
- `harness/`: exact local orchestration and compiler-selection wrapper.
- `production-stop.json`: final checkpoint/supervisor/verified-copy evidence.
- `SHA256SUMS` and `READY.json`: publication integrity.

To repeat, create a fresh scratch root; clone fifth42 into its `repo/` subdirectory,
checkout the immutable commit above, copy `harness/run_comparison.py` into that
root and `harness/nvcc-wrapper.sh` into `toolchain/nvcc` (executable), and create
`evidence/`. Run the orchestration with Cabbage's pinned Python:

```sh
/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python3 -B run_comparison.py
```

It takes the existing Cabbage GPU lease, checks for an idle GPU, installs the
pinned dependencies locally, runs CPU correctness and both build/certificate
gates, and invokes Dot's unmodified `run.sh` only if both GPU gates pass.
It does not stop or restart production. The raw cuPQC SDK, its libraries and
CUDA executables are retained locally and are not redistributed in this report.
