# Ada combined search

Updated: 2026-11-10T11:07:17.882980+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,342,771,328**.
New replicated logical patches: **711,471,104** in 2,779,184 chunks.
Combined verified selected patches, including parents: **1,592,771,328**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5342771328]`.
Local cursor: 5,343,983,744; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14094.276436882908, 'elapsed_seconds': 37959.742305347, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6397281237952755, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2783638, 'prepare_wall_seconds': 37942.09628515743, 'producer_wait_capacity_seconds': 1.767672952846624, 'producer_wait_full_seconds': 6015.865928300947, 'ready': 0, 'ready_depth_seconds': {'0': 27117.94927863829, '1': 3810.9179379083216, '2': 619.6284776618122, '3': 6411.246610506612}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 347954, 'flush_seconds': 2549.6438370344695, 'pending_bytes': 110493, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,773 patches/s**; new independent GMP audits: 21,748.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
