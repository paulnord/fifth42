# Ada combined search

Updated: 2026-11-10T08:51:51.663866+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,197,219,968**.
New replicated logical patches: **565,919,744** in 2,210,624 chunks.
Combined verified selected patches, including parents: **1,447,219,968**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5197219968]`.
Local cursor: 5,197,752,448; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 11455.437055365881, 'elapsed_seconds': 29833.202666633006, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6048474266339205, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2212394, 'prepare_wall_seconds': 29819.179269993678, 'producer_wait_capacity_seconds': 1.4037645545322448, 'producer_wait_full_seconds': 4526.151846214721, 'ready': 2, 'ready_depth_seconds': {'0': 21856.24532037822, '1': 2742.1191034504445, '2': 402.09796733624535, '3': 4832.740274346084}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 276549, 'flush_seconds': 1708.1556403500726, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,985 patches/s**; new independent GMP audits: 17,285.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
