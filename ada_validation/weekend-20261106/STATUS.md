# Ada combined search

Updated: 2026-11-10T21:53:37.637645+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **5,995,371,392**.
New replicated logical patches: **108,036,096** in 422,016 chunks.
Combined verified selected patches, including parents: **2,245,371,392**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 5995371392]`.
Local cursor: 5,996,649,344; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 1374.208256915561, 'elapsed_seconds': 5711.762843349017, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681797, 'mean_ready_depth': 0.33844847791635463, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 26650, 'prepare_wall_seconds': 5710.573291479901, 'producer_wait_capacity_seconds': 0.026505785004701465, 'producer_wait_full_seconds': 1003.4597889385186, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 3778.625400574354, '1': 1933.137440550665}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 53296, 'flush_seconds': 346.77869752497645, 'pending_bytes': 18412, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,110 patches/s**; new independent GMP audits: 3,332.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
