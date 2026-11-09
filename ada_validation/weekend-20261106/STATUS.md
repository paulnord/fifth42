# Ada combined search

Updated: 2026-11-09T23:57:28.579366+00:00

State: **running**. Run **ada-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,588,614,272**.
New replicated logical patches: **23,658,496** in 92,416 chunks.
Combined verified selected patches, including parents: **838,614,272**.
Fresh interval: `[4564955776, 11250000001]`; replicated: `[4564955776, 4588614272]`.
Local cursor: 4,589,292,160; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 512.1155531546101, 'elapsed_seconds': 1243.001689445984, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482047, 'mean_ready_depth': 0.5157818274763488, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 95052, 'prepare_wall_seconds': 1242.3811349854222, 'producer_wait_capacity_seconds': 0.06245972984470427, 'producer_wait_full_seconds': 154.2545437993831, 'ready': 0, 'ready_depth_seconds': {'0': 950.3259657859453, '1': 111.12877117900643, '2': 14.651943097473122, '3': 166.89500852156198}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 11881, 'flush_seconds': 63.87923846981721, 'pending_bytes': 73647, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **120 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,575 patches/s**; new independent GMP audits: 743.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
