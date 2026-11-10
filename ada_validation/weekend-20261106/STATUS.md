# Ada combined search

Updated: 2026-11-10T16:08:16.222706+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,658,227,072**.
New replicated logical patches: **1,026,926,848** in 4,011,433 chunks.
Combined verified selected patches, including parents: **1,908,227,072**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5658227072]`.
Local cursor: 5,659,427,200; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 20362.9208939104, 'elapsed_seconds': 56012.604269556, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6833191661157109, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4015481, 'prepare_wall_seconds': 55987.120031641156, 'producer_wait_capacity_seconds': 2.5523584671900608, 'producer_wait_full_seconds': 9697.63471587724, 'ready': 0, 'ready_depth_seconds': {'0': 39230.92882887117, '1': 5569.202355942049, '2': 932.1355661420966, '3': 10280.337517738692}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 501973, 'flush_seconds': 3836.081740143243, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,352 patches/s**; new independent GMP audits: 31,371.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
