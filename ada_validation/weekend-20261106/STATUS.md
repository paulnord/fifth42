# Ada combined search

Updated: 2026-11-12T23:58:56.980014+00:00

State: **failed**. Run **ada-sharing-30-7b1e3c6c84954267**; gpu with 16 preparation workers.
Verified replicated cursor: **8,972,726,016**.
New replicated logical patches: **3,852,288** in 15,048 chunks.
Combined verified selected patches, including parents: **3,852,288**.
Fresh interval: `[8968873728, 8984000000]`; replicated: `[8968873728, 8972726016]`.
Local cursor: 8,972,726,016; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 120.57407997536939, 'elapsed_seconds': 353.3995717340149, 'inflight': 0, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15357648, 'mean_ready_depth': 0.22474257179528517, 'outstanding': 0, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 941, 'prepare_wall_seconds': 353.04670470778365, 'producer_wait_capacity_seconds': 0.0010229609906673431, 'producer_wait_full_seconds': 19.654349582851864, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 0, 'ready_depth_seconds': {'0': 273.97564049612265, '1': 79.42392862285487}, 'ready_limit': 1, 'reserved_bytes': 0}; buffer: {'flush_count': 1881, 'flush_seconds': 14.415383348008618, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **10,901 patches/s**; new independent GMP audits: 118.
Deadline: **2026-11-13T09:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: ['RuntimeError: Another active fifth service: fifth42-overnight-live-status-20261112.service loaded active running [systemd-run] /usr/bin/python3 -B /home/pnord/fifth42-overnight-sharing-20261112/live_status.py'].

This run covers its assigned sealed r4 suffix under an unchanged original child claim. The predecessor journal is provenance; only this run's native interval advances here. The renewed coordinator holds the original parent lease until the new cutoff.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
