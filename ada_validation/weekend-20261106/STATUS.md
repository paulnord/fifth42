# Ada combined search

Updated: 2026-11-11T22:14:24.668057+00:00

State: **failed**. Run **ada-allocated-r3-02-20261111**; gpu with 16 preparation workers.
Verified replicated cursor: **10,337,095,936**.
New replicated logical patches: **9,095,936** in 35,531 chunks.
Combined verified selected patches, including parents: **9,095,936**.
Fresh interval: `[10328000000, 10392000000]`; replicated: `[10328000000, 10337095936]`.
Local cursor: 10,337,095,936; physical tasks group up to 1 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1227.4529894007137, 'elapsed_seconds': 1907.047485952964, 'inflight': 0, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 1923609, 'mean_ready_depth': 0.21472857306260681, 'outstanding': 0, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batch_windows': 1, 'preparation_batches': 35531, 'prepare_wall_seconds': 1897.0713444631547, 'producer_wait_capacity_seconds': 0.02410798450000584, 'producer_wait_full_seconds': 89.93021492031403, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 1723.0917592786718, '1': 63.470601752982475, '2': 15.428379464661703, '3': 105.0567415796686}, 'ready_limit': 3, 'reserved_bytes': 0}; buffer: {'flush_count': 5010, 'flush_seconds': 44.472313383594155, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **4,770 patches/s**; new independent GMP audits: 278.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: ["TimeoutExpired: Command '['ps', '-eo', 'pid=,args=']' timed out after 5 seconds"].

This run uses its assigned child claim. Historical coverage is imported only for a recorded continuation; fresh claims keep their reference parent separate. A shared coordinator holds the original parent lease.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
