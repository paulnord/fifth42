# Ada combined search

Updated: 2026-11-11T00:39:06.634841+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,180,219,776**.
New replicated logical patches: **292,884,480** in 1,144,080 chunks.
Combined verified selected patches, including parents: **2,430,219,776**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6180219776]`.
Local cursor: 6,180,969,344; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 3689.6959825165104, 'elapsed_seconds': 15639.375255702005, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34739590039068824, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 71642, 'prepare_wall_seconds': 15636.86617502768, 'producer_wait_capacity_seconds': 0.07114718022057787, 'producer_wait_full_seconds': 2916.831441489223, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 10206.320404464554, '1': 5433.054848502448}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 143280, 'flush_seconds': 929.4038663622923, 'pending_bytes': 18418, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,763 patches/s**; new independent GMP audits: 8,956.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
