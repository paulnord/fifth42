# Ada combined search

Updated: 2026-11-10T22:08:41.148861+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,012,541,824**.
New replicated logical patches: **125,206,528** in 489,088 chunks.
Combined verified selected patches, including parents: **2,262,541,824**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6012541824]`.
Local cursor: 6,013,705,088; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1591.1486921968753, 'elapsed_seconds': 6623.361768419971, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681797, 'mean_ready_depth': 0.3391877619817286, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 30850, 'prepare_wall_seconds': 6622.048512470268, 'producer_wait_capacity_seconds': 0.030653259716928005, 'producer_wait_full_seconds': 1170.2232956076623, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 4376.798510759254, '1': 2246.563255025714}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 61696, 'flush_seconds': 400.49195552885067, 'pending_bytes': 18420, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,077 patches/s**; new independent GMP audits: 3,857.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
