# Ada combined search

Updated: 2026-11-10T17:08:34.932012+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,720,359,296**.
New replicated logical patches: **1,089,059,072** in 4,254,137 chunks.
Combined verified selected patches, including parents: **1,970,359,296**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5720359296]`.
Local cursor: 5,721,227,648; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 21662.82467107114, 'elapsed_seconds': 59635.82252794702, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6898623049970686, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4257213, 'prepare_wall_seconds': 59608.79498972098, 'producer_wait_capacity_seconds': 2.706349157728255, 'producer_wait_full_seconds': 10497.621559668623, 'ready': 0, 'ready_depth_seconds': {'0': 41702.2589815642, '1': 5843.07548567123, '2': 974.0336764473468, '3': 11116.45438365324}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 532211, 'flush_seconds': 4015.5038907327107, 'pending_bytes': 73675, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,275 patches/s**; new independent GMP audits: 33,260.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
