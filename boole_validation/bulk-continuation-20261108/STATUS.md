# Boole combined search

Updated: 2026-11-10T03:16:45.427000+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,722,266,368**.
New replicated logical patches: **251,863,296** in 983,841 chunks.
Combined verified selected patches, including parents: **722,266,368**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3722266368]`.
Local cursor: 3,723,759,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1687.363253435993, 'elapsed_seconds': 14094.180293947982, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9816069589887325, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 989486, 'prepare_wall_seconds': 14082.003407889977, 'producer_wait_capacity_seconds': 0.622120242274832, 'producer_wait_full_seconds': 2670.8925493185525, 'ready': 3, 'ready_depth_seconds': {'0': 7794.979527271178, '1': 2185.6300867439713, '2': 691.3966659412836, '3': 3422.1740130515536}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 123889, 'flush_seconds': 725.3105628865887, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **17,971 patches/s**; new independent GMP audits: 7,731.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
