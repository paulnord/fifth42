# Ada combined search

Updated: 2026-11-10T08:21:48.185258+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,164,796,032**.
New replicated logical patches: **533,495,808** in 2,083,968 chunks.
Combined verified selected patches, including parents: **1,414,796,032**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5164796032]`.
Local cursor: 5,165,052,032; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 10907.128024734033, 'elapsed_seconds': 28033.448372674, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5930513560126001, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2084922, 'prepare_wall_seconds': 28020.22866782936, 'producer_wait_capacity_seconds': 1.3228361268993467, 'producer_wait_full_seconds': 4207.707696212048, 'ready': 2, 'ready_depth_seconds': {'0': 20737.741952575336, '1': 2459.9074814956402, '2': 342.0297237151535, '3': 4493.769214065862}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 260615, 'flush_seconds': 1475.6617130428203, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,039 patches/s**; new independent GMP audits: 16,289.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
