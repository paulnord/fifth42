# Boole combined search

Updated: 2026-11-09T23:46:05.429030+00:00

State: **running**. Run **boole-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,495,520,768**.
New replicated logical patches: **25,117,696** in 98,116 chunks.
Combined verified selected patches, including parents: **495,520,768**.
Fresh interval: `[3470403072, 3750000000]`; replicated: `[3470403072, 3495520768]`.
Local cursor: 3,496,941,312; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 178.64043081278214, 'elapsed_seconds': 1453.390034142998, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482160, 'mean_ready_depth': 0.9660385754665615, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 103429, 'prepare_wall_seconds': 1444.3445888053393, 'producer_wait_capacity_seconds': 0.06496450619306415, 'producer_wait_full_seconds': 260.2100254203542, 'ready': 3, 'ready_depth_seconds': {'0': 809.9968821296934, '1': 228.2427542451187, '2': 69.66310567891924, '3': 345.4872908592806}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 12946, 'flush_seconds': 74.2725366296363, 'pending_bytes': 18219, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,201 patches/s**; new independent GMP audits: 809.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
