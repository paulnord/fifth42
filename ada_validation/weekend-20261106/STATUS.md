# Ada combined search

Updated: 2026-11-11T10:11:06.729314+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,771,772,288**.
New replicated logical patches: **884,436,992** in 3,454,832 chunks.
Combined verified selected patches, including parents: **3,021,772,288**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6771772288]`.
Local cursor: 6,772,190,080; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10978.12091331114, 'elapsed_seconds': 49967.02439728199, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.37834399565300314, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 216019, 'prepare_wall_seconds': 49960.82277949696, 'producer_wait_capacity_seconds': 0.21423613576916978, 'producer_wait_full_seconds': 11181.979264965397, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 31062.300733859243, '1': 18904.72366135876}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 432036, 'flush_seconds': 2806.919746165804, 'pending_bytes': 92088, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,708 patches/s**; new independent GMP audits: 27,003.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
