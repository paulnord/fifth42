# Boole combined search

Updated: 2026-11-12T22:09:39.945318+00:00

State: **running**. Run **boole-range-r3-20261111-30-recovery2**; gpu with 16 preparation workers.
Verified replicated cursor: **8,946,769,664**.
New replicated logical patches: **12,908,800** in 50,425 chunks.
Combined verified selected patches, including parents: **26,769,664**.
Fresh interval: `[8933860864, 8984000000]`; replicated: `[8933860864, 8946769664]`.
Local cursor: 8,947,031,808; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 0.19864544179290533, 'elapsed_seconds': 1801.6434290300822, 'inflight': 1, 'max_outstanding': 3, 'maximum_prepared_payload_bytes': 7681479, 'mean_ready_depth': 0.999275304872836, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 37748736, 'preparation_batch_windows': 16, 'preparation_batches': 3202, 'prepare_wall_seconds': 1799.2624674382387, 'producer_wait_capacity_seconds': 0.004292203579097986, 'producer_wait_full_seconds': 1236.7866789344698, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 1.305639233905822, '1': 1800.337786816177}, 'ready_limit': 1, 'reserved_bytes': 37748736}; buffer: {'flush_count': 6431, 'flush_seconds': 48.343065087799914, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **7,274 patches/s**; new independent GMP audits: 401.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Boole; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
