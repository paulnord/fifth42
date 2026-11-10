# Boole combined search

Updated: 2026-11-10T12:32:50.373426+00:00

State: **running**. Run **boole-delegated-20261109-01**; gpu with 16 preparation workers.
Verified replicated cursor: **7,119,251,200**.
New replicated logical patches: **55,251,200** in 215,825 chunks.
Combined verified selected patches, including parents: **55,251,200**.
Fresh interval: `[7064000000, 7128000000]`; replicated: `[7064000000, 7119251200]`.
Local cursor: 7,119,675,136; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 76.75511776673375, 'elapsed_seconds': 4518.0237920630025, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482111, 'mean_ready_depth': 2.1079427717367802, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 217458, 'prepare_wall_seconds': 4517.253178631363, 'producer_wait_capacity_seconds': 0.13752786605618894, 'producer_wait_full_seconds': 1991.4764452743693, 'ready': 1, 'ready_depth_seconds': {'0': 699.6408212979441, '1': 712.3067063853377, '2': 506.7999003705336, '3': 2599.2763626292}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 27209, 'flush_seconds': 154.70248822955182, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,321 patches/s**; new independent GMP audits: 1,699.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
