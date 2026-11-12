# Boole combined search

Updated: 2026-11-12T10:12:54.859831+00:00

State: **running**. Run **boole-range-r3-20261111-25-recovery1**; gpu with 16 preparation workers.
Verified replicated cursor: **8,644,089,344**.
New replicated logical patches: **44,089,344** in 172,224 chunks.
Combined verified selected patches, including parents: **44,089,344**.
Fresh interval: `[8600000000, 8664000000]`; replicated: `[8600000000, 8644089344]`.
Local cursor: 8,644,529,920; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.1734532875707373, 'elapsed_seconds': 5415.1115022999, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681333, 'mean_ready_depth': 0.9993177826663818, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10866, 'prepare_wall_seconds': 5413.008853930165, 'producer_wait_capacity_seconds': 0.014246014878153801, 'producer_wait_full_seconds': 3486.9266792861745, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3.694281250354834, '1': 5411.417219369556}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 21777, 'flush_seconds': 169.0198769083945, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,217 patches/s**; new independent GMP audits: 1,359.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
