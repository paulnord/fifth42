# Ada combined search

Updated: 2026-11-10T11:37:20.844078+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,375,101,056**.
New replicated logical patches: **743,800,832** in 2,905,472 chunks.
Combined verified selected patches, including parents: **1,625,101,056**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5375101056]`.
Local cursor: 5,375,887,488; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14700.506396320881, 'elapsed_seconds': 39758.83440358902, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6455516647708013, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2908000, 'prepare_wall_seconds': 39740.39638937451, 'producer_wait_capacity_seconds': 1.8468033846584149, 'producer_wait_full_seconds': 6358.837893055112, 'ready': 0, 'ready_depth_seconds': {'0': 28300.770184305322, '1': 4023.206955288071, '2': 661.3970057453844, '3': 6773.46025726822}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 363500, 'flush_seconds': 2716.0385702197673, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,724 patches/s**; new independent GMP audits: 22,719.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
