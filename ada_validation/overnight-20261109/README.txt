Overnight continuation — authorized through 10 November 2026, 5 p.m. Central
===========================================================================

Ada resumed at original width-8 cell 4564955776 under its inherited reservation.
Sixteen physical workers, group_limit=4, dispatch_chunksize=4, saved-root and
exact host optimizations, low64 GPU filtering, canonical task cache, eight-record
durable journal buffer and periodic verified bulk/NFS copies are retained.
Arithmetic, certificates, native limits and native binaries are unchanged.

Ada source changes: ReadyQueue consumes a bounded iterator instead of allocating
metadata for every remaining future window. This removed the roughly 6 GiB
whole-range list, the long startup and the shutdown teardown that exceeded the
supervisor grace period. The live main worker RSS was approximately 57 MiB after
restart. Reservation lookup now retries only transient Busy errors for at most
five seconds; digest, claim identity, ownership, range and filesystem failures
remain hard errors. All old sources, configurations and journals remain intact.

The new immutable deadline is 2026-11-10T17:00:00-06:00 (epoch 1794351600).
The independent stop timer and relative runtime limit begin shutdown at 16:59:50.
Independent final copying/reporting may continue through 17:30. Automatic crash
resume remains disabled. Ada has a 120 GiB journal budget and 8 GiB free-space
reserve, checked against available local NVMe capacity before launch; storage or
resource guards can stop computation earlier. Boole and Cabbage retain their
own validated storage/rotation controls and reservations.

Validation: full read-only parent audit checked all 510477 committed receipts,
3989 GMP samples and 9396612899 raw journal bytes. Full local and replica SHA256
and checkpoints matched. Source validation passed buffering, seven scheduling,
four real POSIX claim-retry/corruption tests and the existing coordinator suite.
New lazy-source tests cover bounded consumption of a huge iterator and a partial
final batch. Actual finite and full-production-range signal-stop systemd tests
passed, with nonempty GPU/GMP/brute controls, exact local/replica prefix audits,
final-copy completion, released leases and output reuse rejection.

The launcher/supervisor code is byte-identical to the prior revision whose actual
independent deadline trigger and RuntimeMax cutoff were verified. That evidence
is copied under evidence/previous-deadline-regression.json. The extended UTC stop
command was checked and its live timer was read back. We did not repeat a long
GPU deadline trial merely for the calendar extension. Current runtime evidence
states that reuse explicitly.

Peer restarts were already active when Ada inspected their fresh handoffs. Their
source archives were fully read back and every member checksum verified; both
now have verified Ada-owned GitHub publishers. The read-only relay admits each
stage against its exact configuration, source/native snapshot, signed disjoint
reservation, parent archive/audit, nonempty controls and full captured receipt
prefix. Each stage receives an immutable publication binding; old terminal
publication finishes before a newer stage publishes to the same public path.
Two real-replica relay regression cases check final coverage and rejection of an
incorrect source identity. Publisher readback uses a fresh empty Git repository.

Peer source snapshots and tested controller plans are included under peer-bundles.
They are preserved as host-specific snapshots, not merged over Ada's worker.
Boole's frozen three-stage queue includes 679596928 cells from its restart cursor;
it may finish before the cutoff and stops safely after assigned work. Its request
for additional coordinated allocation is preserved in its controller files.
Cabbage has its original continuation plus an additional 1.75 billion-cell
reservation and explicit validated rotation. Neither node may consume another
owner's reservation. Allocation capacity is separate from completed coverage.

All three currently use group four. Ada's isolated 4/8/16 comparison at commit
ea26749e591ee02cd3abb9579255faf03c6080ae favored four for Ada's region; group eight
was promising in a Cabbage-region replay on Ada but has no measured Cabbage-host
speedup yet. The running peers are retained while that independent experiment
remains pending. Cabbage hardware reported by the user: Ryzen 9 5950X, 16 physical
cores/32 threads, 125 GiB RAM, RTX 3060 12 GiB, driver 595.99.02.

Source baseline: Ada group4 manifest fb76f545da6946f0d57ab065b6b3b146117353d35e6068d081bb3a74c1baa89a.
Current Ada manifest: 5b6582e2f47656993faf01f06b856e513816381a594e6c859eeac08e3cf16f71.
Current Ada config: 60bfa0655a13307e9ac738d867d1c3e46cfe74d10ba4d72c6f9699f5c63d4b0b.
Only explicitly committed selected intervals are coverage. No completed full-box
bound is claimed. See current production snapshots and each peer controller for
range and terminal conditions.
