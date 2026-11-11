# Ada combined search

Updated: 2026-11-11T06:55:35.761967+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,577,396,608**.
New replicated logical patches: **690,061,312** in 2,695,552 chunks.
Combined verified selected patches, including parents: **2,827,396,608**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6577396608]`.
Local cursor: 6,577,847,168; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 8625.25201136031, 'elapsed_seconds': 38230.45022225601, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3676719484495912, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 168549, 'prepare_wall_seconds': 38225.7124175682, 'producer_wait_capacity_seconds': 0.16716416424605995, 'producer_wait_full_seconds': 8074.542607662501, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 24174.186096700025, '1': 14056.264123321977}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 337096, 'flush_seconds': 2192.1949431488174, 'pending_bytes': 18414, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,058 patches/s**; new independent GMP audits: 21,069.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
