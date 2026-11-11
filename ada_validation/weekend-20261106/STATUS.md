# Ada combined search

Updated: 2026-11-11T08:10:48.385282+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,653,002,624**.
New replicated logical patches: **765,667,328** in 2,990,888 chunks.
Combined verified selected patches, including parents: **2,903,002,624**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6653002624]`.
Local cursor: 6,653,582,208; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 9543.8540247794, 'elapsed_seconds': 42744.659799834015, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.37186976217673035, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 187046, 'prepare_wall_seconds': 42739.40059375833, 'producer_wait_capacity_seconds': 0.18543738109292462, 'producer_wait_full_seconds': 9238.088983836351, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 26849.213323840464, '1': 15895.44647408952}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 374090, 'flush_seconds': 2431.520277957199, 'pending_bytes': 18403, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,924 patches/s**; new independent GMP audits: 23,381.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
