# Boole combined search

Updated: 2026-11-10T00:16:05.910553+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,529,010,176**.
New replicated logical patches: **58,607,104** in 228,934 chunks.
Combined verified selected patches, including parents: **529,010,176**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3529010176]`.
Local cursor: 3,529,718,016; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 398.6272422830807, 'elapsed_seconds': 3256.5416853040224, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9675697576374521, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 231592, 'prepare_wall_seconds': 3255.727985393023, 'producer_wait_capacity_seconds': 0.1455010527279228, 'producer_wait_full_seconds': 602.4425766879576, 'ready': 0, 'ready_depth_seconds': {'0': 1813.1773559180438, '1': 511.0754829940852, '2': 157.01077079377137, '3': 775.2780748680816}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 28991, 'flush_seconds': 167.2215414706152, 'pending_bytes': 91111, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,198 patches/s**; new independent GMP audits: 1,810.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
