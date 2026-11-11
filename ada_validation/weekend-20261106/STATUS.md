# Ada combined search

Updated: 2026-11-11T09:56:08.237890+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,756,475,776**.
New replicated logical patches: **869,140,480** in 3,395,080 chunks.
Combined verified selected patches, including parents: **3,006,475,776**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6756475776]`.
Local cursor: 6,757,583,744; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10802.153128202073, 'elapsed_seconds': 49070.87740151398, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3775299322932631, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 212464, 'prepare_wall_seconds': 49064.89677564276, 'producer_wait_capacity_seconds': 0.21064933837624267, 'producer_wait_full_seconds': 10935.511392521032, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 30545.152377346414, '1': 18525.725022964587}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 424926, 'flush_seconds': 2760.7137992666685, 'pending_bytes': 73671, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,735 patches/s**; new independent GMP audits: 26,558.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
