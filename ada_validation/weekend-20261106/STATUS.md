# Ada combined search

Updated: 2026-11-11T16:05:36.891333+00:00

State: **running**. Run **ada-preparation-rotation-02-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,882,698,624**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **3,132,698,624**.
Fresh interval: `[6882696576, 7000000000]`; replicated: `[6882696576, 6882698624]`.
Local cursor: 6,882,991,488; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1.9380043158889748, 'elapsed_seconds': 10.938657539023552, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7677454, 'mean_ready_depth': 0.46421990083666154, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 42, 'prepare_wall_seconds': 10.218162115081213, 'producer_wait_capacity_seconds': 4.6055938582867384e-05, 'producer_wait_full_seconds': 2.9727236899198033, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 5.860711553948931, '1': 5.077942518051714}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 80, 'flush_seconds': 0.4832431781687774, 'pending_bytes': 18425, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **14,974 patches/s**; new independent GMP audits: 6.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
