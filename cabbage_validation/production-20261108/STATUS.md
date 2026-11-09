# Cabbage combined search

Updated: 2026-11-09T21:50:19.783018+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,476,334,464**.
New replicated logical patches: **108,992,768** in 425,753 chunks.
Combined verified selected patches, including parents: **226,334,464**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2476334464]`.
Local cursor: 2,477,052,032; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1510.0527643864625, 'elapsed_seconds': 4747.932277255983, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482508, 'mean_ready_depth': 0.307968913905832, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 428059, 'prepare_wall_seconds': 4746.423892680206, 'producer_wait_capacity_seconds': 0.26989108353154734, 'producer_wait_full_seconds': 150.12816475925501, 'ready': 0, 'ready_depth_seconds': {'0': 3807.8656995842466, '1': 636.1172103068093, '2': 85.74976324359886, '3': 218.19960331032053}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 53540, 'flush_seconds': 302.1342616956681, 'pending_bytes': 127554, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,064 patches/s**; new independent GMP audits: 3,345.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
