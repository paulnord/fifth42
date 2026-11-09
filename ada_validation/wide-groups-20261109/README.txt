Wide group comparison — 9 November 2026
======================================

Completed TEST_ONLY benchmark on Ada after production had stopped at its scheduled 5 p.m. Central cutoff. Production was not restarted. The 27 timed trials plus preflight and nonempty controls finished in 98.12 seconds under a 180-second budget.

All trials use 16 physical preparation workers, the unchanged original width-8 fine grid, 256-cell commits, immutable canonical-task cache, 8-record durable journal buffering, unchanged native GPU/GMP binaries and unchanged point/arithmetic guards. Only the allowed experiment grouping values in width_coverage.py and buffered_pipeline.py change. Dispatch sizes are 4, 2 and 1 for requested groups 4, 8 and 16, exposing sixteen initial preparation jobs per original window.

Measured medians (original cells per second)
-------------------------------------------
Region | group 4 | group 8 | group 16
ada | 20521.3 | 20023.4 | 8782.9
cabbage | 23880.1 | 35094.9 | 30243.9
dense | 6721.0 | 6704.1 | 6632.2

Each region has the same 32,768 original cells for all configurations; three balanced repeats per configuration. Detailed commands and every raw sample are in results.json and logs/. All trials passed exact original-cell span auditing, complete native visits, candidate-set comparisons across groups, a first-chunk independent GMP audit, durable checkpoint checks and recovery. The nonempty shell control matches exhaustive brute force and GMP for all requested groups.

Cabbage and dense are names for replayed SEARCH REGIONS. Every measurement in this bundle ran on ADA HARDWARE, not on Cabbage or Boole. Cabbage-region replay starts at its observed final cursor 2572492928; Ada replay starts at 4564955776; dense starts at 9562500096.

Interpretation
--------------
Keep group 4 for the tested Ada region: group 8 was 2.4% slower, group 16 57.2% slower. In the Cabbage-region replay group 8 was 47.0% faster than group 4 and group 16 26.6% faster. Cabbage needs its own host comparison before selecting group 8. Dense-region native point limits split both larger requested groups back to actual groups of four, preserving coverage but providing no measured benefit.

Timing includes fresh preparation, checked cache consumption, native GPU requests, exact candidate checks, one GMP audit per 128 original 256-cell chunks, durable local journals and final flush. Process startup and subsequent independent receipt audit/recovery are recorded separately. GPU kernel time is a component of the pipeline, not total elapsed time. Wider groups increase independent GMP audit work as well as GPU enumeration; audited pipeline timings retain that cost.

Limitations
-----------
Three short repeats and one window per region establish a useful screening result, not a global optimum. No CPU-only backend comparison or GPU geometry port was performed. No end-to-end improvement is claimed for Cabbage hardware until it runs the matched comparison. All original mathematical/native memory and point limits remain in force.

Production end-of-run findings
------------------------------
The worker on Ada wrote its final clean terminal checkpoint and the final-copy service verified the full local/bulk prefix, but the supervisor recorded Worker exceeded graceful stop allowance during cleanup. Boole reported an NFS reservations lock Busy error; its replica reached its reported local cursor. Cabbage reported a normal stop. Exact observed status snapshots are in production-stop-status.json. These are separate from the successful TEST_ONLY experiment and require follow-up before the next production launch.
