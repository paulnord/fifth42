# Ada combined search

Updated: 2026-11-10T00:12:31.927362+00:00

State: **running**. Run **ada-overnight-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,605,985,408**.
New replicated logical patches: **41,029,632** in 160,272 chunks.
Combined verified selected patches, including parents: **855,985,408**.
Fresh interval: `[4564955776, 11250000001]`; replicated: `[4564955776, 4605985408]`.
Local cursor: 4,606,931,584; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 880.0874272806686, 'elapsed_seconds': 2144.4145006409963, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482047, 'mean_ready_depth': 0.5170684906754298, 'outstanding': 2, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 163805, 'prepare_wall_seconds': 2143.3524066736572, 'producer_wait_capacity_seconds': 0.10759053152287379, 'producer_wait_full_seconds': 267.139555387781, 'ready': 1, 'ready_depth_seconds': {'0': 1639.4953648135415, '1': 190.229117153096, '2': 25.489998298173305, '3': 289.2000184931676}, 'ready_limit': 3, 'reserved_bytes': 16777216}; buffer: {'flush_count': 20475, 'flush_seconds': 110.98098736576503, 'pending_bytes': 73647, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **120 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,554 patches/s**; new independent GMP audits: 1,280.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
