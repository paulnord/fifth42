# Cabbage combined search

Updated: 2026-11-09T20:35:04.590528+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,371,830,656**.
New replicated logical patches: **4,488,960** in 17,535 chunks.
Combined verified selected patches, including parents: **121,830,656**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2371830656]`.
Local cursor: 2,372,890,752; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 78.44730740977684, 'elapsed_seconds': 237.08025110897142, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482045, 'mean_ready_depth': 0.2832525542021718, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 21563, 'prepare_wall_seconds': 236.99565343378345, 'producer_wait_capacity_seconds': 0.013564917666371912, 'producer_wait_full_seconds': 6.086210708483122, 'ready': 0, 'ready_depth_seconds': {'0': 192.5744147261721, '1': 31.11665387492394, '2': 4.130612498091068, '3': 9.258569268800784}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 2695, 'flush_seconds': 14.937891638604924, 'pending_bytes': 127549, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,969 patches/s**; new independent GMP audits: 169.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
