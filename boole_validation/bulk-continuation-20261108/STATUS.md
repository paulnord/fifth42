# Boole combined search

Updated: 2026-11-09T20:34:53.221854+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,363,303,424**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **363,303,424**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3363303424]`.
Local cursor: 3,363,840,000; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2.4058531979098916, 'elapsed_seconds': 18.100521217973437, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481324, 'mean_ready_depth': 0.7097950533935423, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1485, 'prepare_wall_seconds': 18.088959067652468, 'producer_wait_capacity_seconds': 0.000940939353313297, 'producer_wait_full_seconds': 1.1823505156789906, 'ready': 1, 'ready_depth_seconds': {'0': 11.089814923936501, '1': 3.4437706440803595, '2': 1.2969137796317227, '3': 2.2700207403395325}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 185, 'flush_seconds': 1.0135213671601377, 'pending_bytes': 72863, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,935 patches/s**; new independent GMP audits: 12.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
