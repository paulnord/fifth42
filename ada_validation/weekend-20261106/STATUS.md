# Ada combined search

Updated: 2026-11-11T02:24:36.446213+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,294,506,368**.
New replicated logical patches: **407,171,072** in 1,590,512 chunks.
Combined verified selected patches, including parents: **2,544,506,368**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6294506368]`.
Local cursor: 6,295,395,200; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 5123.435096893692, 'elapsed_seconds': 21978.830240702024, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3530780181269423, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 99624, 'prepare_wall_seconds': 21976.00921958685, 'producer_wait_capacity_seconds': 0.09886779321823269, 'producer_wait_full_seconds': 4253.055080253049, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 14218.588416663406, '1': 7760.2418221355765}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 199246, 'flush_seconds': 1292.8503520332742, 'pending_bytes': 110505, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,566 patches/s**; new independent GMP audits: 12,453.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
