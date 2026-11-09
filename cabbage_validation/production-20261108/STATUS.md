# Cabbage combined search

Updated: 2026-11-09T21:20:17.390392+00:00

State: **running**. Run **cabbage-buffered-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **2,435,258,752**.
New replicated logical patches: **67,917,056** in 265,301 chunks.
Combined verified selected patches, including parents: **185,258,752**.
Fresh interval: `[2367341696, 3000000000]`; replicated: `[2367341696, 2435258752]`.
Local cursor: 2,435,566,976; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 936.8625312405638, 'elapsed_seconds': 2943.242122386, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482045, 'mean_ready_depth': 0.3049946023895197, 'outstanding': 1, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 265773, 'prepare_wall_seconds': 2942.307346486312, 'producer_wait_capacity_seconds': 0.16761843214044347, 'producer_wait_full_seconds': 91.13767990155611, 'ready': 0, 'ready_depth_seconds': {'0': 2363.516978441621, '1': 394.50710772676393, '2': 52.48825297044823, '3': 132.72978239518125}, 'ready_limit': 3, 'reserved_bytes': 8388608}; buffer: {'flush_count': 33240, 'flush_seconds': 187.78464445122518, 'pending_bytes': 72881, 'pending_chunks': 4}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **32 GiB**;
free-space reserve: 16 GiB.
Observed rate: **23,091 patches/s**; new independent GMP audits: 2,077.
Deadline: **2026-11-09T17:00:00-06:00**. Independent worker/deadline services on Cabbage; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under the unchanged original reservation.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
