# Ada combined search

Updated: 2026-11-10T18:24:02.226625+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,796,444,544**.
New replicated logical patches: **1,165,144,320** in 4,551,345 chunks.
Combined verified selected patches, including parents: **2,046,444,544**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5796444544]`.
Local cursor: 5,797,749,120; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 23277.134686773934, 'elapsed_seconds': 64159.295064601, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6983126456439661, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4555908, 'prepare_wall_seconds': 64129.91002598411, 'producer_wait_capacity_seconds': 2.8966365839587525, 'producer_wait_full_seconds': 11526.694689631113, 'ready': 3, 'ready_depth_seconds': {'0': 44763.64850093151, '1': 6178.538332143275, '2': 1026.6159442025819, '3': 12190.492286221648}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 569575, 'flush_seconds': 4238.427272756118, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,178 patches/s**; new independent GMP audits: 35,594.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
