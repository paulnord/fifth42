# Ada combined search

Updated: 2026-11-11T09:26:01.132967+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,727,310,208**.
New replicated logical patches: **839,974,912** in 3,281,152 chunks.
Combined verified selected patches, including parents: **2,977,310,208**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6727310208]`.
Local cursor: 6,728,041,344; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 10446.14169466187, 'elapsed_seconds': 47260.48982819199, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7683300, 'mean_ready_depth': 0.37588559116466336, 'outstanding': 2, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 205239, 'prepare_wall_seconds': 47254.70372304105, 'producer_wait_capacity_seconds': 0.2034433296066709, 'producer_wait_full_seconds': 10440.733448473271, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 29495.952668597514, '1': 17764.537157801504}, 'ready_limit': 1, 'reserved_bytes': 25165824}; buffer: {'flush_count': 410476, 'flush_seconds': 2666.6965245876927, 'pending_bytes': 73651, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,788 patches/s**; new independent GMP audits: 25,655.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
