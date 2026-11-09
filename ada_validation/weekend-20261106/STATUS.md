# Ada combined search

Updated: 2026-11-09T22:56:52.610126+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,561,053,056**.
New replicated logical patches: **126,779,392** in 495,232 chunks.
Combined verified selected patches, including parents: **811,053,056**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4561053056]`.
Local cursor: 4,561,454,464; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2546.0044748556684, 'elapsed_seconds': 6356.443060248974, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.5028891328554758, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 496075, 'prepare_wall_seconds': 6354.7666311131325, 'producer_wait_capacity_seconds': 0.2886901873280294, 'producer_wait_full_seconds': 755.3244058492128, 'ready': 0, 'ready_depth_seconds': {'0': 4881.0669999149395, '1': 575.9672568485257, '2': 77.60752625524765, '3': 821.801276418264}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 62009, 'flush_seconds': 344.797740982438, 'pending_bytes': 55226, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,865 patches/s**; new independent GMP audits: 3,876.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
