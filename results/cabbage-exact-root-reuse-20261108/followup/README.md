# Cabbage CUDA follow-up — 2026-11-08

**Range setup fixed; baseline/candidate GPU correctness passed. Timing stopped on a resource conflict after 10 complete pairs (21 completed trials of 30 planned). No deployment or new production coverage.**

This follows the [initial CPU pass and CUDA range rejection](../README.md). All work used a new local scratch directory on Cabbage. No NFS mount was needed or used; Ada, Boole, production services, journals, checkpoints and the shared production ledger were not accessed or changed.

## What was fixed

The raw CUDA source defaults to a 100-billion base limit. The pinned worker already has `overnight_search.extend_arithmetic_range`, which raises that limit to 200 billion in a scratch copy and verifies the arithmetic before the larger shell runs. The initial CUDA build omitted this setup step; the packaged CPU native baseline already included it.

The [range-extension patch](range-extension.patch) changes only `LATTICE_MAX_BASE` in the scratch shared engine header. The resulting header is byte-for-byte identical to the already validated pinned CPU native header. The exact integer proof [3 B^5 + 2^63 < 2^191, B=200,000,000,000](range-proof.json) leaves signed 192-bit headroom for fifth powers, sums, residuals and the cap. Accepted coefficient transforms retain their signed-64-bit overflow checks. Inputs above the limit still reject.

The saved-root optimization itself was not changed. Both Python source variants remained copies of the original pinned baseline/candidate, and both used the same range-corrected CUDA enumeration binary. No production launcher was run.

## Environment and commands

- Host: Cabbage; Ryzen 9 5950X, 16 cores / 32 logical CPUs, 125 GiB RAM. Initial load 0.15/0.31/0.41, about 120 GiB available. No competing compute work observed before the tests.
- GPU: RTX 3060, 12 GiB, driver 595.99.02. Initially 0% / 25 MiB / Xorg only, no compute processes.
- Reused the isolated Python 3.12.16 environment: sympy 1.14.0, fpylll 0.6.4, cysignals 1.12.5, numpy 2.3.5, gmpy2 2.2.2; mpmath 1.3.0.
- Scratch CUDA nvcc/CRT/NVVM 13.2.78, runtime 13.2.75; g++-13 13.4.0; `-O3 -std=c++17 -arch=sm_86` for CUDA, UBSan checks built separately.
- Tested handoff: `be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f`, source baseline `da4e1e312ce1558c9d8cf027c009f8b400f22b83`. Original archive and package hashes passed in the initial test.

The retained scripts document the exact setup and execution. These are historical commands, using the original scratch paths:

```sh
cd /home/pnord/scratch/saved-root-followup-DL829jCa
PY=/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python
"$PY" prepare.py
cp /home/pnord/scratch/saved-root-pAjTHBhR/cpu/run_probe.py ./run_probe.py
cp /home/pnord/scratch/saved-root-pAjTHBhR/cpu/test_root_reuse.py ./test_root_reuse.py
timeout 120 sh build.sh > build.txt 2>&1
# Initial harness attempt stopped on a copied reference executable lacking execute permission:
"$PY" resource_runner.py range-tests "$PY" range_tests.py
# Rebuild that reference in scratch, then rerun:
g++-13 -std=c++17 -O3 -Wall -Wextra -Werror baseline/independent/gmp_reference.cpp -lgmpxx -lgmp -o native/bin/gmp_reference
"$PY" resource_runner.py range-tests-retry "$PY" range_tests.py
"$PY" make_gpu_probe.py
"$PY" resource_runner.py gpu-suite "$PY" gpu_suite.py
# After the resource conflict stopped testing, collect completed evidence only:
"$PY" collect_results.py
```

[build.sh](build.sh) contains every device and CPU compile command. [prepare.py](prepare.py) and [make_gpu_probe.py](make_gpu_probe.py) show the exact scratch transformations. The initial harness failure was a file-mode setup error, not a mathematical discrepancy; its log is retained. No mathematical mismatch or timeout occurred.

## Correctness results

- **708 signed arithmetic cases per backend passed** on native CPU, UBSan CPU and CUDA against Python arbitrary-precision integers. These include zero, signs, 32-bit limb boundaries, both sides of the old limit, both signs near the new limit, and 512 seeded random pairs. Exact fifth powers, sums, negated sums, five-square limits and signed comparisons agreed.
- Boundary enumeration at 100,000,000,001 and 200,000,000,000 passed exact expected/visited counts and full native hit comparisons against the independent GMP implementation on CPU, UBSan CPU and CUDA. A large nonempty Healy fixture passed. Deliberate above-limit and transform-overflow controls rejected on all three backends as expected.
- **All eight CUDA validation cases matched between saved-root baseline and candidate**: three nonempty complete positive small domains (34/384, 100/2951, 1000/42) and five four-patch high-shell windows. Small-domain final hit counts, including direct host hits, were 6, 25 and 2. Exact per-task counts and full native hit records matched GMP; the small-domain exact hit sets matched the independent fifth-power-table oracle.
- Geometry, certificates, points and exact decoded hits also matched the prior CPU records. The follow-up did not rerun all 142 CPU tests; those passed in the initial reproduction, and the saved-root source variants are unchanged.
- **All 10 completed timing pairs matched** task/certificate/geometry/packet/count signatures, native candidate records, point counts and exact hit sets. Every completed trial passed its first-chunk GMP hit audit and local durable-prefix journal recovery. The interrupted candidate trial is excluded.

## Timing results

The steady pipeline includes fresh host preparation and certification on four logical CPUs, bounded prefetch, a persistent native CUDA engine, exact response verification, first-chunk GMP hit audit and local durable journal commits. Startup/shutdown are separate. Reported improvement is for this bounded CPU-preparation-plus-CUDA pipeline, not a faster CUDA kernel. The saved-root patch does not change the kernel.

| Window | Completed pairs | Patches/trial | Baseline steady samples (s) | Candidate steady samples (s) | Median baseline/candidate (s) | Throughput ratio |
|---|---:|---:|---|---|---|---|
| boole | 5 | 4096 | 1.752527178, 1.752190932, 1.766714033, 1.756415273, 1.786128436 | 1.679725766, 1.700460821, 1.711756088, 1.681338382, 1.698729715 | 1.756415273/1.698729715 | 1.033958x |
| ada | 5 | 4096 | 1.761835739, 1.745395118, 1.770218335, 1.774053759, 1.749491839 | 1.698793461, 1.700545724, 1.697192715, 1.704088118, 1.694224305 | 1.761835739/1.698793461 | 1.037110x |
| higher_cost | 0 | 1024 | 0.856342603 | — | 0.856342603/— | not paired |

Window labels denote numeric test windows on Cabbage, not connections to other hosts. The two completed windows measured about **3.4% and 3.7% higher median pipeline throughput**. These short observations do not establish a general or production speedup. No higher-cost ratio is reported from its single unpaired baseline.

Raw CUDA event kernel sums in the two complete windows:

| Window | Baseline kernel sums (s) | Candidate kernel sums (s) |
|---|---|---|
| boole | 0.000961568, 0.000928704, 0.000934784, 0.000942816, 0.000937664 | 0.000960992, 0.000948768, 0.000968320, 0.000945984, 0.000952064 |
| ada | 0.001483712, 0.001465184, 0.001481216, 0.001499904, 0.001489888 | 0.001501920, 0.001474304, 0.001470016, 0.001472352, 0.001484480 |

The unpaired higher-cost baseline kernel sum was 0.008665830 s. Full-precision steady/startup/shutdown/engine/kernel/RPC timings for every completed trial are in [partial-benchmark-results.json](gpu-results/partial-benchmark-results.json); every individual packet timing is in [native-timings.json](gpu-results/native-timings.json). Transfer time is not separately instrumented.

## Resource conflict and stopping point

At 50.495 seconds into the suite, the external monitor detected two unrelated `java` processes (PIDs 298881 and 298894) consuming about 2.93 and 3.03 CPU cores. No foreign GPU process was present. The monitor terminated only our test process group immediately. The unrelated work was left untouched; no test was retried after this conflict.

Ten complete pairs had passed. The higher-cost baseline had completed; its candidate had started but produced no completed result. The suite therefore has **21 completed timing trials of 30 planned, 10 paired comparisons, and an incomplete higher-cost window**. It exited on the resource conflict, not on a correctness failure. The GPU returned to 0% / 25 MiB / Xorg only, and no test PIDs remained.

[resource_runner.py](resource_runner.py) sampled about every 0.5 seconds, checking for foreign CUDA compute processes and foreign processes above 0.5 CPU core over the sample interval. It also imposed a 600-second stage budget; each GPU request was bounded to 30 seconds and each trial subprocess to 140 seconds. Sampling cannot exclude shorter bursts of contention; monitor overhead, clock variation and brief scheduling delays limit the timing claims. The complete resource trace and failure record are retained.

## Evidence and remaining limits

- [Range proof](range-proof.json), [range-test results](range-test-results.json), [source/binary hashes](source-and-binary-identities.json), and the one-line [scratch guard patch](range-extension.patch).
- [Baseline CUDA validation](gpu-results/validation-baseline.json), [candidate validation](gpu-results/validation-candidate.json), and their raw count/hit/timing responses in the same directory.
- [Completed timing records and exact pair checks](gpu-results/partial-benchmark-results.json). Compact exact native packet/count/hit records are retained once per numeric window; all completed trials in each window matched those records. Original raw response files and detailed per-worker stage arrays remain local and are hashed in the publication manifest.
- [GPU suite output](gpu-suite.txt), [resource trace](gpu-suite-resources.jsonl), and [stop record](gpu-suite-failure.json). Harnesses are included for review, not as an automatic production launcher.
- [SHA256SUMS](SHA256SUMS) and [publication manifest](publication-manifest.json) identify the published evidence and local originals.
- No NFS/shared-ledger acceptance, deployment, full-shell result or new production coverage. Completing the higher-cost timing pairs requires another idle resource window.
