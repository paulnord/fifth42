# Boole combined search

Updated: 2026-11-09T20:49:57.625963+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,379,291,136**.
New replicated logical patches: **15,989,760** in 62,460 chunks.
Combined verified selected patches, including parents: **379,291,136**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3379291136]`.
Local cursor: 3,380,566,528; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 119.94685835472774, 'elapsed_seconds': 929.8560969060054, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481767, 'mean_ready_depth': 0.9218420935834943, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 67433, 'prepare_wall_seconds': 929.6079661070835, 'producer_wait_capacity_seconds': 0.04266418912447989, 'producer_wait_full_seconds': 159.35268145240843, 'ready': 0, 'ready_depth_seconds': {'0': 533.0719165353221, '1': 144.32161230791826, '2': 44.528822123014834, '3': 207.93374484975357}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 8436, 'flush_seconds': 46.229967396880966, 'pending_bytes': 127516, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,525 patches/s**; new independent GMP audits: 527.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
