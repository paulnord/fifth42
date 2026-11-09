# Ada combined search

Updated: 2026-11-09T20:24:29.228449+00:00

State: **running**. Run **ada-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,410,408,320**.
New replicated logical patches: **11,565,056** in 45,176 chunks.
Combined verified selected patches, including parents: **660,408,320**.
Fresh interval: `[4398843264, 11250000001]`; replicated: `[4398843264, 4410408320]`.
Local cursor: 4,411,209,088; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 672.364328542084, 'elapsed_seconds': 1002.2708326250431, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 963958, 'mean_ready_depth': 0.08461966535252005, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 48133, 'prepare_wall_seconds': 1002.080862173927, 'producer_wait_capacity_seconds': 0.028397765243425965, 'producer_wait_full_seconds': 1.2123115896829404, 'ready': 0, 'ready_depth_seconds': {'0': 950.4928682408645, '1': 29.827652823296376, '2': 10.866762950492557, '3': 11.0835479083471}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 6016, 'flush_seconds': 32.343262536567636, 'pending_bytes': 173781, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **11,857 patches/s**; new independent GMP audits: 377.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
