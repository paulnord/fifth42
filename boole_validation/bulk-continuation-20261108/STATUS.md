# Boole combined search

Updated: 2026-11-09T21:20:08.360286+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,412,925,952**.
New replicated logical patches: **49,624,576** in 193,846 chunks.
Combined verified selected patches, including parents: **412,925,952**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3412925952]`.
Local cursor: 3,413,643,776; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 348.65515629947186, 'elapsed_seconds': 2732.3325437179883, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482168, 'mean_ready_depth': 0.9417013673876452, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 195965, 'prepare_wall_seconds': 2731.633225168509, 'producer_wait_capacity_seconds': 0.12377920956350863, 'producer_wait_full_seconds': 490.7337497440749, 'ready': 1, 'ready_depth_seconds': {'0': 1555.9170582789811, '1': 414.10309378936654, '2': 127.99897424131632, '3': 634.3134167683311}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 24532, 'flush_seconds': 135.64011641516117, 'pending_bytes': 36437, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,347 patches/s**; new independent GMP audits: 1,531.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
