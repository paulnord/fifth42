# Ada combined search

Updated: 2026-11-10T17:38:46.821654+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,750,704,512**.
New replicated logical patches: **1,119,404,288** in 4,372,673 chunks.
Combined verified selected patches, including parents: **2,000,704,512**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5750704512]`.
Local cursor: 5,751,960,704; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 22310.869334083633, 'elapsed_seconds': 61448.35979198199, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6931637232319153, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 4377315, 'prepare_wall_seconds': 61420.56430397404, 'producer_wait_capacity_seconds': 2.7831735172658227, 'producer_wait_full_seconds': 10905.348211536882, 'ready': 0, 'ready_depth_seconds': {'0': 42933.50807908364, '1': 5977.870511899062, '2': 995.0402529194253, '3': 11541.94094738888}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 547234, 'flush_seconds': 4104.750270802702, 'pending_bytes': 36836, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,236 patches/s**; new independent GMP audits: 34,198.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
