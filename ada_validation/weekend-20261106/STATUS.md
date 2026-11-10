# Ada combined search

Updated: 2026-11-10T23:38:57.461844+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,114,249,600**.
New replicated logical patches: **226,914,304** in 886,384 chunks.
Combined verified selected patches, including parents: **2,364,249,600**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6114249600]`.
Local cursor: 6,114,704,256; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2859.344065687328, 'elapsed_seconds': 12032.534482694988, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34413337767307595, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 55476, 'prepare_wall_seconds': 12030.894435311726, 'producer_wait_capacity_seconds': 0.05506258684908971, 'producer_wait_full_seconds': 2198.133014866151, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 7891.737746732426, '1': 4140.796733497584}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 110951, 'flush_seconds': 719.174547476403, 'pending_bytes': 128919, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,884 patches/s**; new independent GMP audits: 6,935.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
