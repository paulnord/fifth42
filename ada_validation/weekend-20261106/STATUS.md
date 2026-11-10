# Ada combined search

Updated: 2026-11-10T03:05:43.544402+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,806,664,320**.
New replicated logical patches: **175,364,096** in 685,016 chunks.
Combined verified selected patches, including parents: **1,056,664,320**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4806664320]`.
Local cursor: 4,807,721,088; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 3603.7692529144115, 'elapsed_seconds': 9066.383449366025, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5517453130929948, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 688900, 'prepare_wall_seconds': 9061.759903345956, 'producer_wait_capacity_seconds': 0.4365339604555629, 'producer_wait_full_seconds': 1230.143552547379, 'ready': 3, 'ready_depth_seconds': {'0': 6820.99531105347, '1': 812.4785964901675, '2': 108.87264454277465, '3': 1324.036896438629}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 86112, 'flush_seconds': 474.62291486677714, 'pending_bytes': 18415, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,452 patches/s**; new independent GMP audits: 5,383.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
