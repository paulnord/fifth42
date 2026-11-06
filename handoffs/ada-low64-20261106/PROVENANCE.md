# Publication provenance and limits

Source archives were read from the user's saved handoff files and verified:

- fifth42-ada-morning-test-handoff-20261106.tar.gz
  SHA-256 a8e26d9a169b1ce15df5dc3b7668b95f1af51a2895e013ebc736d68733a75965
  All 19 original manifest entries matched.
- fifth42-sieve-findings-and-reproduction-20261106.tar.gz
  SHA-256 49fffe13be7d569c54164be0850d5d13107dfd1646cb2aaacd9fb75d0a575075
  All 788 original manifest entries matched.

SOURCE_MAP.tsv maps each preserved file to its archive member and SHA-256.
The original full findings checksum list is preserved in ordered plain-text
parts under provenance/. New README files and checksum lists describe this
curated layout. Executable source, fixed packets and historical results were
not rewritten. Original nested checksums are explicitly renamed ARCHIVE_*.

This publication is separate from deployment. It does not change main, older
handoff branches, Ada files, services, checkpoints, leases or search coverage.
It contains no binaries, tarball dependency or required manual file transfer.
Every published text file is kept below 65,000 bytes for bounded connector
reads; this is a conservative packaging target, not a claimed connector limit.

CPU timings are historical bounded experiments, not GPU/end-to-end speedups.
The low64 CUDA candidate is not GPU-validated. Host/batch CUDA adapters and an
integrated distinct-coverage executor remain unimplemented. See the main README.
