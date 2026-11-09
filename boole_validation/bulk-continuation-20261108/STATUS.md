# Boole combined search

Updated: 2026-11-09T21:50:15.592140+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,445,331,456**.
New replicated logical patches: **82,030,080** in 320,430 chunks.
Combined verified selected patches, including parents: **445,331,456**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3445331456]`.
Local cursor: 3,446,666,752; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 578.8366986231995, 'elapsed_seconds': 4547.284765273973, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482168, 'mean_ready_depth': 0.9449810370440584, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 325649, 'prepare_wall_seconds': 4545.756176958559, 'producer_wait_capacity_seconds': 0.2054687826312147, 'producer_wait_full_seconds': 817.9730017604888, 'ready': 3, 'ready_depth_seconds': {'0': 2584.435817620717, '1': 688.0216880847584, '2': 215.40559083712287, '3': 1059.4216678214143}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 40774, 'flush_seconds': 226.61573982558912, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,325 patches/s**; new independent GMP audits: 2,545.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
