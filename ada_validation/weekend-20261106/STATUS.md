# Ada combined search

Updated: 2026-11-11T10:41:13.793231+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,800,767,872**.
New replicated logical patches: **913,432,576** in 3,568,096 chunks.
Combined verified selected patches, including parents: **3,050,767,872**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6800767872]`.
Local cursor: 6,801,496,960; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11329.643479230232, 'elapsed_seconds': 51775.228565634985, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3799580355753099, 'outstanding': 1, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 223180, 'prepare_wall_seconds': 51768.861423157156, 'producer_wait_capacity_seconds': 0.2212820965796709, 'producer_wait_full_seconds': 11685.54963011673, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 32102.814427621663, '1': 19672.414137261338}, 'ready_limit': 1, 'reserved_bytes': 12582912}; buffer: {'flush_count': 446360, 'flush_seconds': 2898.6080101233674, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,656 patches/s**; new independent GMP audits: 27,898.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
