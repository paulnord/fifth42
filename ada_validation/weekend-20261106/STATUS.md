# Ada combined search

Updated: 2026-11-11T17:38:49.939677+00:00

State: **running**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **6,952,088,960**.
New replicated logical patches: **28,366,848** in 110,808 chunks.
Combined verified selected patches, including parents: **3,202,088,960**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 6952088960]`.
Local cursor: 6,953,049,472; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 339.0938292686478, 'elapsed_seconds': 1824.027855109016, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680760, 'mean_ready_depth': 0.4504757848381856, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7154, 'prepare_wall_seconds': 1823.062399878807, 'producer_wait_capacity_seconds': 0.006962232349906117, 'producer_wait_full_seconds': 563.9828241965733, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1002.3474718950456, '1': 821.6803795969463}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14304, 'flush_seconds': 90.43376843287842, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **16,060 patches/s**; new independent GMP audits: 895.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
