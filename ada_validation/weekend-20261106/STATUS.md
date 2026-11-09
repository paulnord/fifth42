# Ada combined search

Updated: 2026-11-09T21:56:39.379533+00:00

State: **running**. Run **ada-group4-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,489,319,808**.
New replicated logical patches: **55,046,144** in 215,024 chunks.
Combined verified selected patches, including parents: **739,319,808**.
Fresh interval: `[4434273664, 11250000001]`; replicated: `[4434273664, 4489319808]`.
Local cursor: 4,489,477,504; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1104.5395591309061, 'elapsed_seconds': 2746.8580491279718, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482483, 'mean_ready_depth': 0.4947812331859101, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 215188, 'prepare_wall_seconds': 2746.1292553897365, 'producer_wait_capacity_seconds': 0.1251692541409284, 'producer_wait_full_seconds': 319.2495965526323, 'ready': 0, 'ready_depth_seconds': {'0': 2117.000290905533, '1': 248.55619250313612, '2': 33.36707417387515, '3': 347.9344906944316}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 26898, 'flush_seconds': 148.26826973061543, 'pending_bytes': 73629, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **19,793 patches/s**; new independent GMP audits: 1,682.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
