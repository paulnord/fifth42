# Boole combined search

Updated: 2026-11-10T14:00:03.599181+00:00

State: **running**. Run **boole-delegated-20261109-02**; gpu with 16 preparation workers.
Verified replicated cursor: **7,182,589,696**.
New replicated logical patches: **54,589,696** in 213,241 chunks.
Combined verified selected patches, including parents: **54,589,696**.
Fresh interval: `[7128000000, 7192000000]`; replicated: `[7128000000, 7182589696]`.
Local cursor: 7,183,048,448; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 65.96649174776394, 'elapsed_seconds': 4521.656741020037, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482367, 'mean_ready_depth': 2.1728732074847916, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 214831, 'prepare_wall_seconds': 4520.8826637741295, 'producer_wait_capacity_seconds': 0.1411559347761795, 'producer_wait_full_seconds': 2028.4536241421592, 'ready': 3, 'ready_depth_seconds': {'0': 623.5925912702223, '1': 674.2259616148658, '2': 520.7537372541847, '3': 2703.0844499607338}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 26891, 'flush_seconds': 150.5682998894481, 'pending_bytes': 55246, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,162 patches/s**; new independent GMP audits: 1,679.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
