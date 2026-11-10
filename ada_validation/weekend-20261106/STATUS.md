# Ada combined search

Updated: 2026-11-10T17:53:55.299363+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,766,805,888**.
New replicated logical patches: **1,135,505,664** in 4,435,569 chunks.
Combined verified selected patches, including parents: **2,016,805,888**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5766805888]`.
Local cursor: 5,767,272,832; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 22633.280735772743, 'elapsed_seconds': 62354.393192844, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6948542923992808, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4436956, 'prepare_wall_seconds': 62326.22643410164, 'producer_wait_capacity_seconds': 2.8212352299015038, 'producer_wait_full_seconds': 11110.813546426129, 'ready': 0, 'ready_depth_seconds': {'0': 43545.762322229624, '1': 6046.340236573771, '2': 1005.9943767124205, '3': 11756.296256667178}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 554696, 'flush_seconds': 4150.311857482651, 'pending_bytes': 55251, 'pending_chunks': 3}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,216 patches/s**; new independent GMP audits: 34,664.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
