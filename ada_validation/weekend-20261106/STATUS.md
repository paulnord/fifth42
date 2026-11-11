# Ada combined search

Updated: 2026-11-11T15:50:24.150918+00:00

State: **running**. Run **ada-preparation-rotation-01-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,871,424,128**.
New replicated logical patches: **28,770,304** in 112,384 chunks.
Combined verified selected patches, including parents: **3,121,424,128**.
Fresh interval: `[6842653824, 7000000000]`; replicated: `[6842653824, 6871424128]`.
Local cursor: 6,872,413,312; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 347.533392211888, 'elapsed_seconds': 1821.1112760090036, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680500, 'mean_ready_depth': 0.43865599453146337, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7250, 'prepare_wall_seconds': 1820.1641896012588, 'producer_wait_capacity_seconds': 0.0067829746985808015, 'producer_wait_full_seconds': 542.3080164734856, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1022.2698954538209, '1': 798.8413779301918}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 14496, 'flush_seconds': 91.81420942541445, 'pending_bytes': 18426, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,302 patches/s**; new independent GMP audits: 907.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
