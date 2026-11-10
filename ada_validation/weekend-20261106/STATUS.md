# Ada combined search

Updated: 2026-11-10T09:37:02.243522+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,246,355,584**.
New replicated logical patches: **615,055,360** in 2,402,560 chunks.
Combined verified selected patches, including parents: **1,496,355,584**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5246355584]`.
Local cursor: 5,247,201,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 12439.988658579881, 'elapsed_seconds': 32545.112316732004, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6120764062834817, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2405638, 'prepare_wall_seconds': 32529.86354944296, 'producer_wait_capacity_seconds': 1.5267888344242238, 'producer_wait_full_seconds': 5006.082841868629, 'ready': 3, 'ready_depth_seconds': {'0': 23752.569416033104, '1': 3005.609163261135, '2': 446.31498452380765, '3': 5340.61875220295}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 300704, 'flush_seconds': 1889.6314910540823, 'pending_bytes': 55238, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,923 patches/s**; new independent GMP audits: 18,795.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
