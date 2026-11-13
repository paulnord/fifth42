# Boole combined search

Updated: 2026-11-13T01:11:29.318214+00:00

State: **running**. Run **boole-shared-deadline-r1-32-overnight-20261112**; gpu with 16 preparation workers.
Verified replicated cursor: **9,080,471,296**.
New replicated logical patches: **32,471,296** in 126,841 chunks.
Combined verified selected patches, including parents: **32,471,296**.
Fresh interval: `[9048000000, 9112000000]`; replicated: `[9048000000, 9080471296]`.
Local cursor: 9,080,602,368; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.15949752286542207, 'elapsed_seconds': 4632.699333047029, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683087, 'mean_ready_depth': 0.9994189506820156, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 7946, 'prepare_wall_seconds': 4630.09302761103, 'producer_wait_capacity_seconds': 0.010008915094658732, 'producer_wait_full_seconds': 3222.9647242543288, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 2.691824997891672, '1': 4630.007506259135}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 15916, 'flush_seconds': 123.60685111349449, 'pending_bytes': 19844, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,023 patches/s**; new independent GMP audits: 994.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
