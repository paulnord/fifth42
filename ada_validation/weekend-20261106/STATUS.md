# Ada combined search

Updated: 2026-11-11T07:40:46.315982+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,622,378,880**.
New replicated logical patches: **735,043,584** in 2,871,264 chunks.
Combined verified selected patches, including parents: **2,872,378,880**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6622378880]`.
Local cursor: 6,623,472,512; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 9179.126096514403, 'elapsed_seconds': 40943.636308329005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.37021824073169207, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 179701, 'prepare_wall_seconds': 40938.52778692462, 'producer_wait_capacity_seconds': 0.17818533931858838, 'producer_wait_full_seconds': 8770.472592574602, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 25785.55530310719, '1': 15158.081003227795}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 359401, 'flush_seconds': 2337.1068133400404, 'pending_bytes': 36835, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,977 patches/s**; new independent GMP audits: 22,463.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
