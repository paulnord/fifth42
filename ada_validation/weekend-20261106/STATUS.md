# Ada combined search

Updated: 2026-11-10T11:22:16.813690+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,358,954,624**.
New replicated logical patches: **727,654,400** in 2,842,400 chunks.
Combined verified selected patches, including parents: **1,608,954,624**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5358954624]`.
Local cursor: 5,359,841,408; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 14416.274142701935, 'elapsed_seconds': 38853.69407099602, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6419037151230291, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 2845215, 'prepare_wall_seconds': 38835.65336818952, 'producer_wait_capacity_seconds': 1.8070632495800965, 'producer_wait_full_seconds': 6185.216937289748, 'ready': 0, 'ready_depth_seconds': {'0': 27728.694234136376, '1': 3899.5403315592557, '2': 635.588274748472, '3': 6589.871229789918}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 355651, 'flush_seconds': 2616.944425635971, 'pending_bytes': 128915, 'pending_chunks': 7}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,747 patches/s**; new independent GMP audits: 22,229.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
