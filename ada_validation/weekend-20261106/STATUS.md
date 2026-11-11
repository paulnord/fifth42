# Ada combined search

Updated: 2026-11-11T09:10:57.647283+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,711,942,016**.
New replicated logical patches: **824,606,720** in 3,221,120 chunks.
Combined verified selected patches, including parents: **2,961,942,016**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6711942016]`.
Local cursor: 6,713,209,728; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10265.224612318212, 'elapsed_seconds': 46354.80145141302, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3751284887360492, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 201610, 'prepare_wall_seconds': 46348.484455589845, 'producer_wait_capacity_seconds': 0.19986735569546, 'producer_wait_full_seconds': 10196.811671065807, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 28965.79483449983, '1': 17389.006614128186}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 403216, 'flush_seconds': 2620.82667549653, 'pending_bytes': 18419, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,814 patches/s**; new independent GMP audits: 25,202.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
