# Four 133rd powers: audited result and ADA handoff

This directory is separate from the repository's three-fifth-powers search.
It preserves the full reproduction bundle for
`a^133 + b^133 + c^133 + d^133 = 42` and a plan for a bounded CPU benchmark on ADA.

**Connector-readable files:** start with [text/README.md](text/README.md).
The unpacked [source, proofs, and audit manifests](text/INVENTORY.json) are
ordinary UTF-8 files that can be fetched individually through the GitHub
connector when the archive or direct Git networking is unavailable. This
subset does not include raw production logs, checkpoints, or executables.

## Completed result

No four distinct signed integer bases in **[-4,000,000, 4,000,000]**, inclusive,
satisfy the equation. The audited zero raw modular matches also exclude repeated
bases under the included reductions. This is a finite computational result,
not a global impossibility proof or formal verification of the executable.

The new 3M-to-4M shell completed 236 chunks and 240,226 gap checkpoints, with
zero candidates in both modular passes and 33,596,847,250 filtered pair entries.
Its measured wall time was about 6 minutes 1 second with nine workers; sampled
combined coordinator/search RSS peaked at about 345 MiB. These measurements
were made in the original cloud environment, **not on ADA**. The archive includes
the frozen 3M evidence and its nested 2.1M evidence, source, proof notes, logs,
manifests, independent audits, and scheduler failure/resume tests.

## Integrity and unpacking

The unchanged archive is 5,749,673 bytes. SHA-256:

```text
2cfc019a955a8e5518ff027bf11c8585f0e197b6a9030c4b02dfd5a56ee5a050
```

Run from this directory:

```bash
sha256sum -c SHA256SUMS
python3 verify_bundle.py
mkdir frozen
tar -xzf four133_4000000_reproduction.tar.gz -C frozen
tar -xzf frozen/four133_3000000_reproduction.tar.gz -C frozen
tar -xzf frozen/four133_extension_2100000.tar.gz -C frozen
```

Use a new `frozen` directory. Keep these original bytes unchanged. The verifier
checks the archive, nested archive hashes, and every manifest-listed file without
executing bundled binaries. It verifies integrity, not the mathematical proof.
Read `frozen/four133_4000000/RESULT.txt`, `result.json`,
`independent_mathematical_audit.md`, and `audit_production_report.json` first.
The archived README describes the original run procedure; `RESULT.txt` records
its final outcome. An audit rerun writes its report, so use a disposable copy.

## Rebuild from source on ADA

Use Linux, Python 3, and a C++17 compiler. Rebuild locally rather than assuming
the bundled executable is portable. Start a new working tree without checkpoints:

```bash
mkdir -p work/four133_4000000
cp -a frozen/four133_3000000 frozen/four133_extension work/
cp frozen/four133_4000000/{search133_incremental.cpp,run_parallel.py,benchmark_parallel.py} work/four133_4000000/
(cd work/four133_4000000 && python3 -c 'import run_parallel; print(run_parallel.build())')
```

The build helper records the compiler command and source/binary SHA-256 values.
Do not copy the old 4M `build.json`, `runs/`, or `benchmark/` into this working
directory. **Never reuse old checkpoints after a source, driver, configuration,
or binary change.** Do not relabel old reports with new fingerprints.

## Codex benchmark plan

1. Check ADA is available and confirm the CPU/time budget before using shared
   resources. This handoff does not launch a job or authorize a larger search.
2. Preserve the evidence archive and all fifth42 code/results. Make changes only
   in a separate four133 working directory or worktree.
3. In the working copy, adjust the coordinator's current **nine-worker cap** for
   the approved test counts **1, 8, 16, and 32**. Recheck worker-count changes,
   locking, resume, STOP, failure, and interrupted-parent behavior.
4. Replace the original benchmark's **nine tasks** with the same fixed workload
   split into at least 32 disjoint tasks, preferably several waves. Nine tasks
   cannot measure 16- or 32-worker scaling. Run identical total work at every
   worker count, bounded within the already proved 4M domain; validate every
   task and compare exact checkpoint/pair counts and matches.
5. Rebuild from source and use fresh benchmark/output directories for the new
   fingerprints. Record compiler/flags, source/driver/binary hashes, affinity,
   task list, wall and CPU time, peak combined RSS, and observed concurrency.
   Report repeat timings and speedup over one worker. Benchmark logs confer
   **no additional coverage**. Do not run a new full search merely to benchmark.
6. Stop after reporting the bounded benchmark and correctness checks. A search
   **above 4M requires a new proof of the ordinary-sum/sign cases**, updated
   implementation and independent tests, and separate approval for the run.

ADA's repository records 16 physical cores and 32 logical CPUs, so 32 workers
are a test case, not an assumed improvement. The earlier 1/2/4/9-worker benchmark
measured a 7.4x speedup at nine in its own environment, not a prediction for ADA.

## Repository placement

The dedicated `handoff/four133-4000000` branch adds only this directory and
leaves `main` and all fifth-power files unchanged. The repository's existing
`scripts/check_repository.py` deliberately rejects binaries and files over
256 KiB; it will flag this intentionally preserved 5.75 MB archive. That
checker has not been weakened. Do not merge the branch without deciding how
the repository should retain this evidence bundle.
