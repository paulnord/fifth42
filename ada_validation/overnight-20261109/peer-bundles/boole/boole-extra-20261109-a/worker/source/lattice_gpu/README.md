# Prepared CUDA backend for the fifth-power lattice prototype

This is a separate experimental backend for the prototype at
`ddf28f04725b29b2f1d53b5d33c16379b0f66a20`. The existing direct fifth42 GPU search
remains the comparison baseline. No speedup, new completed box, or production
readiness is claimed here. Published handoff results and active jobs are unchanged.

CPU Python keeps exact rational patch construction, lattice reduction and
coverage certificates. CUDA enumerates a conservative coefficient box and
computes exact signed 192-bit fifth-power residuals. Python independently
reconstructs returned points and checks rational patch membership and residuals.
See [coverage and arithmetic bounds](COVERAGE.md).

Code: [host certificates](model.py), [shared integer kernel](src/kernel.hpp),
[CUDA engine](src/enumerate.cu), [CPU emulation](src/emulated.cpp),
[bounded device comparisons](check_devices.py).

Preparation checks are recorded in `PREPARATION.json`. The host mathematical
and guard tests pass, and C++ host syntax passes. The CUDA binary has not been
built or run yet. Host emulation, sanitizer execution and hardware comparisons
are all pending the guarded validator. These checks are separate from the
original published 17-test suite, which has not yet been independently rerun on
ADA while four133 occupies the cores.

When ADA is free, from a normal ADA terminal:

```sh
python3 ~/fifth-lattice-gpu/validate.py
```

The validator refuses busy CPUs, existing search jobs or an inaccessible GPU.
It first requires a passing fresh CPU reproduction with all five expected
outputs deleted and regenerated; it runs the corrected bounded CPU recipe if
needed. Then it freezes the new sources in a unique validation directory,
builds serially at nice 19 with one-CPU affinity, acquires the existing project
GPU leases and checks that the GPU has no compute process. CUDA device 0 is the
only visible device. No production search is launched and no automatic resume
or queue is installed.

Validation includes Python-integer arithmetic comparisons, CPU emulation and
ASan/UBSan, complete small positive domains and target42 signed reductions,
nonempty residual12/residual2951 controls, repeats, zero and negative arithmetic
bases, exact residual boundaries, incomplete/malformed packets, buffer overflow,
the two selected large patches, and bound-1,000 agreement with the freshly
reproduced CPU baseline. GPU timing is limited to 120 seconds summed across
device-program process times; each such process has a 20-second wall cap. The
outer validation has a 600-second cap and yields if production work resumes.
Only its own validation process group is terminated on interruption.

The box enclosure can do more enumeration than the original sphere recursion,
and CPU rational LLL may dominate. Reports separate CPU preparation, engine
process time, kernel time and exact host verification. A future performance
comparison must include the entire pipeline at identical targets and bounds.
Correctness timings from sanitizers or selected fixture patches are not a
demonstration of practical speedup.

For now, full-domain preparation is deliberately capped at bound 1,000. The
two large controls select known fixture patches and exercise >128-bit powers;
they do not extend the completed 70-million direct-search result.
