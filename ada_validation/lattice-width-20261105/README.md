# Certified width comparison — 2026-11-05

PASS: 80 timed CPU/CUDA pipeline observations, five rotating paired
repeats, 16 physical CPU workers, fresh preparation on every timed variant.
All widths passed exact certificates, full per-task count checks, independent
oracles at both benchmark bounds, and nonempty controls at 34 and 100.
The optimized packer is used throughout. Suite elapsed: 46.801 s.

| Bound | Width | Patches | Coefficient points | CPU pipeline (s) | CUDA pipeline (s) |
|---:|---:|---:|---:|---:|---:|
| 8,000 | 2 | 3,690 | 6,644,070 | 0.330578 | 0.327821 |
| 8,000 | 4 | 1,847 | 13,352,469 | 0.176402 | 0.170645 |
| 8,000 | 8 | 926 | 33,933,518 | 0.095180 | 0.082388 |
| 32,000 | 2 | 14,750 | 50,087,938 | 1.245089 | 1.225606 |
| 32,000 | 4 | 7,378 | 69,176,516 | 0.650113 | 0.626242 |
| 32,000 | 8 | 3,692 | 141,244,596 | 0.369570 | 0.318121 |

These are per-search medians with persistent engines and a worker pool.
At 32,000, CUDA width 2 took 1.225606 s and width 8 took 0.318121 s,
about 74.0% less time (3.85x throughput). Wider patches increased enumeration
from 50,087,938 to 141,244,596 points, while reducing patches from 14,750 to 3,692.

Actual cold one-pass CUDA medians were 1.687234 s (width 2) and 0.735301 s
(width 8), about 56.4% less time. Cold runs included actual pool/process startup
and shutdown. The corresponding CPU cold medians were 1.498399 and 0.596566 s.
Width 8/CUDA is the selected persistent configuration, rather than a claim
that CUDA wins cold one-pass searches. Broader widths have not been tested.

This comparison concerns the conservative coefficient-box pipeline. Earlier
CPU sphere/progression width measurements used a different enumeration method.
No speedup ratio combines those separate experiments. Every width covers the
same requested domain, with independently checked geometry for its own grid;
certificate and packet bytes are expected to differ between widths.

Full trial outputs remain on ADA under `${WIDTH_RUN_DIR}/trials`.
The report retains every trial filename/hash and per-sample stage timing.
Production and pinned lattice sources were preserved. See [live overnight status](../overnight-20261105/STATUS.md).
