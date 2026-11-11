# Ada combined search

Updated: 2026-11-11T06:10:30.113072+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,530,591,616**.
New replicated logical patches: **643,256,320** in 2,512,720 chunks.
Combined verified selected patches, including parents: **2,780,591,616**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6530591616]`.
Local cursor: 6,531,906,432; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 8060.961822311045, 'elapsed_seconds': 35532.02242489497, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.36529666154851953, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 157362, 'prepare_wall_seconds': 35527.03852425213, 'producer_wait_capacity_seconds': 0.15604207874275744, 'producer_wait_full_seconds': 7400.357262199337, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 22552.29325125675, '1': 12979.729169881262}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 314720, 'flush_seconds': 2047.5807282714522, 'pending_bytes': 18418, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,140 patches/s**; new independent GMP audits: 19,671.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
