# Cabbage combined search

Updated: 2026-11-09T21:35:18.185496+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,455,711,872**.
New replicated logical patches: **88,370,176** in 345,196 chunks.
Combined verified selected patches, including parents: **205,711,872**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2455711872]`.
Local cursor: 2,456,327,552; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 1225.290330473741, 'elapsed_seconds': 3846.13691988599, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482045, 'mean_ready_depth': 0.30732857400778746, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 347047, 'prepare_wall_seconds': 3844.9183288945933, 'producer_wait_capacity_seconds': 0.21873558877268806, 'producer_wait_full_seconds': 121.41372804139974, 'ready': 0, 'ready_depth_seconds': {'0': 3086.468107907276, '1': 513.7949477167567, '2': 69.38876345934113, '3': 176.48510013060877}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 43406, 'flush_seconds': 244.1936654074234, 'pending_bytes': 109336, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,080 patches/s**; new independent GMP audits: 2,712.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
