# Ada combined search

Updated: 2026-11-10T11:52:24.788019+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,391,446,144**.
New replicated logical patches: **760,145,920** in 2,969,320 chunks.
Combined verified selected patches, including parents: **1,641,446,144**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5391446144]`.
Local cursor: 5,391,904,896; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14989.659617911326, 'elapsed_seconds': 40662.94649429503, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6488799958969277, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2970578, 'prepare_wall_seconds': 40644.1173709422, 'producer_wait_capacity_seconds': 1.8867162081878632, 'producer_wait_full_seconds': 6533.79286348098, 'ready': 2, 'ready_depth_seconds': {'0': 28878.943161567207, '1': 4140.811491407454, '2': 685.0144574173028, '3': 6958.17738271103}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 371322, 'flush_seconds': 2809.0348843054962, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,702 patches/s**; new independent GMP audits: 23,208.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
