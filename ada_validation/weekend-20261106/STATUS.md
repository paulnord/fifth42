# Ada combined search

Updated: 2026-11-10T01:20:25.616449+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,684,646,528**.
New replicated logical patches: **53,346,304** in 208,384 chunks.
Combined verified selected patches, including parents: **934,646,528**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4684646528]`.
Local cursor: 4,684,920,960; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1115.376441357599, 'elapsed_seconds': 2745.942083013011, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482217, 'mean_ready_depth': 0.5344225707372129, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 209028, 'prepare_wall_seconds': 2744.3674779013963, 'producer_wait_capacity_seconds': 0.1325920817325823, 'producer_wait_full_seconds': 357.10926568473224, 'ready': 3, 'ready_depth_seconds': {'0': 2082.521412640519, '1': 244.96364699781407, '2': 32.841287076473236, '3': 385.6157353161834}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 26128, 'flush_seconds': 142.72585173306288, 'pending_bytes': 18410, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,487 patches/s**; new independent GMP audits: 1,634.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
