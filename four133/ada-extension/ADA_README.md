# Eight-hour four133 extension on ADA

This separate workspace extends the verified box |base| <= 4,000,000 for
`a^133+b^133+c^133+d^133=42`. Repeated bases are retained. The archived search,
its binaries, raw logs, and checkpoints remain unchanged in
`../four133-handoff/frozen`.

The generalized engine enumerates every permitted ordinary sum and both
remaining normalized sign patterns. See `PROOF.md`. Raising the archived
engine's numeric bound alone would omit additional two-positive cases.

Run, from a **normal ADA terminal**:

```sh
python3 ~/four133-eight-hour/run.py launch
```

The launcher checks current tests and calibration, reruns the old archive's
raw-log audits in disposable copies, freezes all required code into a new job
directory, and starts a detached coordinator. It uses 16 CPU workers and no
GPU. It refuses a duplicate launch. The hard budget is eight hours from the
coordinator's first start; resume never resets that budget. Dispatch stops
20 seconds early to leave cleanup time. Completion or an exact candidate can
stop the job earlier.

Inspect status:

```sh
python3 ~/four133-eight-hour/run.py status
```

The latest job path is recorded in `jobs/latest.json`. To stop, create `STOP`
inside that job directory. To resume after an interruption, remove that file
and run `python3 JOB/code/run.py coordinate --job JOB` in a normal terminal.
Use the frozen coordinator from that job, preserving its original budget.

Every completed chunk is independently checked for its configuration,
contiguous gap coverage, expected residue-progression counts, modular
candidates, and arbitrary-precision exact residuals. Chunk logs and receipts
are committed atomically. Interrupted partial logs are preserved. Source
fingerprints and completed-log hashes are checked on resume. Worker processes
die if the coordinator is killed. A global file lock prevents concurrent
coordinators from this workspace.

`progress.json` reports elapsed time, completed gap cases, pair counts,
candidate counts, CPU time, and sampled combined worker RSS. Partial coverage
does not establish a larger full box. A full-box result requires every planned
case and both moduli to complete and reconcile with the verified prior box.

The test controls are modular collisions; they are **not solutions to 42**.
`validation.json`, `baseline-validation.json`, and `runner-validation.json`
record the independent oracle, sanitizer, archived-engine comparison, and
coordinator tests. `prior-verification.json` records fresh audits of all three
archived production stages. Calibration logs are bounded experiments, separate
from production evidence. Runtime logs and binaries must not be pushed to Git.

ADA: AMD Ryzen 9 5950X, 16 physical cores / 32 hardware threads, 121.44 GiB
OS-visible RAM (130,392,805,376 bytes). Earlier identical-window measurements
favored 16 workers over 32. The final bound and timing estimate are in
`plan.json`; the estimate is not a promise of full-box completion by the cap.
