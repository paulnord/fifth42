# Ada combined search

Updated: 2026-11-10T17:23:38.387472+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,735,811,456**.
New replicated logical patches: **1,104,511,232** in 4,314,497 chunks.
Combined verified selected patches, including parents: **1,985,811,456**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5735811456]`.
Local cursor: 5,736,530,304; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 21987.402099373343, 'elapsed_seconds': 60541.11448711704, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6915192533294033, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4317113, 'prepare_wall_seconds': 60513.70370466268, 'producer_wait_capacity_seconds': 2.744747205695603, 'producer_wait_full_seconds': 10700.966196304304, 'ready': 0, 'ready_depth_seconds': {'0': 42317.55853975675, '1': 5910.363744297356, '2': 984.5940649489639, '3': 11328.59813722194}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 539705, 'flush_seconds': 4060.17351385043, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,255 patches/s**; new independent GMP audits: 33,728.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
