# Exactness and coverage

The possible signed representatives of fifth-power residues modulo 11 are
-1,0,1. Three of these sum to an integer in [-3,3]. Congruence to 42=-2 modulo
11 therefore requires exactly (-1,-1,0), in some order. There is exactly one
multiple of 11. Naming it z and ordering the other two values loses no solution.

Fifth powers are strictly increasing on integers. At each fixed z, if the
smallest/largest remaining pair sum is too small, every pair using that smaller
endpoint is too small; advance it. If too large, every pair using that larger
endpoint is too large; retreat it. At equality, each endpoint has only that
partner, so record and move both. Include i==j to retain repeated variables.
The argument uses exact order and applies to negative integers as well.

In the baseline workspace, at B<=35,000,000 all powers, pair sums and residual
targets fit signed 128 bits.
The sufficient inequality is `3*B^5 + 2^63 < 2^127`. Targets are restricted to
signed 64-bit inputs. The modulo filter is accepted only when target=9 modulo
11; `--filter none` is available for general-target test cases. The separate
[extension](../extended/README.md) uses exact signed 192-bit arithmetic and
completed the full B=70,000,000 box with no solutions.

The sorted pair-value list has approximately 10B/11 entries and there are
approximately 2B/11 z rows. The baseline takes at most their product, roughly
20B^2/121 comparisons, and O(B) table memory. It does not allocate a quadratic
pair-sum table. Proof of a finite box does not imply a theorem for all integers.

Raw local runs store a covered prefix [0,next_row) of the canonical z-row space.
Only next_row==total_rows establishes full-box coverage. Output-buffer overflow,
CUDA errors, invalid metadata or failed Python candidate verification reject
the whole chunk. Atomic rename and fsync commit coverage only after success.
SIGINT, SIGTERM and budget interruption terminate the engine and retain the last
committed prefix. Changed-machine/source/binary resumption is rejected.

GPU setup and every operation needed for the result are checked. The baseline
assigns one GPU thread to each z row. Checkpoints preserve configuration,
source/binary hashes, counts, timings and candidates, not just a next-index marker.
These files remain local and ignored because an old partial run needs its exact
original binaries and source to resume.

Before a long or substantial shared-resource run, obtain approval for the
specific bounds, time and resource use. Use a finite budget and do not silently
continue when it expires. The completed 35-million search used a 3,540-second
runner budget and a 3,600-second outer timeout with a 10-second termination grace.
It finished before either limit. The subsequent 70-million extension run used
a 28,740-second runner budget and an approved 28,800-second outer cap; it
completed in 11,738.294699 seconds total elapsed time. See
[coverage and timings](../COVERAGE.md). No new search was started for this update.
