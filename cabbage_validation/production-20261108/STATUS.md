# Cabbage combined search

Updated: 2026-11-09T21:05:12.354050+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,413,495,680**.
New replicated logical patches: **46,153,984** in 180,289 chunks.
Combined verified selected patches, including parents: **163,495,680**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2413495680]`.
Local cursor: 2,414,729,344; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 650.7924784750794, 'elapsed_seconds': 2041.3210780459922, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482045, 'mean_ready_depth': 0.30226050491021555, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 184665, 'prepare_wall_seconds': 2040.6670969492407, 'producer_wait_capacity_seconds': 0.11635471176123247, 'producer_wait_full_seconds': 61.544269926671404, 'ready': 0, 'ready_depth_seconds': {'0': 1640.584475943062, '1': 274.53058862895705, '2': 36.13788664073218, '3': 90.06812594120856}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 23095, 'flush_seconds': 130.92173747497145, 'pending_bytes': 91111, 'pending_chunks': 5}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,122 patches/s**; new independent GMP audits: 1,443.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
