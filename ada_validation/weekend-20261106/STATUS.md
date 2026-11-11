# Ada combined search

Updated: 2026-11-11T18:24:00.696641+00:00

State: **running**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **6,995,758,464**.
New replicated logical patches: **72,036,352** in 281,392 chunks.
Combined verified selected patches, including parents: **3,245,758,464**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 6995758464]`.
Local cursor: 6,996,237,696; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 833.5941368028289, 'elapsed_seconds': 4528.75321777002, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681850, 'mean_ready_depth': 0.4526697483010052, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 17674, 'prepare_wall_seconds': 4527.474157690129, 'producer_wait_capacity_seconds': 0.017299005470704287, 'producer_wait_full_seconds': 1414.2456378122442, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2478.723635258677, '1': 2050.029579205322}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 35344, 'flush_seconds': 224.88187889329856, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **15,983 patches/s**; new independent GMP audits: 2,210.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
