# Ada combined search

Updated: 2026-11-11T05:10:20.716095+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,468,694,912**.
New replicated logical patches: **581,359,616** in 2,270,936 chunks.
Combined verified selected patches, including parents: **2,718,694,912**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6468694912]`.
Local cursor: 6,470,013,824; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 7291.772288122098, 'elapsed_seconds': 31913.768952717015, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.36199608836625535, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 142218, 'prepare_wall_seconds': 31909.190023600997, 'producer_wait_capacity_seconds': 0.1410212479531765, 'producer_wait_full_seconds': 6520.5541855129995, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 20361.109424344962, '1': 11552.659525908006}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 284432, 'flush_seconds': 1846.5260475203395, 'pending_bytes': 18411, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,253 patches/s**; new independent GMP audits: 17,778.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
