# Boole combined search

Updated: 2026-11-09T22:05:26.304879+00:00

State: **running**. Run **boole-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **3,462,919,680**.
New replicated logical patches: **99,618,304** in 389,134 chunks.
Combined verified selected patches, including parents: **462,919,680**.
Fresh interval: `[3363301376, 3750000000]`; replicated: `[3363301376, 3462919680]`.
Local cursor: 3,463,079,424; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 690.0046694962657, 'elapsed_seconds': 5455.626815814001, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482168, 'mean_ready_depth': 0.9505141177049758, 'outstanding': 4, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 389514, 'prepare_wall_seconds': 5454.245323367359, 'producer_wait_capacity_seconds': 0.245773913920857, 'producer_wait_full_seconds': 992.3893696127925, 'ready': 3, 'ready_depth_seconds': {'0': 3088.6190966326394, '1': 827.7151693706983, '2': 259.94250731158536, '3': 1279.350041789061}, 'ready_limit': 3, 'reserved_bytes': 33554432}; buffer: {'flush_count': 48776, 'flush_seconds': 273.2189390382846, 'pending_bytes': 18208, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **18,271 patches/s**; new independent GMP audits: 3,044.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
