# Ada combined search

Updated: 2026-11-11T07:55:44.826764+00:00

State: **running**. Run **ada-preparation-20261110**; gpu with 16 preparation workers.
Verified replicated cursor: **6,637,714,304**.
New replicated logical patches: **750,379,008** in 2,931,168 chunks.
Combined verified selected patches, including parents: **2,887,714,304**.
Fresh interval: `[5887335296, 7000000000]`; replicated: `[5887335296, 6637714304]`.
Local cursor: 6,638,521,216; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 9361.788156757772, 'elapsed_seconds': 41839.57446294697, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7682585, 'mean_ready_depth': 0.3710235848094661, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 183362, 'prepare_wall_seconds': 41833.783466352324, 'producer_wait_capacity_seconds': 0.1818083616090007, 'producer_wait_full_seconds': 9001.57782014599, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 26316.105555896822, '1': 15523.468904145178}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 366720, 'flush_seconds': 2383.9781934492057, 'pending_bytes': 18419, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **64 GiB**;
free-space reserve: 8 GiB.
Observed rate: **17,951 patches/s**; new independent GMP audits: 22,921.
Deadline: **2026-11-11T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
