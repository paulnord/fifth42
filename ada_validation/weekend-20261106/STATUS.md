# Ada combined search

Updated: 2026-11-09T21:11:34.396383+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,434,275,712**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **684,275,712**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4434275712]`.
Local cursor: 4,435,230,080; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 16.147091401799116, 'elapsed_seconds': 40.310110235994216, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481328, 'mean_ready_depth': 0.4930335223991843, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3177, 'prepare_wall_seconds': 40.2935637498158, 'producer_wait_capacity_seconds': 0.001849165593739599, 'producer_wait_full_seconds': 4.64643447502749, 'ready': 1, 'ready_depth_seconds': {'0': 31.03436608472839, '1': 3.7371835814556107, '2': 0.47862670687027276, '3': 5.059932880918495}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 397, 'flush_seconds': 2.183263547020033, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,605 patches/s**; new independent GMP audits: 25.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
