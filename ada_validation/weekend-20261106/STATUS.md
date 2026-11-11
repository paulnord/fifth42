# Ada combined search

Updated: 2026-11-11T16:48:07.136006+00:00

State: **stopped**. Run **ada-preparation-rotation-02-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,923,722,112**.
New replicated logical patches: **41,025,536** in 160,256 chunks.
Combined verified selected patches, including parents: **3,173,722,112**.
Fresh interval: `[6882696576, 7000000000]`; replicated: `[6882696576, 6923722112]`.
Local cursor: 6,923,722,112; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 473.3966847777483, 'elapsed_seconds': 2534.6719546010136, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7690463, 'mean_ready_depth': 0.4445247630466953, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10016, 'prepare_wall_seconds': 2534.1190343978233, 'producer_wait_capacity_seconds': 0.00970585021423176, 'producer_wait_full_seconds': 768.1183831030503, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1407.9475006939028, '1': 1126.7244500201195}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 20032, 'flush_seconds': 125.99418979836628, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,186 patches/s**; new independent GMP audits: 1,252.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
