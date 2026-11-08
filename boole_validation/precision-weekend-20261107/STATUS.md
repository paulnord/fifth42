# Boole adaptive-precision search

Updated: 2026-11-08T23:02:07.921662+00:00

State: **running**. Continuation **boole-continuation-20261108**, GPU with 16 preparation workers.
Current cursor: **3,262,261,760**.
Combined committed patches: **262,261,760** across the sealed parent and this continuation.
New committed patches: **18,784,000** in 73,375 chunks.

Parent committed interval: `[3000000000, 3243477760]`.
Continuation interval: `[3243477760, 3750000000]`; committed: `[3243477760, 3262261760]`.
The continuation starts exactly at the independently sealed parent cursor under the original reservation.

Observed worker rate: **3,540 patches/s**; new independent GMP audits: 574.
Deadline: **2026-11-09T09:00:00-06:00**. Console-independent worker and deadline timer on Boole; reporter on Ada.
GitHub updates every **15 minutes**, plus a terminal snapshot.
Alerts: None reported.

This continuation has a 32 GiB journal budget;
the parent and continuation together have a 64 GiB allowance.
Storage limits may stop the run before the deadline.

Source manifest: `dc2c91a39e6e72a25199665edc81d057c61da8509b664c62f59740045f6f8a9a`.
[Configuration](evidence/continuation-configuration.json), [parent audit](evidence/parent-audit.json),
[launch evidence](evidence/continuation-launch.json), [storage limits](evidence/continuation-limits.json).
The parent raw journal hash matches Ada's separately captured baseline. Receipts are verified; historical coefficients were not recomputed.
Selected early-interval coverage only. Ada's coverage is separate. No completed full-box bound.

[Ada's separate search](../../ada_validation/weekend-20261106/STATUS.md).
