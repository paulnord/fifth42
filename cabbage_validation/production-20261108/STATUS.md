# Cabbage combined search

Updated: 2026-11-12T09:01:21.231723+00:00

State: **running**. Run **cabbage-extended-memory-r2-cap100-20261111-job-44**; gpu with 16 preparation workers.
Verified replicated cursor: **9,816,002,048**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **2,048**.
Fresh interval: `[9816000000, 9880000000]`; replicated: `[9816000000, 9816002048]`.
Local cursor: 9,816,163,840; physical tasks group up to 2 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 8; ready queue: {'active': 1, 'consumer_wait_empty_seconds': 2.1131919409381226, 'elapsed_seconds': 10.913753861910664, 'inflight': 1, 'max_outstanding': 3, 'maximum_item_payload_bytes': 134217728, 'maximum_prepared_payload_bytes': 15350111, 'mean_ready_depth': 0.40605838091508667, 'outstanding': 3, 'peak_outstanding': 3, 'peak_ready': 1, 'peak_reserved_bytes': 402653184, 'preparation_batch_windows': 16, 'preparation_batches': 26, 'prepare_wall_seconds': 10.033415435580537, 'producer_wait_capacity_seconds': 2.6106019504368305e-05, 'producer_wait_full_seconds': 2.037533905939199, 'queue_units': 'bounded preparation batches; original execution/journal windows preserved', 'ready': 1, 'ready_depth_seconds': {'0': 6.4821295130532235, '1': 4.431621222873218}, 'ready_limit': 1, 'reserved_bytes': 402653184}; buffer: {'flush_count': 48, 'flush_seconds': 0.3071212823269889, 'pending_bytes': 35300, 'pending_chunks': 1}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **8,748 patches/s**; new independent GMP audits: 4.
Deadline: **2026-11-12T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

Coverage is limited to this explicitly reserved interval and its verified parent accounting. Fresh disjoint reservations do not fill gaps in earlier coverage.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.

Residual band: **0 < |a^5+b^5-c^5| <= 100**. All exact hits remain in status.json.
Below 12: []
Equal to 12: []
At most 42: []
From 43 through 100: []
