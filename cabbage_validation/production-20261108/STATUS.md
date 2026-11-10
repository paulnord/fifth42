# Cabbage combined search

Updated: 2026-11-10T04:02:15.715426+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,957,752,448**.
New replicated logical patches: **385,259,520** in 1,504,920 chunks.
Combined verified selected patches, including parents: **707,752,448**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2957752448]`.
Local cursor: 2,958,821,504; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 5247.135544042627, 'elapsed_seconds': 16966.516643362993, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482297, 'mean_ready_depth': 0.3430346419942168, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1508484, 'prepare_wall_seconds': 16961.20181469369, 'producer_wait_capacity_seconds': 0.9759041058714502, 'producer_wait_full_seconds': 723.0754311294295, 'ready': 3, 'ready_depth_seconds': {'0': 13430.146271182515, '1': 2232.870097838226, '2': 323.2679551540059, '3': 980.2323181662359}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 188660, 'flush_seconds': 1101.5600911662914, 'pending_bytes': 18217, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **22,758 patches/s**; new independent GMP audits: 11,786.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
