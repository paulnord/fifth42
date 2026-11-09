# Ada combined search

Updated: 2026-11-09T20:39:32.560244+00:00

State: **running**. Run **ada-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,421,929,088**.
New replicated logical patches: **23,085,824** in 90,179 chunks.
Combined verified selected patches, including parents: **671,929,088**.
Fresh interval: `[4398843264, 11250000001]`; replicated: `[4398843264, 4421929088]`.
Local cursor: 4,422,246,528; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1274.8535081161535, 'elapsed_seconds': 1903.666400991031, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 963958, 'mean_ready_depth': 0.08642821281262565, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 91150, 'prepare_wall_seconds': 1903.3551499507157, 'producer_wait_capacity_seconds': 0.05353349761571735, 'producer_wait_full_seconds': 2.768485792563297, 'ready': 0, 'ready_depth_seconds': {'0': 1803.3197855352773, '1': 57.755670175363775, '2': 20.998019264487084, '3': 21.592925374920014}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 11394, 'flush_seconds': 64.67113950062776, 'pending_bytes': 104257, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **12,025 patches/s**; new independent GMP audits: 713.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
