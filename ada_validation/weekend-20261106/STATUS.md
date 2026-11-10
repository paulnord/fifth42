# Ada combined search

Updated: 2026-11-10T12:07:24.510523+00:00

State: **running**. Run **ada-suballocation-20261109**; gpu with 16 preparation workers.
Verified replicated cursor: **5,407,410,304**.
New replicated logical patches: **776,110,080** in 3,031,680 chunks.
Combined verified selected patches, including parents: **1,657,410,304**.
Fresh interval: `[4631300224, 7000000000]`; replicated: `[4631300224, 5407410304]`.
Local cursor: 5,407,635,584; physical tasks group up to 4 original width-8 cells.
Saved-root reuse, exact host optimizations, low64 filtering and an immutable canonical task cache are enabled.
Journal records remain separate 256-cell receipts, with up to eight buffered before a durable checkpoint.
Dispatch chunksize: 4; ready queue: {'active': 0, 'consumer_wait_empty_seconds': 15233.283280592994, 'elapsed_seconds': 41566.71214027499, 'inflight': 1, 'max_outstanding': 5, 'maximum_prepared_payload_bytes': 482928, 'mean_ready_depth': 0.6540372112321621, 'outstanding': 3, 'peak_outstanding': 5, 'peak_ready': 3, 'peak_reserved_bytes': 41943040, 'preparation_batches': 3032306, 'prepare_wall_seconds': 41547.48776065849, 'producer_wait_capacity_seconds': 1.9259330461500213, 'producer_wait_full_seconds': 6711.534485135926, 'ready': 2, 'ready_depth_seconds': {'0': 29395.6803522986, '1': 4302.2890913625015, '2': 722.3406899127294, '3': 7146.402005709184}, 'ready_limit': 3, 'reserved_bytes': 25165824}; buffer: {'flush_count': 379038, 'flush_seconds': 2949.2289114679443, 'pending_bytes': 0, 'pending_chunks': 0}.

Journal storage: **local durable journal, verified bulk copy every minute**. New journal cap: **116 GiB**;
free-space reserve: 8 GiB.
Observed rate: **18,675 patches/s**; new independent GMP audits: 23,690.
Deadline: **2026-11-10T17:00:00-06:00**. Independent worker/deadline services on Ada; separate publisher on Ada.
GitHub updates every **15 minutes**, plus startup/terminal transitions. Alerts: None reported.

The fresh trial starts at the exact final parent cursor under a child claim capped at 7,000,000,000. A separate coordinator holds the original parent lease while child searches run.
[Configuration](evidence/configuration.json), [parent audit](evidence/parent-audit.json),
[verified archive](evidence/parent-archive-receipt.json), [source manifest](evidence/source-manifest.json).
Archived receipt integrity was verified; historical coefficients were not recomputed.
Selected interval only. Other hosts' coverage is separate. No completed full-box bound.
