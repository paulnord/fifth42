# Ada combined search

Updated: 2026-11-10T08:36:52.083981+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,181,116,544**.
New replicated logical patches: **549,816,320** in 2,147,720 chunks.
Combined verified selected patches, including parents: **1,431,116,544**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5181116544]`.
Local cursor: 5,181,540,480; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11207.538081265287, 'elapsed_seconds': 28937.572129180015, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5975997505766144, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2149354, 'prepare_wall_seconds': 28923.94503984478, 'producer_wait_capacity_seconds': 1.3637370490469038, 'producer_wait_full_seconds': 4365.555606172129, 'ready': 2, 'ready_depth_seconds': {'0': 21333.001933631196, '1': 2577.649727114942, '2': 365.3252426898107, '3': 4661.595224732067}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 268669, 'flush_seconds': 1566.6840394916944, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,015 patches/s**; new independent GMP audits: 16,792.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
