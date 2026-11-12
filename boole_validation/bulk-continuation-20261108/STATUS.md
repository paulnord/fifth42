# Boole combined search

Updated: 2026-11-12T14:52:12.388402+00:00

State: **running**. Run **boole-range-r3-20261111-27-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,777,772,800**.
New replicated logical patches: **49,772,800** in 194,425 chunks.
Combined verified selected patches, including parents: **49,772,800**.
Fresh interval: `[8728000000, 8792000000]`; replicated: `[8728000000, 8777772800]`.
Local cursor: 8,778,112,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.16046533116605133, 'elapsed_seconds': 6310.320280957036, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682331, 'mean_ready_depth': 0.999376162889331, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 12218, 'prepare_wall_seconds': 6308.105860179057, 'producer_wait_capacity_seconds': 0.016567896818742156, 'producer_wait_full_seconds': 4159.7793552880175, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.936608611489646, '1': 6306.383668985567}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 24467, 'flush_seconds': 190.01156092283782, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,929 patches/s**; new independent GMP audits: 1,528.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
