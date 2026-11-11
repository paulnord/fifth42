# Ada combined search

Updated: 2026-11-11T00:24:08.150021+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,163,225,472**.
New replicated logical patches: **275,890,176** in 1,077,696 chunks.
Combined verified selected patches, including parents: **2,413,225,472**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6163225472]`.
Local cursor: 6,164,525,952; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 3484.16281862749, 'elapsed_seconds': 14741.297706995974, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34660611130189745, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 67634, 'prepare_wall_seconds': 14738.93413487461, 'producer_wait_capacity_seconds': 0.06715156137943268, 'producer_wait_full_seconds': 2735.440513722191, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 9631.873830865545, '1': 5109.423873765452}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 135264, 'flush_seconds': 877.008893398568, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,792 patches/s**; new independent GMP audits: 8,455.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
