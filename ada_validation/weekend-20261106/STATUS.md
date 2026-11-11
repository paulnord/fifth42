# Ada combined search

Updated: 2026-11-11T10:26:10.186893+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,785,702,784**.
New replicated logical patches: **898,367,488** in 3,509,248 chunks.
Combined verified selected patches, including parents: **3,035,702,784**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6785702784]`.
Local cursor: 6,786,866,048; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11152.342425126059, 'elapsed_seconds': 50864.584909974015, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3791489844839832, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 219580, 'prepare_wall_seconds': 50858.353695816244, 'producer_wait_capacity_seconds': 0.21772371686529368, 'producer_wait_full_seconds': 11431.581715006207, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 31579.329194066, '1': 19285.255714815983}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 439158, 'flush_seconds': 2852.3324008352356, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,682 patches/s**; new independent GMP audits: 27,448.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
