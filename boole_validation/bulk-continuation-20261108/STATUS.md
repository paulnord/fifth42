# Boole combined search

Updated: 2026-11-10T20:03:55.629554+00:00

State: **stopped**. Run **boole-delegated-20261109-06**; gpu with 16 preparation workers.
Verified replicated cursor: **7,437,246,208**.
New replicated logical patches: **53,246,208** in 207,993 chunks.
Combined verified selected patches, including parents: **53,246,208**.
Fresh interval: `[7384000000, 7448000000]`; replicated: `[7384000000, 7437246208]`.
Local cursor: 7,437,659,904; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 79.48188919067616, 'elapsed_seconds': 4764.892240863992, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 487141, 'mean_ready_depth': 2.1345154074812975, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 209610, 'prepare_wall_seconds': 4764.049938946904, 'producer_wait_capacity_seconds': 0.13615630473941565, 'producer_wait_full_seconds': 2231.574239041016, 'ready': 0, 'ready_depth_seconds': {'0': 739.0106085551088, '1': 705.3744927299558, '2': 496.15999986446695, '3': 2824.347136884462}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 26279, 'flush_seconds': 158.30237138830125, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,261 patches/s**; new independent GMP audits: 1,638.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
