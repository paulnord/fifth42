# Ada combined search

Updated: 2026-11-11T15:19:51.080842+00:00

State: **stopped**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,842,653,824**.
New replicated logical patches: **955,318,528** in 3,731,713 chunks.
Combined verified selected patches, including parents: **3,092,653,824**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6842653824]`.
Local cursor: 6,842,653,824; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11816.665142188082, 'elapsed_seconds': 54360.98337929597, 'inflight': 0, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.38252561300665516, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 233234, 'prepare_wall_seconds': 54353.515251064906, 'producer_wait_capacity_seconds': 0.23114489222643897, 'producer_wait_full_seconds': 12434.484971797909, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 33566.51488449919, '1': 20794.468490809784}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 466465, 'flush_seconds': 3053.9498992306762, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,574 patches/s**; new independent GMP audits: 29,155.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
