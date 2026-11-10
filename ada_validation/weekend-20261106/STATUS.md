# Ada combined search

Updated: 2026-11-10T15:53:12.852908+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,643,339,904**.
New replicated logical patches: **1,012,039,680** in 3,953,280 chunks.
Combined verified selected patches, including parents: **1,893,339,904**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5643339904]`.
Local cursor: 5,643,899,264; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 20040.921356620383, 'elapsed_seconds': 55116.732985295996, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6817357722117352, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3955332, 'prepare_wall_seconds': 55091.21733203012, 'producer_wait_capacity_seconds': 2.5137916312087327, 'producer_wait_full_seconds': 9502.544107520662, 'ready': 3, 'ready_depth_seconds': {'0': 38617.59511522652, '1': 5500.221328142798, '2': 921.9224277311005, '3': 10076.994113304594}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 494446, 'flush_seconds': 3791.9685559723293, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,371 patches/s**; new independent GMP audits: 30,902.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
