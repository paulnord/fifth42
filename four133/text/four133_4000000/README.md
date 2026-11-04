# Parallel incremental 133rd-power search: three million to four million

This is a separate authorized stage for four signed integer 133rd powers summing to 42. It preserves the completed, independently audited inclusive three-million result and searches only the shell

    3,000,000 < max absolute base ≤ 4,000,000.

Do not infer a finished result from this README. Full coverage requires completed production logs and the final independent audit.

## Partition

The same three ordinary-base-sum cases are exhaustive at four million: 42, 4,206,972 and -4,206,888. The additional sums still have magnitude greater than the bound, so only their three-versus-one sign patterns need searching. The ordinary-sum interval excludes the next multiples of 4,206,930. See `independent_mathematical_audit.md` for the proof and the prior stage for the conditional sign and convexity arguments.

Per modulus:

- Sum 42: h = 1,...,1,595, split into 2 chunks.
- Positive extra sum: h = 1,...,59,259, split into 58 chunks.
- Negative extra sum: h = 1,...,59,259, split into 58 chunks.

Each chunk contains at most 1,024 consecutive h values. There are **118 chunks per modulus, 236 chunks total**, covering **240,226 per-gap checkpoints** across the two moduli. The division does not change with the number of workers: a bounded queue distributes these distinct chunks dynamically.

Every canonical tuple has a unique largest magnitude d. Only the right pair is restricted to d > 3,000,000; the left list and every h up to the new bound remain available. This is incremental shell coverage, not a full rerun of the old box.

## Worker benchmark

The runtime exposes nine logical CPUs and permits all nine in process affinity. Cgroup quota files are not exposed, so actual throughput was measured rather than assuming dedicated cores.

A fixed 323,802,036-entry workload, separate from production coverage, took:

- 1 worker: 29.73 seconds.
- 2 workers: 15.39 seconds.
- 4 workers: 9.58 seconds.
- 9 workers: 4.01 seconds.

Nine workers gave a measured 7.4-fold speedup and sampled combined search-process RSS of approximately 322 MiB. The selection rule chooses the smallest tested count within 5% of maximum measured throughput; it selected nine. Raw measurements and isolated benchmark logs are in `benchmark/`. They are not adopted as production coverage.

## Running and resuming

```
python run_parallel.py --workers 9
```

The coordinator validates all prior completed chunks and their recorded hashes before dispatch. Each task has one unique modulus/branch/h interval and one unique partial-log filename. Only complete validated chunks are atomically promoted to `.log`; one coordinator writes the progress manifest atomically. It retains successful out-of-order results, including those finishing after a failure or pause request.

A per-run file lock rejects a second coordinator using the same directory. The lock descriptor is inherited by every search process, so killing the coordinator does not release the lock while orphaned engines still write. A restart is blocked until those bounded processes exit; then uncommitted partial files can be safely rerun. The executable is snapshotted by hash inside the run directory.

Worker count can change between restarts without changing the mathematical partition. Configuration, source, driver, binary, previous-bound evidence, or completed-log hash changes are rejected rather than mixed.

To pause after N newly dispatched chunks:

```
python run_parallel.py --workers 9 --max-new-chunks N
```

Creating `runs/STOP` requests a graceful pause: no new tasks start, in-flight tasks finish and are validated, and their results are retained. Remove that marker before resuming. A reported exact solution also stops further dispatch. Worker failure preserves other completed work and returns failure; missing or corrupted completed logs are not silently discarded.

## Small tests and final audit

```
python run_parallel.py --test --run-dir new_test --workers 9 --chunk-size 7 --max-new-chunks 3
python run_parallel.py --test --run-dir new_test --workers 4 --chunk-size 7
python audit_production_counts.py --require-complete
```

Test mode uses small synthetic sums and modulus 97 to create real collisions; it cannot supply production coverage. Independent tests additionally cover all branch tuples, shell boundaries, split ranges, lock contention, out-of-order completion, graceful STOP, failure, exact-solution stopping, changed worker counts, missing/tampered logs, and parent-only hard interruption with surviving children.

The preceding three-million proof, logs and reports are kept separate and frozen. No formal proof-checker installation or setup was changed. No ada, Valpo, or BNL resources were used. The current engine deliberately rejects bounds above four million; future extensions require a fresh analysis of additional ordinary-sum and sign cases.
