# Ada combined search

Updated: 2026-11-10T02:35:36.937235+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,772,653,184**.
New replicated logical patches: **141,352,960** in 552,160 chunks.
Combined verified selected patches, including parents: **1,022,653,184**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4772653184]`.
Local cursor: 4,772,857,984; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 2894.2629156893236, 'elapsed_seconds': 7255.618187074026, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482301, 'mean_ready_depth': 0.5475265591466064, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 552439, 'prepare_wall_seconds': 7252.1104731285595, 'producer_wait_capacity_seconds': 0.35001666308380663, 'producer_wait_full_seconds': 974.5011034014751, 'ready': 0, 'ready_depth_seconds': {'0': 5469.132856306387, '1': 649.7978415883263, '2': 87.21664699306712, '3': 1049.4708416252397}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 69054, 'flush_seconds': 379.7950757520157, 'pending_bytes': 128908, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,491 patches/s**; new independent GMP audits: 4,316.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
