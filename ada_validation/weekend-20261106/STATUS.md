# Ada combined search

Updated: 2026-11-10T22:23:44.681555+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,029,616,000**.
New replicated logical patches: **142,280,704** in 555,784 chunks.
Combined verified selected patches, including parents: **2,279,616,000**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6029616000]`.
Local cursor: 6,030,695,296; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1803.2197152243461, 'elapsed_seconds': 7517.017986306979, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681797, 'mean_ready_depth': 0.3398204986079276, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 34954, 'prepare_wall_seconds': 7515.585633477662, 'producer_wait_capacity_seconds': 0.03473508404567838, 'producer_wait_full_seconds': 1334.9924853027915, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4962.581184011418, '1': 2554.4368001515977}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 69904, 'flush_seconds': 453.25927189103095, 'pending_bytes': 18400, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,045 patches/s**; new independent GMP audits: 4,370.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
