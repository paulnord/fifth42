# Cabbage combined search

Updated: 2026-11-10T01:16:33.216263+00:00

State: **running**. Run **cabbage-extended-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,733,085,056**.
New replicated logical patches: **160,592,128** in 627,313 chunks.
Combined verified selected patches, including parents: **483,085,056**.
Fresh interval: `[2572492928, 3000000000]`; replicated: `[2572492928, 2733085056]`.
Local cursor: 2,734,414,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2183.2507217871025, 'elapsed_seconds': 7022.754210135958, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482186, 'mean_ready_depth': 0.3329987754047646, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 631786, 'prepare_wall_seconds': 7020.552356406988, 'producer_wait_capacity_seconds': 0.40790809562895447, 'producer_wait_full_seconds': 270.27220121765276, 'ready': 1, 'ready_depth_seconds': {'0': 5569.397055213049, '1': 944.275999485224, '2': 132.95091114839306, '3': 376.1302433873061}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 79014, 'flush_seconds': 457.26338597532595, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,024 patches/s**; new independent GMP audits: 4,936.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
