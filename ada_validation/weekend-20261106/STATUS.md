# Ada combined search

Updated: 2026-11-11T01:54:24.393731+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,261,676,928**.
New replicated logical patches: **374,341,632** in 1,462,272 chunks.
Combined verified selected patches, including parents: **2,511,676,928**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6261676928]`.
Local cursor: 6,262,911,872; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 4717.002106321976, 'elapsed_seconds': 20161.79064517701, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3513963758921072, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 91672, 'prepare_wall_seconds': 20159.16476892261, 'producer_wait_capacity_seconds': 0.09098424774128944, 'producer_wait_full_seconds': 3860.481238997949, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 13077.01047873142, '1': 7084.7801642105915}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 183343, 'flush_seconds': 1189.4819215248572, 'pending_bytes': 36831, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,624 patches/s**; new independent GMP audits: 11,459.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
