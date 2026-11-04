# four133 status on ADA

**Running; no modular candidates in the completed work.** Snapshot: November 4, 2026, 1:52:01 PM CST (19:52:01 UTC). This is a dated snapshot, not a live dashboard.

The equation is `a^133+b^133+c^133+d^133=42`, with signed integer bases and repeated bases retained. The verified inclusive ±4,000,000 box has no solutions. The active job searches the shell **4,000,000 < max|base| ≤ 10,800,000**. The larger full box is **not yet certified**.

| Item | Snapshot |
| --- | --- |
| Job | `B10800000-20261104T184003Z` |
| Started | November 4, 2026, 12:40:03 p.m. CST / 18:40:03 UTC |
| Resources | 16 CPU workers; no GPU |
| Time budget | 28,800 s; hard cap November 4, 8:40:03 p.m. CST / November 5, 02:40:03 UTC |
| Elapsed at snapshot | 72.0 minutes |
| Verified completed chunks | 3,378 / 10,474 |
| Completed gap cases across both moduli | 3,454,204 / 10,708,282 (32.3%) |
| Generated pair entries in completed chunks | 564,667,290,046 / 3,216,036,649,420 (17.6%) |
| Raw / canonical / distinct modular matches | 0 / 0 / 0 |
| Reported errors | None |
| Sampled peak combined worker RSS | 1585.4 MiB |
| CPU Tctl at snapshot | 78.375 °C |

Gap and entry percentages are coverage bookkeeping, not wall-time estimates. Active partial chunks are excluded. The original calibrated estimate was 7.37 hours plus coordinator overhead; the eight-hour budget is enforced even if the shell is incomplete. Dispatch stops 20 seconds early for cleanup. Completion or an exact candidate can stop the run earlier; there is no automatic continuation.

ADA has an **AMD Ryzen 9 5950X**, **16 physical cores / 32 hardware threads**, and **121.44 GiB OS-visible RAM** (130,392,805,376 bytes). The matched 1/8/16/32-worker comparison selected 16 workers: median wall times 30.770 / 4.569 / 2.841 / 3.103 seconds on identical 2,048-gap windows, with all counts and candidates identical. See [worker scaling](ada-extension/worker-scaling.json).

## Coverage by normalized case

The original ordinary sum is `s = sign*S`; normalization has target `T = sign*42`. Patterns 22 and 31 mean two positive/two negative and three positive/one negative after normalization. Every permitted `s=42+k*4,206,930` is considered, including additional two-positive cases beyond the old bound. The [general proof](ada-extension/PROOF.md) explains the sign reduction, strict and nonstrict gap bounds, shell condition, and repeated-base handling. Raising only the old program's numeric limit would omit cases.

Modulus A = `2305843009213693921`; modulus B = `2305843009213693951`. The last two columns count completed gap cases, not necessarily a contiguous prefix while workers finish out of order.

| Pattern | Original sum s | Normalized target T | Required gaps per modulus | Completed A | Completed B |
| --- | ---: | ---: | ---: | ---: | ---: |
| 31 | -21,034,608 | -42 | 160,000 | 160,000 | 160,000 |
| 31 | -16,827,678 | -42 | 160,000 | 160,000 | 160,000 |
| 31 | -12,620,748 | -42 | 160,000 | 160,000 | 160,000 |
| 22 | -8,413,818 | -42 | 1,173,374 | 1,173,374 | 1,173,374 |
| 31 | -8,413,818 | -42 | 128,455 | 73,728 | 73,728 |
| 22 | -4,206,888 | -42 | 829,698 | 0 | 0 |
| 31 | -4,206,888 | -42 | 64,227 | 0 | 0 |
| 22 | 42 | +42 | 2,621 | 0 | 0 |
| 22 | 4,206,972 | +42 | 829,706 | 0 | 0 |
| 31 | 4,206,972 | +42 | 64,228 | 0 | 0 |
| 22 | 8,413,902 | +42 | 1,173,379 | 0 | 0 |
| 31 | 8,413,902 | +42 | 128,456 | 0 | 0 |
| 31 | 12,620,832 | +42 | 159,999 | 0 | 0 |
| 31 | 16,827,762 | +42 | 159,999 | 0 | 0 |
| 31 | 21,034,692 | +42 | 159,999 | 0 | 0 |

## Evidence and validation

The pinned handoff is [commit 6160c2f](https://github.com/paulnord/fifth42/tree/6160c2f765c3898cb328968ad823dd13badd0ddd/four133/text). The full archived reproduction bundle (SHA-256 `2cfc019a955a8e5518ff027bf11c8585f0e197b6a9030c4b02dfd5a56ee5a050`) passed all nested manifest checks: 458 + 260 + 19 listed files. All three stages' raw-log audits were rerun in disposable copies and agreed with the saved reports, excluding elapsed audit times. The originals remain unchanged. See [prior verification](ada-extension/prior-verification.json).

The new source passed 60 independent Cartesian-oracle configurations with ASan/UBSan, 1,964 modular positive controls, 12 repeated-base controls, and 6 boundary controls. Thirty comparisons with a fresh build of the archived engine agreed on 834 canonical modular candidates. These controls **are not exact solutions to 42**. Coordinator tests cover completion/resume at 1/8/16 workers, STOP, budget expiration, changed/missing logs, changed source, exclusive locks, preservation of partial logs, and worker cleanup after coordinator SIGKILL.

Final B=10,800,000 calibration: 5,760 gap cases in 19.363 s wall, 297.964 s child CPU, 1631.4 MiB sampled combined RSS. A further 16-worker check using full 1,024-gap chunks covered 16,384 gap cases and 9,229,726,408 pair entries in 86.886 s wall / 1305.540 s child CPU, with no modular matches. The calibration windows are separate experiments, not additional completed full-box coverage.

This export rechecked frozen source/binary identities, the prior-verification identity, every available completed chunk's log hash, and its receipt's task/configuration identity. The coordinator had already independently reconciled each chunk's pair counts before committing its receipt. [status.json](status.json) records the snapshot counts and evidence hashes; it is not a resumable checkpoint. Logs, binaries, raw receipts, and checkpoints stay on ADA.

The two-minute thermal trace averaged Tctl 78.45 °C (77.875–80.25 °C), beginning 5.5 minutes after launch. Initial warm-up was not recorded; CPU fan RPM is not exposed by the available sensors. See [thermal samples](ada-extension/temperature.csv).

For review, start with [source and validation files](ada-extension/README.md), [search.cpp](ada-extension/src/search.cpp), [math133.py](ada-extension/math133.py), and [run.py](ada-extension/run.py). The published source hashes match the active frozen job. This status publication does not alter or restart the run.
