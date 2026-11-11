# Cabbage combined search

Updated: 2026-11-11T20:21:56.693383+00:00

State: **running**. Run **cabbage-extended-r3-cap100-job-36-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **9,352,539,904**.
New replicated logical patches: **48,539,904** in 189,609 chunks.
Combined verified selected patches, including parents: **48,539,904**.
Fresh interval: `[9304000000, 9368000000]`; replicated: `[9304000000, 9352539904]`.
Local cursor: 9,352,949,504; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1582.9727504201, 'elapsed_seconds': 4764.05281870201, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 3843670, 'mean_ready_depth': 0.2645515952999172, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 4, 'preparation_batches': 47735, 'prepare_wall_seconds': 4763.847861078917, 'producer_wait_capacity_seconds': 0.03415629704250023, 'producer_wait_full_seconds': 1033.4770258828066, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3503.7150416443474, '1': 1260.337773280684}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 23907, 'flush_seconds': 241.8902630560333, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,260 patches/s**; new independent GMP audits: 1,492.
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
