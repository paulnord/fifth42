# Ada combined search

Updated: 2026-11-10T02:05:30.361275+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,737,386,624**.
New replicated logical patches: **106,086,400** in 414,400 chunks.
Combined verified selected patches, including parents: **987,386,624**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4737386624]`.
Local cursor: 4,737,771,648; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2182.0646613608696, 'elapsed_seconds': 5447.414502486994, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5432240998033736, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 415236, 'prepare_wall_seconds': 5444.5262076313375, 'producer_wait_capacity_seconds': 0.2631976859411225, 'producer_wait_full_seconds': 723.3601479482604, 'ready': 3, 'ready_depth_seconds': {'0': 4113.698878034367, '1': 488.21293312101625, '2': 65.55416456051171, '3': 779.9485257091001}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 51904, 'flush_seconds': 284.850167989498, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,514 patches/s**; new independent GMP audits: 3,245.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
