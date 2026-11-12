# Cabbage combined search

Updated: 2026-11-12T22:42:24.850909+00:00

State: **stopping**. Run **cabbage-extended-memory-r2-cap100-20261111-job-50**; gpu with 16 preparation workers.
Verified replicated cursor: **10,263,625,472**.
New replicated logical patches: **63,625,472** in 248,537 chunks.
Combined verified selected patches, including parents: **63,625,472**.
Fresh interval: `[10200000000, 10264000000]`; replicated: `[10200000000, 10263625472]`.
Local cursor: 10,264,000,000; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 793.3726407003123, 'elapsed_seconds': 7227.650437147007, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15356723, 'mean_ready_depth': 0.47105950411350717, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 15625, 'prepare_wall_seconds': 7225.911580273882, 'producer_wait_capacity_seconds': 0.013576931436546147, 'producer_wait_full_seconds': 2107.9235349822557, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 3822.9970026217634, '1': 3404.6534308282426}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 31294, 'flush_seconds': 280.5986521303421, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,854 patches/s**; new independent GMP audits: 1,954.
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
