# Boole combined search

Updated: 2026-11-09T22:12:28.832711+00:00

State: **failed**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,470,403,072**.
New replicated logical patches: **107,101,696** in 418,366 chunks.
Combined verified selected patches, including parents: **470,403,072**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3470403072]`.
Local cursor: 3,470,403,072; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 739.9267767822021, 'elapsed_seconds': 5857.314621092984, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482168, 'mean_ready_depth': 0.9495807944069328, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 418366, 'prepare_wall_seconds': 5855.732300019998, 'producer_wait_capacity_seconds': 0.26395443186629564, 'producer_wait_full_seconds': 1062.1845962679363, 'ready': 0, 'ready_depth_seconds': {'0': 3315.413802379975, '1': 891.8949593784055, '2': 279.91905526345363, '3': 1370.0868003611686}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 52391, 'flush_seconds': 294.37893036945025, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,279 patches/s**; new independent GMP audits: 3,269.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: ["Busy('/mnt/nfs_share/fifth42-shared-20261107/reservations.jsonl')"].

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
