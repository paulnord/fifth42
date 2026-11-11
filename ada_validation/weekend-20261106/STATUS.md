# Ada combined search

Updated: 2026-11-11T21:41:17.220135+00:00

State: **stopped**. Run **ada-allocated-r3-01-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,328,000,000**.
New replicated logical patches: **64,000,000** in 250,000 chunks.
Combined verified selected patches, including parents: **64,000,000**.
Fresh interval: `[10264000000, 10328000000]`; replicated: `[10264000000, 10328000000]`.
Local cursor: 10,328,000,000; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 7269.502098030469, 'elapsed_seconds': 11508.629600631015, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1924556, 'mean_ready_depth': 0.22404424776423132, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 250000, 'prepare_wall_seconds': 11506.631835443026, 'producer_wait_capacity_seconds': 0.17586295236833394, 'producer_wait_full_seconds': 560.1242691962398, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 10376.676671213063, '1': 354.26671814045403, '2': 108.88307725841878, '3': 668.8031296710833}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 35233, 'flush_seconds': 323.0857892796048, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,561 patches/s**; new independent GMP audits: 1,954.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
