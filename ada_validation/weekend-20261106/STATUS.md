# Ada combined search

Updated: 2026-11-11T15:20:16.881728+00:00

State: **running**. Run **ada-preparation-rotation-01-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,842,655,872**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **3,092,655,872**.
Fresh interval: `[6842653824, 7000000000]`; replicated: `[6842653824, 6842655872]`.
Local cursor: 6,842,946,688; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2.1140318600228056, 'elapsed_seconds': 10.001552161003929, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7676781, 'mean_ready_depth': 0.4344505835684904, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 40, 'prepare_wall_seconds': 9.959488196007442, 'producer_wait_capacity_seconds': 4.292087396606803e-05, 'producer_wait_full_seconds': 2.976513379777316, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 5.656370345095638, '1': 4.3451801729388535}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 78, 'flush_seconds': 0.46418575721327215, 'pending_bytes': 128947, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **15,969 patches/s**; new independent GMP audits: 5.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
