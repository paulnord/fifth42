# Ada combined search

Updated: 2026-11-11T09:41:04.668300+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,742,510,464**.
New replicated logical patches: **855,175,168** in 3,340,528 chunks.
Combined verified selected patches, including parents: **2,992,510,464**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6742510464]`.
Local cursor: 6,742,809,472; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10622.637160428392, 'elapsed_seconds': 48163.413649616996, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3767451116710233, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 208842, 'prepare_wall_seconds': 48156.86658068455, 'producer_wait_capacity_seconds': 0.20704614993883297, 'producer_wait_full_seconds': 10686.501459716179, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 30018.082992779324, '1': 18145.330653882644}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 417680, 'flush_seconds': 2714.4835675462964, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,761 patches/s**; new independent GMP audits: 26,106.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
