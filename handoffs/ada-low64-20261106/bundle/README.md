# Text-only reproduction inputs

This is a curated, unpacked projection of the 6 November 2026 findings bundle.
Start with ../README.md for the GitHub layout and safe Ada procedure.

All included source, packets and historical result files are byte-for-byte
copies from the verified archives. The reconstructed lattice_gpu and
lattice_prototype source trees, tests, six overlay files, four frozen packets,
native sieve/audit harnesses and selected reports are present. No patches need
to be reapplied. The source and data are intended for scratch validation only.

Use this directory's SHA256SUMS for the curated inputs. ARCHIVE_* checksum
lists describe the original larger archives and are historical, not checksums
to run against this subset. Old documentation may refer to omitted files.

Omitted: prebuilt binaries, nested tarballs, large generated task JSON, repeated
historical timing data and unrelated source trees. Packet regeneration produces
fresh task JSON when needed. The existing reproduce.py native and host-tests
entry points use rebuilt binaries and the included inputs. Other reproduction
modes retain their original dependency requirements; none authorize an Ada run.

ARCHIVE_README.md and ARCHIVE_REPRODUCE.md preserve original findings and
provenance. The base tarball and two older patch files mentioned there are not
needed because the reconstructed required source is already included here.
