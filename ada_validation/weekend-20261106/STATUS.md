# Ada combined search

Updated: 2026-11-10T14:07:49.145420+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,533,630,848**.
New replicated logical patches: **902,330,624** in 3,524,729 chunks.
Combined verified selected patches, including parents: **1,783,630,848**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5533630848]`.
Local cursor: 5,534,310,784; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 17747.90537014359, 'elapsed_seconds': 48789.44747337303, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6710395247819917, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3526997, 'prepare_wall_seconds': 48767.08049510862, 'producer_wait_capacity_seconds': 2.240864953317214, 'producer_wait_full_seconds': 8166.5409423260135, 'ready': 0, 'ready_depth_seconds': {'0': 34253.45131867909, '1': 5010.0543552733725, '2': 848.2321046438883, '3': 8677.709694115678}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 440880, 'flush_seconds': 3475.4151326118154, 'pending_bytes': 73675, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,506 patches/s**; new independent GMP audits: 27,555.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
