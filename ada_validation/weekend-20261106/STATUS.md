# Ada combined search

Updated: 2026-11-10T07:21:39.687930+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,097,687,168**.
New replicated logical patches: **466,386,944** in 1,821,824 chunks.
Combined verified selected patches, including parents: **1,347,687,168**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5097687168]`.
Local cursor: 5,098,383,488; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 9555.697659200465, 'elapsed_seconds': 24418.33768279804, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5838889183124024, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1824004, 'prepare_wall_seconds': 24406.480085282587, 'producer_wait_capacity_seconds': 1.156861566589214, 'producer_wait_full_seconds': 3597.621530858625, 'ready': 3, 'ready_depth_seconds': {'0': 18147.017519998306, '1': 2132.3482692011166, '2': 291.6671706350171, '3': 3847.30472204159}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 228000, 'flush_seconds': 1263.792483913363, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,123 patches/s**; new independent GMP audits: 14,251.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
