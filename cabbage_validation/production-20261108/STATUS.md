# Cabbage combined search

Updated: 2026-11-09T23:46:25.450901+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,609,328,512**.
New replicated logical patches: **36,835,584** in 143,889 chunks.
Combined verified selected patches, including parents: **359,328,512**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2609328512]`.
Local cursor: 2,610,129,024; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 502.8560486062779, 'elapsed_seconds': 1621.9816623359802, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.32253334171863335, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 146948, 'prepare_wall_seconds': 1621.427742557309, 'producer_wait_capacity_seconds': 0.09505947917932644, 'producer_wait_full_seconds': 58.089948415989056, 'ready': 3, 'ready_depth_seconds': {'0': 1291.136651057459, '1': 219.97557713167043, '2': 29.44071059662383, '3': 81.42872247821651}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 18378, 'flush_seconds': 104.33848069736268, 'pending_bytes': 18221, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,163 patches/s**; new independent GMP audits: 1,149.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
