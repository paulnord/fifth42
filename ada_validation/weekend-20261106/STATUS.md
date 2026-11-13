# Ada combined search

Updated: 2026-11-13T00:26:18.418456+00:00

State: **stopped**. Run **ada-sharing-30-6857e3975a144414**; gpu with 16 preparation workers.
Verified replicated cursor: **8,984,000,000**.
New replicated logical patches: **11,273,984** in 44,039 chunks.
Combined verified selected patches, including parents: **11,273,984**.
Fresh interval: `[8972726016, 8984000000]`; replicated: `[8972726016, 8984000000]`.
Local cursor: 8,984,000,000; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 315.3364264932461, 'elapsed_seconds': 1032.5199638770428, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357160, 'mean_ready_depth': 0.2435124420742894, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 2753, 'prepare_wall_seconds': 1031.6393303489313, 'producer_wait_capacity_seconds': 0.0028484200593084097, 'producer_wait_full_seconds': 59.54975520912558, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 781.0885022347793, '1': 251.43145789415576}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 5505, 'flush_seconds': 43.65996604645625, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,919 patches/s**; new independent GMP audits: 345.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run covers its assigned sealed r4 suffix under an unchanged original child claim. The predecessor journal is provenance; only this run's native interval advances here. The renewed coordinator holds the original parent lease until the new cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
