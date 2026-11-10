# Ada combined search

Updated: 2026-11-10T19:54:12.879660+00:00

State: **stopped**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,882,704,256**.
New replicated logical patches: **1,251,404,032** in 4,888,297 chunks.
Combined verified selected patches, including parents: **2,132,704,256**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5882704256]`.
Local cursor: 5,887,335,296; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 25202.41449142364, 'elapsed_seconds': 69547.28014549904, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.7086410454084222, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4906388, 'prepare_wall_seconds': 69515.9207708601, 'producer_wait_capacity_seconds': 3.1212420675437897, 'producer_wait_full_seconds': 12797.628974375257, 'ready': 0, 'ready_depth_seconds': {'0': 48378.46911818057, '1': 6567.286663050589, '2': 1087.8024384973687, '3': 13513.721922524506}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 613417, 'flush_seconds': 4504.228715883335, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,060 patches/s**; new independent GMP audits: 38,332.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
