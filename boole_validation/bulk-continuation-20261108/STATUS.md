# Boole combined search

Updated: 2026-11-09T21:05:06.249004+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,396,702,464**.
New replicated logical patches: **33,401,088** in 130,473 chunks.
Combined verified selected patches, including parents: **396,702,464**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3396702464]`.
Local cursor: 3,397,085,440; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 233.10311068675946, 'elapsed_seconds': 1829.0575995389954, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481824, 'mean_ready_depth': 0.942949626935717, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 131193, 'prepare_wall_seconds': 1828.5839195344015, 'producer_wait_capacity_seconds': 0.08305607526563108, 'producer_wait_full_seconds': 329.0159343536361, 'ready': 0, 'ready_depth_seconds': {'0': 1039.0496736124041, '1': 279.8486765475245, '2': 85.61724064557347, '3': 424.5420077635208}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 16423, 'flush_seconds': 90.94425909116399, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,343 patches/s**; new independent GMP audits: 1,025.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
