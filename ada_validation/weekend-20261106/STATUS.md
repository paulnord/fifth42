# Ada combined search

Updated: 2026-11-11T00:09:04.556230+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,147,308,416**.
New replicated logical patches: **259,973,120** in 1,015,520 chunks.
Combined verified selected patches, including parents: **2,397,308,416**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6147308416]`.
Local cursor: 6,147,967,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 3275.7422727638623, 'elapsed_seconds': 13837.471519250015, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34578882951943374, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 63586, 'prepare_wall_seconds': 13835.195358162804, 'producer_wait_capacity_seconds': 0.06314032775117084, 'producer_wait_full_seconds': 2553.76717037661, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 9052.628435984021, '1': 4784.8430801499635}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 127168, 'flush_seconds': 824.377235869586, 'pending_bytes': 18418, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,821 patches/s**; new independent GMP audits: 7,949.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
