# Ada combined search

Updated: 2026-11-11T11:11:18.794059+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,829,634,688**.
New replicated logical patches: **942,299,392** in 3,680,857 chunks.
Combined verified selected patches, including parents: **3,079,634,688**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6829634688]`.
Local cursor: 6,830,232,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 11669.624914846732, 'elapsed_seconds': 53576.420674883004, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.38177871127258295, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 230179, 'prepare_wall_seconds': 53569.923961397784, 'producer_wait_capacity_seconds': 0.2281665931805037, 'producer_wait_full_seconds': 12207.490889223816, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 33122.0838321434, '1': 20454.3368398546}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 460355, 'flush_seconds': 3008.735797537898, 'pending_bytes': 73664, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,597 patches/s**; new independent GMP audits: 28,773.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
