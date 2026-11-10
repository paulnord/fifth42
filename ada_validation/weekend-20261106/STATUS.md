# Ada combined search

Updated: 2026-11-10T07:36:42.965125+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,114,169,472**.
New replicated logical patches: **482,869,248** in 1,886,208 chunks.
Combined verified selected patches, including parents: **1,364,169,472**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5114169472]`.
Local cursor: 5,115,150,464; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 9901.562651366403, 'elapsed_seconds': 25322.582771797024, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.5857687328527441, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 1889574, 'prepare_wall_seconds': 25310.600264037144, 'producer_wait_capacity_seconds': 1.1985755920177326, 'producer_wait_full_seconds': 3748.1936478157877, 'ready': 0, 'ready_depth_seconds': {'0': 18805.289130833873, '1': 2208.140900098777, '2': 302.42189752467675, '3': 4006.7308425487136}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 236196, 'flush_seconds': 1309.6091216802015, 'pending_bytes': 110498, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,103 patches/s**; new independent GMP audits: 14,763.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
