# Ada combined search

Updated: 2026-11-11T01:39:20.923447+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,245,849,984**.
New replicated logical patches: **358,514,688** in 1,400,448 chunks.
Combined verified selected patches, including parents: **2,495,849,984**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6245849984]`.
Local cursor: 6,246,636,416; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 4514.623727127793, 'elapsed_seconds': 19262.118125886016, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3505970343803764, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 87714, 'prepare_wall_seconds': 19259.150830050465, 'producer_wait_capacity_seconds': 0.08707863686140627, 'producer_wait_full_seconds': 3668.665427747532, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 12508.87663207989, '1': 6753.241490820132}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 175424, 'flush_seconds': 1138.0909042935236, 'pending_bytes': 18420, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,652 patches/s**; new independent GMP audits: 10,965.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
