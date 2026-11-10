# Ada combined search

Updated: 2026-11-10T23:23:53.887785+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,097,034,112**.
New replicated logical patches: **209,698,816** in 819,136 chunks.
Combined verified selected patches, including parents: **2,347,034,112**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6097034112]`.
Local cursor: 6,097,992,576; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2650.1750759976567, 'elapsed_seconds': 11135.795677511021, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682185, 'mean_ready_depth': 0.34329958121023135, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 51426, 'prepare_wall_seconds': 11133.862647775153, 'producer_wait_capacity_seconds': 0.0510395803139545, 'producer_wait_full_seconds': 2023.119516421517, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 7312.881681992731, '1': 3822.913992532238}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 102848, 'flush_seconds': 666.5213516482618, 'pending_bytes': 18417, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,915 patches/s**; new independent GMP audits: 6,429.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
