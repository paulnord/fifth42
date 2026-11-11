# Ada combined search

Updated: 2026-11-11T21:57:20.377597+00:00

State: **running**. Run **ada-allocated-r3-02-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,332,829,952**.
New replicated logical patches: **4,829,952** in 18,867 chunks.
Combined verified selected patches, including parents: **4,829,952**.
Fresh interval: `[10328000000, 10392000000]`; replicated: `[10328000000, 10332829952]`.
Local cursor: 10,333,024,768; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 563.013089524, 'elapsed_seconds': 894.0131759219803, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923609, 'mean_ready_depth': 0.23021841087977948, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 19499, 'prepare_wall_seconds': 893.8476641972084, 'producer_wait_capacity_seconds': 0.013191876118071377, 'producer_wait_full_seconds': 45.524269695044495, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 804.2930802559713, '1': 27.475308709195815, '2': 8.391373004182242, '3': 53.85341264959425}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 2738, 'flush_seconds': 24.464788143639453, 'pending_bytes': 349497, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **5,582 patches/s**; new independent GMP audits: 153.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
