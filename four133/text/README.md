# Connector-readable source and evidence

This is an unchanged text subset of the preserved reproduction archive. Read
files individually using the GitHub connector on branch
`handoff/four133-4000000`, with paths beginning `four133/text/`.
Preserve the relative paths below when materializing files on ADA; no direct
Git networking or archive download is required for source inspection.

## Start here

- [4M result](four133_4000000/RESULT.txt) and [machine-readable summary](four133_4000000/result.json).
- [4M proof notes](four133_4000000/independent_mathematical_audit.md), [3M proof](four133_3000000/independent_extended_proof.md), and [2.1M proof](four133_extension/independent_proof.md).
- [Search engine](four133_4000000/search133_incremental.cpp), [parallel coordinator](four133_4000000/run_parallel.py), and [bounded benchmark runner](four133_4000000/benchmark_parallel.py).
- [4M independent audit code](four133_4000000/audit_production_counts.py), [completed report](four133_4000000/audit_production_report.json), and [original full-archive manifest](four133_4000000/manifest.json).
- [3M audit report](four133_3000000/audit_production_report.json), [3M manifest](four133_3000000/manifest.json), and [2.1M manifest](four133_extension/manifest.json).
- [Scheduler audit tests](four133_4000000/audit_parallel/patched/audit.py), [failure/interruption scenarios](four133_4000000/audit_parallel/patched/scenarios.py), and their sibling `fixture/` source files.
- [Original benchmark measurements](four133_4000000/benchmark/results.json).
- [Inventory of every mirrored file and its SHA-256](INVENTORY.json).

The three stage directories remain siblings, matching the archived code's
relative paths. Every inventory-listed file is byte-for-byte identical to its
archive member. All new files are UTF-8 text below 256 KiB. The original bundle
and its checksum remain unchanged one directory above.

## What this subset can and cannot do

The sources, proof notes, saved audit reports, original manifests, and benchmark
plan can be inspected without the archive. The original stage manifests list
the **full archive contents**, including files omitted here; `INVENTORY.json`
describes this text subset. A manifest alone does not reproduce its raw logs.

Raw production logs, completed run checkpoints, bundled executables, nested
archives, and most generated test logs/state are deliberately omitted. Full
production-log audits and prior-evidence validation need the complete archive.
Do not weaken those checks to make the subset look like a completed run.
Never adopt the saved summaries as fresh coverage or resume old checkpoints
under different source/driver/binary fingerprints.

## Rebuild and bounded benchmark handoff

Materialize required inventory-listed files with their relative paths, then
work in a separate writable copy. Rebuild locally before running anything:

```bash
cd four133_4000000
python3 -c 'import run_parallel; print(run_parallel.build())'
python3 run_parallel.py --test --run-dir fresh-small-test --workers 1 --chunk-size 7
```

The small test uses a synthetic domain and confers no production coverage.
No prebuilt executable is supplied here. `build.json` is historical provenance;
the missing executable causes the helper to compile and record a new build.
Audit scripts can create files, so run them only in disposable copies.

For ADA's planned **1/8/16/32-worker** comparison, use the plan in
[the handoff README](../README.md#codex-benchmark-plan). The original coordinator
caps workers at **nine**, and the original benchmark has only **nine tasks**.
Adjust both in the working copy, use enough disjoint tasks to occupy 32 workers,
hold total work fixed, record fingerprints and timings, and use fresh outputs.
The benchmark imports the sibling 3M audit report, so materialize that report
as well. Keep benchmark work inside the already proved 4M domain.

No job was started on ADA for this publication. Confirm shared-resource use
before a benchmark. Stop after the bounded benchmark report; a larger search
needs new ordinary-sum/sign-case proofs, independent tests, and separate approval.
