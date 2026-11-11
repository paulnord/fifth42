# Ada combined search

Updated: 2026-11-11T16:20:45.554470+00:00

State: **running**. Run **ada-preparation-rotation-02-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,896,991,616**.
New replicated logical patches: **14,295,040** in 55,840 chunks.
Combined verified selected patches, including parents: **3,146,991,616**.
Fresh interval: `[6882696576, 7000000000]`; replicated: `[6882696576, 6896991616]`.
Local cursor: 6,897,765,760; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 173.21192010404775, 'elapsed_seconds': 918.1557133109891, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683495, 'mean_ready_depth': 0.4423432759531251, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3642, 'prepare_wall_seconds': 917.3268374835607, 'producer_wait_capacity_seconds': 0.003535242867656052, 'producer_wait_full_seconds': 276.34620111907134, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 512.0157040439663, '1': 406.1400060610613}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 7280, 'flush_seconds': 44.51973402075237, 'pending_bytes': 18428, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 8 GiB.
Observed rate: **16,238 patches/s**; new independent GMP audits: 456.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
