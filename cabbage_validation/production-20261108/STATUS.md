# Cabbage combined search

Updated: 2026-11-11T19:21:42.889522+00:00

State: **running**. Run **cabbage-extended-r3-cap100-job-36-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,315,794,688**.
New replicated logical patches: **11,794,688** in 46,073 chunks.
Combined verified selected patches, including parents: **11,794,688**.
Fresh interval: `[9304000000, 9368000000]`; replicated: `[9304000000, 9315794688]`.
Local cursor: 9,315,919,616; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 383.17337208619574, 'elapsed_seconds': 1152.6499247719767, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3843157, 'mean_ready_depth': 0.2632090388153847, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 11586, 'prepare_wall_seconds': 1151.9647645134246, 'producer_wait_capacity_seconds': 0.008442460733931512, 'producer_wait_full_seconds': 247.92654324223986, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 849.2620429061353, '1': 303.3878787898575}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 5803, 'flush_seconds': 59.22551408747677, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,289 patches/s**; new independent GMP audits: 363.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
