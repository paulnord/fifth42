# Boole combined search

Updated: 2026-11-10T05:00:41.670298+00:00

State: **running**. Run **boole-extra-20261109-a**; gpu with 16 preparation workers.
Verified replicated cursor: **180,648,192**.
New replicated logical patches: **80,648,192** in 315,032 chunks.
Combined verified selected patches, including parents: **80,648,192**.
Fresh interval: `[100000000, 300000000]`; replicated: `[100000000, 180648192]`.
Local cursor: 181,886,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1041.07308232598, 'elapsed_seconds': 4503.005178230989, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 546826, 'mean_ready_depth': 0.5390302985939847, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 319106, 'prepare_wall_seconds': 4501.911537566979, 'producer_wait_capacity_seconds': 0.19441313279094175, 'producer_wait_full_seconds': 550.208358224947, 'ready': 1, 'ready_depth_seconds': {'0': 3430.206054938084, '1': 355.8994600304868, '2': 79.34222189558204, '3': 637.5574406568194}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 39951, 'flush_seconds': 218.3791525788838, 'pending_bytes': 85576, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,138 patches/s**; new independent GMP audits: 2,494.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
