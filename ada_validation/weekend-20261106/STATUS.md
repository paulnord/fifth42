# Ada combined search

Updated: 2026-11-10T20:38:20.490358+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **5,909,412,736**.
New replicated logical patches: **22,077,440** in 86,240 chunks.
Combined verified selected patches, including parents: **2,159,412,736**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 5909412736]`.
Local cursor: 5,910,494,080; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 289.85998862661654, 'elapsed_seconds': 1193.87510354002, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7679899, 'mean_ready_depth': 0.33393352917455416, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 5610, 'prepare_wall_seconds': 1193.2974681121996, 'producer_wait_capacity_seconds': 0.0055842032306827605, 'producer_wait_full_seconds': 203.5099166512955, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 795.2001739552361, '1': 398.67492671875516}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 11216, 'flush_seconds': 74.34051986731356, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,240 patches/s**; new independent GMP audits: 702.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
