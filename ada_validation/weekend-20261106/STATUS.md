# Ada combined search

Updated: 2026-11-10T03:35:55.176131+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,841,932,928**.
New replicated logical patches: **210,632,704** in 822,784 chunks.
Combined verified selected patches, including parents: **1,091,932,928**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4841932928]`.
Local cursor: 4,842,532,992; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 4311.78546492348, 'elapsed_seconds': 10875.492495322018, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482387, 'mean_ready_depth': 0.5556965358533756, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 824710, 'prepare_wall_seconds': 10870.251363433897, 'producer_wait_capacity_seconds': 0.5227770606870763, 'producer_wait_full_seconds': 1491.2817539459793, 'ready': 0, 'ready_depth_seconds': {'0': 8169.5236979498295, '1': 971.9449450002867, '2': 130.54299297719263, '3': 1603.4808581317193}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 103088, 'flush_seconds': 569.1185963183525, 'pending_bytes': 110511, 'pending_chunks': 6}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,413 patches/s**; new independent GMP audits: 6,444.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
