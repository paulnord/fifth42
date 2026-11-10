# Ada combined search

Updated: 2026-11-10T16:53:26.502980+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,705,480,576**.
New replicated logical patches: **1,074,180,352** in 4,196,017 chunks.
Combined verified selected patches, including parents: **1,955,480,576**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5705480576]`.
Local cursor: 5,705,762,944; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 21340.329685168806, 'elapsed_seconds': 58730.890748554026, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6881923416746196, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4197024, 'prepare_wall_seconds': 58704.2461975147, 'producer_wait_capacity_seconds': 2.6680098934448324, 'producer_wait_full_seconds': 10295.707629894314, 'ready': 0, 'ready_depth_seconds': {'0': 41087.46685806697, '1': 5774.213826247666, '2': 963.6947833762388, '3': 10905.515279961168}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 524682, 'flush_seconds': 3970.6829854696407, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,294 patches/s**; new independent GMP audits: 32,790.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
