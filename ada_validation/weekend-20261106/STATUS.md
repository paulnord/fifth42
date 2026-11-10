# Ada combined search

Updated: 2026-11-10T12:22:28.454756+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,422,473,344**.
New replicated logical patches: **791,173,120** in 3,090,520 chunks.
Combined verified selected patches, including parents: **1,672,473,344**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5422473344]`.
Local cursor: 5,423,644,800; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 15529.133772331988, 'elapsed_seconds': 42470.26949899102, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6569224783949846, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3094806, 'prepare_wall_seconds': 42450.65287932096, 'producer_wait_capacity_seconds': 1.965571339474991, 'producer_wait_full_seconds': 6888.654077251849, 'ready': 0, 'ready_depth_seconds': {'0': 29981.075037915725, '1': 4411.851492098649, '2': 744.2056997255422, '3': 7333.137268610124}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 386850, 'flush_seconds': 3034.6328204393503, 'pending_bytes': 110504, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,655 patches/s**; new independent GMP audits: 24,179.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
