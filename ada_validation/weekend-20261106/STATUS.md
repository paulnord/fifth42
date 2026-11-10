# Ada combined search

Updated: 2026-11-10T04:36:08.393712+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,910,219,392**.
New replicated logical patches: **278,919,168** in 1,089,528 chunks.
Combined verified selected patches, including parents: **1,160,219,392**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4910219392]`.
Local cursor: 4,911,544,448; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5721.783628432429, 'elapsed_seconds': 14491.851245785016, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5632060319100617, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1094532, 'prepare_wall_seconds': 14484.633015093452, 'producer_wait_capacity_seconds': 0.6937412939732894, 'producer_wait_full_seconds': 2026.59399514104, 'ready': 3, 'ready_depth_seconds': {'0': 10855.569807269669, '1': 1286.529732148687, '2': 173.88681247323984, '3': 2175.864892691432}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 136816, 'flush_seconds': 756.8597989638802, 'pending_bytes': 18421, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,335 patches/s**; new independent GMP audits: 8,552.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
