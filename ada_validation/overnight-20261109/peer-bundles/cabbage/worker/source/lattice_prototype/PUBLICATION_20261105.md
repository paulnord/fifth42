# Optimization package publication, 2026-11-05

Repository: https://github.com/paulnord/fifth42 (public at publication).
Branch: `handoff/fifth-lattice-optimizations-20261105`.
Parent commit: `ddf28f04725b29b2f1d53b5d33c16379b0f66a20` on
`handoff/fifth-lattice-prototype`.
The parent's main baseline is `853fd98fc91968987fcb3e9e4c43b4fe880c8246`.

This is an isolated text-only handoff for a later ADA session. Only
`lattice_prototype/` changes. Main, the existing handoff branch, production
sources, and running ADA jobs are not modified. No production search or GPU
workload is launched. This publication adds no CI workflow or deployment.

## Exact source provenance

Input: `fifth_lattice_adaptation_20261105.zip`, 142655 bytes.
SHA-256: `691015eec96ff55b7e42e4c3c6cb24d7e7d0abaa7b996d42b7b6949356981dd1`.

All 96 input files, including source, tests, dependency pins, licenses,
historical documents, raw `results/`, and the original `SHA256SUMS`, are
preserved byte-for-byte. No archives, compiled binaries, caches, binary
profiles, or third-party wheels are committed. The seven frozen upstream
source identities remain in `vendor/SOURCES.json`.

New files are the current `ADA_OPTIMIZATION_HANDOFF.md`, this publication
note, `publication_validation/` cloud revalidation evidence, and
`PACKAGE_SHA256SUMS`. The package manifest covers every file except itself;
the original manifest continues to cover exactly the original package.
All three checksum commands are run from `lattice_prototype/`:

```sh
sha256sum -c PACKAGE_SHA256SUMS
sha256sum -c SHA256SUMS
sha256sum -c compiled_experiment/SHA256SUMS
```

The historical `PUBLICATION.md` describes the earlier branch and mistakenly
labels the repository private. Current repository visibility is public. Its
bytes are retained as source history, not current access guidance. Other
historical statements that this adaptation was unpublished apply to the
original archive creation, before this publication.

## Validation and interpretation

See `publication_validation/SUMMARY.md` for the commands and results of this
publication's fresh checks, performed in a separate cloud scratch copy. They
do not establish ADA timing or production readiness. Earlier cloud benchmark
data is unchanged under `results/`; it is not relabeled as current or ADA data.

Reference behavior is unchanged. All optimizations remain explicit opt-ins.
Licensing constraints, native-call watchdog limits, complete finite-domain
coverage versus fixture-selected patches, and CPU emulation versus GPU
execution remain documented. Start with `ADA_OPTIMIZATION_HANDOFF.md`.
