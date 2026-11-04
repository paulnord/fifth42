# Verified search coverage

The largest completed box is **[-70,000,000,70,000,000]^3**, with no solutions
to x^5+y^5+z^5=42. All sign combinations are covered using the proved modulo-11
role assignment and ordering a<=b. This does not rule out larger solutions.

| Backend | Inclusive box bound | Completed canonical rows | Exact steps | Solutions |
| --- | ---: | ---: | ---: | ---: |
| CPU | 10,000 | 1,819 | 16,536,529 | 0 |
| CPU | 100,000 | 18,181 | 1,652,834,710 | 0 |
| GPU | 100,000 | 18,181 | 1,652,834,710 | 0 |
| GPU | 1,000,000 | 181,819 | 165,290,016,529 | 0 |
| GPU | 10,000,000 | 1,818,181 | 16,528,919,834,710 | 0 |
| GPU | 35,000,000 | 6,363,637 | 202,479,360,247,934 | 0 |
| GPU (192-bit) | 70,000,000 | 12,727,273 | 789,730,204,184,468 | 0 |

## Overnight result, checked November 4, 2026

**Complete, exit code 0, no solutions.** The 70-million run committed all
12,727,273 rows in 195 contiguous chunks (65,536 rows per full chunk). Its z
values span -69,999,996 through +69,999,996 in steps of 11; the other variables
span the full inclusive bound in all admissible residue classes. The extended
GPU engine used exact signed 192-bit arithmetic and the `highword` variant.

| Timing | Recorded value |
| --- | --- |
| Job started | November 3, 2026, 17:43:48 CST / 23:43:48 UTC |
| Job finished | November 3, 2026, 20:59:26 CST / November 4, 02:59:26 UTC |
| GPU search, summed across chunks | 11,242.0431 s (3h 7m 22s) |
| Engine setup, summed across chunks | 434.13082 s (included in engine wall time) |
| Engine wall time, summed across chunks | 11,736.239574 s (3h 15m 36s) |
| Total job elapsed time | 11,738.294699 s (3h 15m 38s) |
| Approved outer cap / inner runner budget | 28,800 s (8h) / 28,740 s |

The job finished normally before either budget expired. Calibration's rough
5.33-hour projection was separate from the measured timings above.

ADA at Valparaiso has an **AMD Ryzen 9 5950X 16-Core Processor**, **16 physical
cores / 32 logical CPUs**, and **121.44 GiB OS-visible RAM**
(130,392,805,376 bytes from Linux `MemTotal`). The RAM figure is the OS-reported
usable total. The search used its **NVIDIA GeForce RTX 3080 Ti**, CUDA 12.8 and
g++-13.

The final job record and log agree with the checkpoint. Rechecking
`extended.run.coverage` validated chunk continuity, metadata, step counts and
candidate records. Saved passing GPU validation and current source/binary
fingerprints match the run. No search or GPU validation was rerun for this
update. The compact [70-million result](results/gpu-B70000000.json) preserves
exact counts, timings, verification evidence and hashes.

## Earlier baseline runs

The 35-million run committed 98 chunks, with z from -34,999,998 through
+34,999,998 in steps of 11. Search time was 2,749.48181 seconds and engine wall
time 2,856.43546 seconds. Its outer one-hour timeout was not reached.

Every original checkpoint's row continuity, metadata, candidates and fingerprints
were checked. The committed [baseline results](results/coverage.json) retain the
source/binary hashes, exact counts and timing, while raw checkpoints, binaries
and local machine identifiers remain untracked. Test-only alternate targets,
CPU emulation and benchmark samples do not confer additional full-box coverage.

The GPU proof of concept was executed on Ada's RTX 3080 Ti with CUDA 12.8 and
g++-13. The restricted agent session could inspect files and compile but could
not access device nodes; GPU execution took place in the user's normal terminal.
No BNL resources were used.
