# Boole combined search

Updated: 2026-11-10T05:45:48.717015+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **229,179,392**.
New replicated logical patches: **129,179,392** in 504,607 chunks.
Combined verified selected patches, including parents: **129,179,392**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 229179392]`.
Local cursor: 230,548,224; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1670.124315421097, 'elapsed_seconds': 7208.6614327399875, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 547058, 'mean_ready_depth': 0.5403326516885182, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 509731, 'prepare_wall_seconds': 7206.918479195563, 'producer_wait_capacity_seconds': 0.3102349378168583, 'producer_wait_full_seconds': 886.0250799063942, 'ready': 1, 'ready_depth_seconds': {'0': 5491.630320717639, '1': 564.7094203094603, '2': 126.59934585099109, '3': 1025.7223450219026}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 63820, 'flush_seconds': 349.6809467058047, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,100 patches/s**; new independent GMP audits: 3,983.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
