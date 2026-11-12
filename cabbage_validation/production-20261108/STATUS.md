# Cabbage combined search

Updated: 2026-11-12T13:29:13.342486+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-46**; gpu with 16 preparation workers.
Verified replicated cursor: **9,969,643,264**.
New replicated logical patches: **25,643,264** in 100,169 chunks.
Combined verified selected patches, including parents: **25,643,264**.
Fresh interval: `[9944000000, 10008000000]`; replicated: `[9944000000, 9969643264]`.
Local cursor: 9,970,042,624; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 375.07860937027726, 'elapsed_seconds': 2727.5183254500153, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15355535, 'mean_ready_depth': 0.42268976291270255, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 6354, 'prepare_wall_seconds': 2726.4918993115425, 'producer_wait_capacity_seconds': 0.005949971149675548, 'producer_wait_full_seconds': 665.1931661304552, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1574.6242101084208, '1': 1152.8940743245184}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 12715, 'flush_seconds': 113.36786739726085, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **9,538 patches/s**; new independent GMP audits: 795.
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
