# Ada combined search

Updated: 2026-11-10T09:06:55.515479+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,213,476,992**.
New replicated logical patches: **582,176,768** in 2,274,128 chunks.
Combined verified selected patches, including parents: **1,463,476,992**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5213476992]`.
Local cursor: 5,214,179,456; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11761.557616955834, 'elapsed_seconds': 30736.933748376032, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6086367722590987, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2276578, 'prepare_wall_seconds': 30722.496796912863, 'producer_wait_capacity_seconds': 1.4445980810560286, 'producer_wait_full_seconds': 4686.004500069888, 'ready': 1, 'ready_depth_seconds': {'0': 22457.749059427646, '1': 2853.2213630802, '2': 423.48319270531647, '3': 5002.480132420838}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 284572, 'flush_seconds': 1793.4647814910277, 'pending_bytes': 18423, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,961 patches/s**; new independent GMP audits: 17,786.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
