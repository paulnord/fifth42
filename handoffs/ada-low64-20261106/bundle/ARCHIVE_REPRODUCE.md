# Reproduction and dependency map

## Requirements

The native verification path needs Linux, Python 3, a C++17 compiler with unsigned
128-bit support (the original used g++ 14.2.0), and UBSan. It does not require
CUDA, a GPU, network access, GMP Python packages, or a search checkpoint.

Optional packet generation, sphere tests and host tests additionally need the
packages in `requirements-reproduction.txt`; packaging checks used Python 3.12.14.
Install them in your own isolated environment when desired:

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements-reproduction.txt

No dependencies are installed by the reproduction script. Linux CPU-affinity
support is needed by the original timing/recheck scripts. Fresh timing values
will depend on the machine, load and compiler. Original low-word runs persisted
median/min/max values but not raw timing vectors, so their sampling uncertainty
cannot be reconstructed.

## Integrity and small correctness reproduction

From this archive's root:

    sha256sum -c SHA256SUMS
    python3 reproduce.py native --output ../fifth42-native-recheck

The output must not already exist. The script copies the inputs, rebuilds the
benchmarks and audit, then checks all original packet modes and primitivity
variants against their recorded counts and complete hits. It also reruns the
Python bigint audit, finite congruence checks and nonempty low-word controls.
Evidence in the bundle is never overwritten. A single correctness repetition
is used instead of a new performance campaign. Compiler commands and results
are written to the output's `reproduction.log` and `validation.json`.

## Patch order and exact source provenance

Base commit: `8e34d94dab4b3741392d73bed40ea51c365cc3bd`.

1. Start from `source-provenance/base-source-8e34d94.tar.gz`, or that exact Git
   revision. This is the base, not the later working-tree candidate.
2. Apply `fifth42-coordinator-delivery-20261106/fifth42-coordinator-candidate.patch`.
3. Apply `fifth42-host-ideas-delivery-20261106/fifth42-host-ideas-add-on.patch`.

Both patch checks and applies passed in a clean extracted base during packaging.
The supplied `fifth42-coordinator-20261105/` is exactly that reconstructed source
tree; host-add-on source hashes were checked against its manifest. It is not a
Git clone and contains no `.git` credentials or history. The original source-
and-results tarballs are partial candidate overlays, not standalone repositories.
Do not apply either patch a second time to the supplied reconstructed tree.

The experiment headers are a distinct, private source overlay at
`fifth42-coordinator-overlay/{src,vendor}`. Its `kernel.hpp` changes only the
maximum base from 100000000000 to 200000000000 relative to the base header.
It is already the overlay used in the preserved experiments, not an instruction
to change a production limit. All original per-patch, packet, transform and
arithmetic guards remain. Reproduction builds use this overlay explicitly;
building the unmodified base header would reject the high-range packets.

The standalone sieve harnesses depend on those overlay headers. The independent
audit includes the actual additional-sieve `bench.cpp` with its main renamed.
Its harmless no-return warning comes from renaming main; that function is never
called. The packet scripts additionally depend on the reconstructed Python
source and the original fpylll/GMP versions.

## Rebuild packet certificates and rerun optional tests

After installing the optional dependencies, run each into a fresh directory:

    .venv/bin/python reproduce.py packets --output ../fifth42-packet-recheck
    .venv/bin/python reproduce.py sphere --output ../fifth42-sphere-recheck
    .venv/bin/python reproduce.py host-tests --output ../fifth42-host-recheck

`packets` regenerates all four packets and compares the point counts, geometry,
direct-domain bands, packet hashes and certificate hashes to the originals.
`sphere` runs the original alternating baseline/candidate bounded sphere script,
including the independent exact controls and oracle. `host-tests` runs the
original 107-test discovery suite after building its three required local CPU
binaries with `make` and ASan/UBSan, and explicitly points all tests at the
included frozen prototype. It therefore also needs `make` and ASan.
No Ada or remote command is involved.

To deliberately repeat the original full CPU sieve timing experiment:

    python3 reproduce.py timings --output ../fifth42-timing-recheck

This uses the original seven-repeat gcd and eleven-repeat additional-sieve
scripts, preserves new results in the output copy, and does not rerun packet
preparation. Do not treat timing repetition as additional geometric coverage.

For the host arithmetic/width calibration, first create a host-tests working
copy as above, then build its isolated CPU engine:

    cd ../fifth42-host-recheck
    g++ -O3 -std=c++17 -pthread fifth42-coordinator-overlay/src/scaling_cpu.cpp -o cpu-engine
    PYTHONPATH=/path/to/optional/dependencies python3 fifth42-coordinator-20261105/lattice_gpu/host_optimization_benchmark.py --engine "$PWD/cpu-engine" --output "$PWD/host-arithmetic-new" --workers 4 --repeats 5
    PYTHONPATH=/path/to/optional/dependencies python3 fifth42-coordinator-20261105/lattice_gpu/host_optimization_benchmark.py --engine "$PWD/cpu-engine" --output "$PWD/host-width-new" --workers 4 --repeats 5 --width-sweep

Use your venv's Python instead of PYTHONPATH if dependencies were installed there.
The source path defaults to the included frozen lattice prototype. Outputs must
be fresh. These are optional reproductions of completed controlled calibrations,
not the proposed fixed-time exploration and not a request to repeat them on Ada.

## Evidence preservation

The five original delivery/experiment directories were copied byte-for-byte.
Original checksum files retain their original relative-path convention: the
primitivity and delivery checksum lists are checked within their directories;
the audit list is checked from their common parent. The top-level SHA256SUMS
removes that ambiguity for the complete bundle. Nested older evidence archives
are retained intact. All new packaging checks live under `package-validation/`.

No machine-specific Python wheel installation is bundled. Pinned requirements,
source snapshots, packet/certificate hashes, original machine/compiler metadata,
commands, exact-result oracles and preserved measurements provide the reproducible
inputs. Their local CPU timings are evidence about those bounded experiments,
not a prediction for Ada.
