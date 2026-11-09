Ada group size 4 — 9 November 2026
================================

This revision continues Ada from original width-8 cell 4,434,273,664 under
the original reservation, after clean stop and independent audit of all
138,400 parent receipts and 1,082 GMP checks. Both final journal copies
match byte for byte (4,809,957,255 bytes). The width-8 grid and the 256-cell
commit intervals are unchanged. Physical groups cover four original cells;
dispatch chunks of four expose sixteen preparation jobs per commit.

Only policy.py changes in the frozen runtime: group_limit=4 and
dispatch_chunksize=4, with unique isolated validation directories. All
arithmetic, certificate checks, GPU code, native binaries, cache, buffering,
replication, and resource/deadline guards retain their tested implementation.
Local durable journals replicate to bulk/NFS every 60 seconds.

Matched comparison
------------------
Five balanced repeats per setting on the identical 32,768 original cells
[4434273664,4434306432), workers=16, cache+8-record durable journal buffer.
Uncontended median end-to-end search times, including preparation, candidate
verification, GPU execution, a GMP sample, durable commits, and final flush:

* Group 2 / dispatch 8: 2.541018 seconds (12,896 cells/sec).
* Group 4 / dispatch 4: 1.547314 seconds (21,177 cells/sec).
* Throughput ratio: 1.6422x (64.2% improvement).

These short matched trials are not a claim about sustained production rate
or other search regions. Startup and subsequent independent journal auditing
are recorded separately and excluded from steady_seconds. Every trial had
identical original-cell coverage, equal candidate sets, complete native visit
counts, an independent GMP sample, and successful journal recovery. Groupings
intentionally change physical task counts, certificate boxes and enumerated
coefficient counts.

selection-results.json records the preliminary balanced comparison while the
parent journal audit was running; holdout-results.json is the clean comparison
after that audit completed. Use the latter for the reported speed ratio.
All twenty timing samples and their commands are retained.

The nonempty four-cell control compares group 2 and group 4 against exhaustive
brute force and GMP, preserving (26,32,34,384) and (39,48,51,2916). The actual
release also runs cache/journal tests, scheduling tests, coordinator tests,
and finite/signal/deadline systemd tests with isolated ledger reservations
and independently checked local and bulk replicas. Read the validation JSON
and logs for completed test outcomes.

Production remains limited to TODAY, 9 November 2026, 5 p.m. Central.
The stop timer begins cleanup at 16:59:50; automatic resume is disabled.
Independent final copying may continue after computation stops.

Boole and Cabbage already use group 4 / dispatch 4 and need no configuration
change for this Ada continuation. Their existing jobs and publishers continue.

Reproduction
------------
Use the existing pinned Python and native toolchain identities in the runtime
manifest. check_nonempty_groups.py verifies the wide nonempty control.
benchmark_groups_holdout.py runs the matched performance experiment. Both
require an idle Ada GPU and the shared benchmark/production leases.
validate_sources.py exercises the exact source snapshot. configure.py and
validate_runtime.py are host- and date-specific launch tools, preserved for
audit; their unique existing output directories must never be reused.

The parent production source and initial buffered optimization evidence are
under ada_validation/buffered-20261109 at parent commit
027cfea7c065f960dc9dfc5513a7622b00137f19. This folder is a fresh continuation.
