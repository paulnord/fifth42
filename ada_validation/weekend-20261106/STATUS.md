# Ada combined search

Updated: 2026-11-11T04:10:06.207163+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,406,052,736**.
New replicated logical patches: **518,717,440** in 2,026,240 chunks.
Combined verified selected patches, including parents: **2,656,052,736**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6406052736]`.
Local cursor: 6,407,232,384; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 6512.932192784618, 'elapsed_seconds': 28298.573657887988, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.35870632242641015, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 126885, 'prepare_wall_seconds': 28294.855878946604, 'producer_wait_capacity_seconds': 0.12582124181790277, 'producer_wait_full_seconds': 5670.352962108096, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 18147.696370222082, '1': 10150.877286733885}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 253768, 'flush_seconds': 1647.190841331554, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,365 patches/s**; new independent GMP audits: 15,861.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
