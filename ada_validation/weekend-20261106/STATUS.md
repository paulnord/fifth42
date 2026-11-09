# Ada combined search

Updated: 2026-11-09T21:41:41.068035+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,471,334,272**.
New replicated logical patches: **37,060,608** in 144,768 chunks.
Combined verified selected patches, including parents: **721,334,272**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4471334272]`.
Local cursor: 4,471,496,064; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 742.4346383099328, 'elapsed_seconds': 1844.5439087459818, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.4929002102045692, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 144644, 'prepare_wall_seconds': 1843.8543074447662, 'producer_wait_capacity_seconds': 0.08410268899751827, 'producer_wait_full_seconds': 212.92191445681965, 'ready': 3, 'ready_depth_seconds': {'0': 1422.2594631445827, '1': 167.70649153221166, '2': 22.26427071436774, '3': 232.313682463835}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 18080, 'flush_seconds': 99.62684149498818, 'pending_bytes': 18405, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,686 patches/s**; new independent GMP audits: 1,131.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
