# Ada combined search

Updated: 2026-11-10T06:36:29.808406+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,047,107,712**.
New replicated logical patches: **415,807,488** in 1,624,248 chunks.
Combined verified selected patches, including parents: **1,297,107,712**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5047107712]`.
Local cursor: 5,047,857,280; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 8513.804884292418, 'elapsed_seconds': 21707.80034230504, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5784058276451672, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1626614, 'prepare_wall_seconds': 21697.483849437966, 'producer_wait_capacity_seconds': 1.0314953493070789, 'producer_wait_full_seconds': 3154.659637438017, 'ready': 0, 'ready_depth_seconds': {'0': 16165.546413384378, '1': 1905.4284091658192, '2': 259.98674256022787, '3': 3376.838776353572}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 203326, 'flush_seconds': 1126.574424446153, 'pending_bytes': 110504, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,183 patches/s**; new independent GMP audits: 12,708.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
