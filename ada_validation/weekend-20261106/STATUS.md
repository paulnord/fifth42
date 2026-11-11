# Ada combined search

Updated: 2026-11-11T06:40:37.193913+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,561,676,160**.
New replicated logical patches: **674,340,864** in 2,634,144 chunks.
Combined verified selected patches, including parents: **2,811,676,160**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6561676160]`.
Local cursor: 6,562,618,240; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 8438.106915055192, 'elapsed_seconds': 37330.881788122, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3668882300356681, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 164826, 'prepare_wall_seconds': 37325.63878300489, 'producer_wait_capacity_seconds': 0.16346701892325655, 'producer_wait_full_seconds': 7847.802975128347, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 23634.62064066314, '1': 13696.261144914839}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 329648, 'flush_seconds': 2144.4333806556533, 'pending_bytes': 18399, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,085 patches/s**; new independent GMP audits: 20,604.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
