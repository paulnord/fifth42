# Cabbage combined search

Updated: 2026-11-10T10:58:43.833717+00:00

State: **stopped**. Run **cabbage-extended-next-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **1,004,282,880**.
New replicated logical patches: **504,282,880** in 1,969,855 chunks.
Combined verified selected patches, including parents: **504,282,880**.
Fresh interval: `[500000000, 2250000000]`; replicated: `[500000000, 1004282880]`.
Local cursor: 1,005,835,776; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 9246.335757091409, 'elapsed_seconds': 22733.203068403993, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 514657, 'mean_ready_depth': 0.1386895781190545, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1975922, 'prepare_wall_seconds': 22726.26089287596, 'producer_wait_capacity_seconds': 1.2176504145609215, 'producer_wait_full_seconds': 397.2103539039381, 'ready': 0, 'ready_depth_seconds': {'0': 20486.604905241693, '1': 1768.6971635934897, '2': 49.54180706408806, '3': 428.35918837669306}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 247149, 'flush_seconds': 1339.1316923821578, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,242 patches/s**; new independent GMP audits: 15,437.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
