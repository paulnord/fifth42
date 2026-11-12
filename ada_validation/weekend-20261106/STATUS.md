# Ada combined search

Updated: 2026-11-12T23:00:11.430362+00:00

State: **stopped**. Run **ada-early31-p0001-560f185a37b6**; gpu with 16 preparation workers.
Verified replicated cursor: **8,990,258,176**.
New replicated logical patches: **6,258,176** in 24,446 chunks.
Combined verified selected patches, including parents: **6,258,176**.
Fresh interval: `[8984000000, 9048000000]`; replicated: `[8984000000, 8990258176]`.
Local cursor: 8,990,258,176; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 172.84012152033392, 'elapsed_seconds': 573.8991973130032, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15358227, 'mean_ready_depth': 0.24525895436197856, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 1528, 'prepare_wall_seconds': 573.4894582729321, 'producer_wait_capacity_seconds': 0.0016251176130026579, 'producer_wait_full_seconds': 32.85778175573796, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 433.1452779858373, '1': 140.753917042166}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 3056, 'flush_seconds': 23.881473123678006, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,905 patches/s**; new independent GMP audits: 191.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run covers a separately delegated claim31 suffix under its unchanged original reservation. The predecessor journal is provenance; only this run's native interval advances here. The original coordinator retains its parent lease; this early grant ends by its existing cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
