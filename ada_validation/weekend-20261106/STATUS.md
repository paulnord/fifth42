# Ada combined search

Updated: 2026-11-11T17:53:53.499678+00:00

State: **running**. Run **ada-allocated-r3-00-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **6,967,303,552**.
New replicated logical patches: **43,581,440** in 170,240 chunks.
Combined verified selected patches, including parents: **3,217,303,552**.
Fresh interval: `[6923722112, 7000000000]`; replicated: `[6923722112, 6967303552]`.
Local cursor: 6,967,496,064; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 504.3096021299716, 'elapsed_seconds': 2726.281956050021, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7680760, 'mean_ready_depth': 0.45130306353583693, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 10674, 'prepare_wall_seconds': 2725.246400588425, 'producer_wait_capacity_seconds': 0.010435054951813072, 'producer_wait_full_seconds': 845.9321440230124, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1495.9025532751693, '1': 1230.3793988278485}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 21344, 'flush_seconds': 135.32574987056432, 'pending_bytes': 18415, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **16,034 patches/s**; new independent GMP audits: 1,335.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
