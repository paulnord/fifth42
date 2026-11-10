# Ada combined search

Updated: 2026-11-10T09:21:58.928483+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,229,938,816**.
New replicated logical patches: **598,638,592** in 2,338,432 chunks.
Combined verified selected patches, including parents: **1,479,938,816**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5229938816]`.
Local cursor: 5,230,704,768; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 12097.91845193418, 'elapsed_seconds': 31640.792943823035, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6105237746554182, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2341137, 'prepare_wall_seconds': 31625.95162933896, 'producer_wait_capacity_seconds': 1.4857044032542035, 'producer_wait_full_seconds': 4845.641014238936, 'ready': 0, 'ready_depth_seconds': {'0': 23101.324221165793, '1': 2932.6575920048053, '2': 435.63464034273056, '3': 5171.176489487698}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 292642, 'flush_seconds': 1844.8128542846534, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,942 patches/s**; new independent GMP audits: 18,291.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
