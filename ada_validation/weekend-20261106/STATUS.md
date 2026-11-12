# Ada combined search

Updated: 2026-11-12T22:50:24.098266+00:00

State: **running**. Run **ada-early31-p0001-560f185a37b6**; gpu with 16 preparation workers.
Verified replicated cursor: **8,984,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[8984000000, 9048000000]`; replicated: `[8984000000, 8984002048]`.
Local cursor: 8,984,196,608; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2.9819855869282037, 'elapsed_seconds': 10.000063064973801, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15351867, 'mean_ready_depth': 0.2679445917367002, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 27, 'prepare_wall_seconds': 9.96750158118084, 'producer_wait_capacity_seconds': 3.223586827516556e-05, 'producer_wait_full_seconds': 0.6430521049769595, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 7.320597835700028, '1': 2.6794628152856603}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 50, 'flush_seconds': 0.3451827197568491, 'pending_bytes': 105444, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,238 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run covers a separately delegated claim31 suffix under its unchanged original reservation. The predecessor journal is provenance; only this run's native interval advances here. The original coordinator retains its parent lease; this early grant ends by its existing cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
