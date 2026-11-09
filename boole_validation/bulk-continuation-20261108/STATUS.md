# Boole combined search

Updated: 2026-11-09T21:35:15.116621+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,429,077,760**.
New replicated logical patches: **65,776,384** in 256,939 chunks.
Combined verified selected patches, including parents: **429,077,760**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3429077760]`.
Local cursor: 3,430,281,728; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 464.96530928032007, 'elapsed_seconds': 3638.887480158999, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482168, 'mean_ready_depth': 0.9418118060409906, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 260941, 'prepare_wall_seconds': 3637.9588591223583, 'producer_wait_capacity_seconds': 0.1646465954836458, 'producer_wait_full_seconds': 652.6383825588273, 'ready': 0, 'ready_depth_seconds': {'0': 2073.6045030089444, '1': 548.8930338072823, '2': 170.91567206708714, '3': 845.4742705756798}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 32669, 'flush_seconds': 180.0922745988355, 'pending_bytes': 54658, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,348 patches/s**; new independent GMP audits: 2,039.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
