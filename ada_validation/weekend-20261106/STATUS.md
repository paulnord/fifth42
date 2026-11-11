# Ada combined search

Updated: 2026-11-11T18:28:16.775361+00:00

State: **stopped**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **7,000,000,000**.
New replicated logical patches: **76,277,888** in 297,961 chunks.
Combined verified selected patches, including parents: **3,250,000,000**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 7000000000]`.
Local cursor: 7,000,000,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 877.514221487043, 'elapsed_seconds': 4773.815578546026, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681850, 'mean_ready_depth': 0.4528258405096757, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 18623, 'prepare_wall_seconds': 4773.148419873964, 'producer_wait_capacity_seconds': 0.018225886509753764, 'producer_wait_full_seconds': 1492.2074259324581, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 2612.108523195726, '1': 2161.707051793288}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 37246, 'flush_seconds': 237.0228981070104, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **15,978 patches/s**; new independent GMP audits: 2,328.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
