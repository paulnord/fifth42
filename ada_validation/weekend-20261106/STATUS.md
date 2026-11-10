# Ada combined search

Updated: 2026-11-10T00:35:15.645880+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **4,631,302,272**.
New replicated logical patches: **2,048** in 8 chunks.
Combined verified selected patches, including parents: **881,302,272**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 4631302272]`.
Local cursor: 4,632,119,424; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 15.639573033200577, 'elapsed_seconds': 40.18908944900613, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 481593, 'mean_ready_depth': 0.5539994180617983, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3106, 'prepare_wall_seconds': 40.164436707040295, 'producer_wait_capacity_seconds': 0.0019454031134955585, 'producer_wait_full_seconds': 5.397182464948855, 'ready': 0, 'ready_depth_seconds': {'0': 30.098745970870368, '1': 3.738364467106294, '2': 0.5295667199534364, '3': 5.822411420056596}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 388, 'flush_seconds': 2.122056962456554, 'pending_bytes': 36834, 'pending_chunks': 2}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **19,771 patches/s**; new independent GMP audits: 25.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
