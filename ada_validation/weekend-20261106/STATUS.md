# Ada combined search

Updated: 2026-11-11T08:55:54.056593+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,697,819,008**.
New replicated logical patches: **810,483,712** in 3,165,952 chunks.
Combined verified selected patches, including parents: **2,947,819,008**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6697819008]`.
Local cursor: 6,698,343,296; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10087.142930539616, 'elapsed_seconds': 45455.75154775102, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.3742996305111685, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 197998, 'prepare_wall_seconds': 45450.187440961075, 'producer_wait_capacity_seconds': 0.19630333507666364, 'producer_wait_full_seconds': 9955.864250003942, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 28441.68053747731, '1': 17014.07100893068}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 395994, 'flush_seconds': 2573.8538891613134, 'pending_bytes': 18416, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,841 patches/s**; new independent GMP audits: 24,750.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
