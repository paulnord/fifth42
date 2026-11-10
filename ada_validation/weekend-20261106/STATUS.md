# Ada combined search

Updated: 2026-11-10T10:22:09.494410+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,294,616,704**.
New replicated logical patches: **663,316,480** in 2,591,080 chunks.
Combined verified selected patches, including parents: **1,544,616,704**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5294616704]`.
Local cursor: 5,295,855,744; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 13302.89934352535, 'elapsed_seconds': 35245.72267949302, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6246680595932669, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2595242, 'prepare_wall_seconds': 35229.27062852954, 'producer_wait_capacity_seconds': 1.647655857843347, 'producer_wait_full_seconds': 5501.902511176944, 'ready': 0, 'ready_depth_seconds': {'0': 25483.703202265257, '1': 3373.3072660149774, '2': 522.5667024789727, '3': 5866.145508062793}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 324405, 'flush_seconds': 2181.621501055488, 'pending_bytes': 36836, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,850 patches/s**; new independent GMP audits: 20,276.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
