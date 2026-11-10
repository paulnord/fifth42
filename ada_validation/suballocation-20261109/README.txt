Boole follow-on allocation — 9 November 2026
==========================================

Ada has reserved 4,250,000,001 additional original width-8 cells for Boole:
[7,000,000,000, 11,250,000,001), half-open. The grant contains 67 separate
64,000,000-cell claims (the last is shorter). These are reservations, not
completed coverage. The deadline remains Tuesday, November 10, 5 p.m. Central
(epoch 1794351600); start cleanup at 4:59:50 p.m.

Grant directory:
/mnt/nfs_share/fifth42-shared-20261107/suballocations/ada-boole-20261109-r1

Read GRANT.json, BOOLE_ALLOCATIONS.json and READY.json there. GRANT.json SHA256:
7c8422f5e9086519db3bc8ad2e8eeab8d7d1d60706f9b327766ba0a069c6a389

Ada is already running its retained child claim [4,631,300,224, 7,000,000,000).
The original legacy reservation is unchanged. A separate coordinator holds
its original owner lock continuously; old clients cannot acquire that lease.
The new Ada worker has a hard range_end=7000000000. Its actual GPU prefix,
nonempty controls, GMP audit, child lock, original parent lock and deadline
have been verified. Both real finite and graceful-signal GPU tests passed.
The brief Ada handoff took 72 seconds to service launch. A prelaunch source
check caught a claim-metadata mismatch; the original source artifact stayed
frozen and the new child claim is pinned separately in the configuration.

Instructions for Boole's local agent
----------------------------------

1. Keep the current three-stage queue running. Stage the new work in fresh
   directories using Boole's already tested overnight source and native
   binaries. Do not edit a running frozen directory or any completed journal.
   Keep group_limit=4, dispatch_chunksize=4, 16 physical workers and the same
   grid, arithmetic, certificates, packet checks, controls and GMP cadence.
   The Ada archive supplied here is review evidence; use Boole's own binaries.

2. Use the child ledger above and the exact job/claim hashes from
   BOOLE_ALLOCATIONS.json. Every fresh run starts at that claim's first cell
   and stops at its last. Use allocation_role='boole', suballocation_grant_file
   pointing to GRANT.json, suballocation_grant_sha256 as above, and the unchanged
   deadline. Keep parent_selected_patches=0 for each fresh disjoint claim:
   reservation and parent history do not establish coverage of intervening work.
   Pin each new child-claim proof separately from baseline source artifacts.
   Retain local durable journals, verified NFS replicas and independent final
   copies. These 64-million-cell stages fit the tested 32-GiB journal budget.

3. Include the supplied suballocation_guard.py in each new source manifest.
   Call suballocation_guard.check(config) at admission AND at least every five
   seconds while running. Retain all existing resource/geometry/source/parent
   and child owner-lock checks. The guard requires the pinned grant, live
   heartbeat, held legacy parent lease, independently checked bounded Ada
   prefix, final READY and containment in Boole's assigned interval. Fail
   closed and stop gracefully if any check fails. Do not add overlapping rows
   to the original reservations.jsonl or release/rewrite its Ada reservation.

4. Validate a finite actual-GPU run and graceful stop in the isolated TEST_ONLY
   namespace on Boole before admitting production. Check exact native/GMP
   counts and full near-miss records, nonempty controls, original width-8
   boundaries, child lease exclusion, replica readback, source hashes and the
   absolute deadline. Never reuse a failed or partially completed output.
   Preserve the tested Boole binary identities pinned in GRANT.json.

5. Append the admitted fresh stages to a NEW once-only frozen queue plan.
   Stop ONLY boole-overnight-queue-20261109.service before replacing its
   controller; keep the active compute and independent final copier running.
   Adopt the active stage and retain both already assigned follow-on ranges.
   Enter each new claim only after the preceding stage completes cleanly and
   its final copy is verified. Partial/failed runs require explicit review.
   Do not restart compute merely to change the controller. Do not enter a
   delegated range until grant READY says active_delegation_ready and the
   live guard passes. Unused later claims can remain reserved at the deadline.

6. Publisher admission is prepared on Ada. Use stable collector share
   /mnt/nfs_share/boole-delegated-publishing-20261109.
   For each run_id boole-delegated-20261109-00 (and successive two-digit IDs),
   place evidence under runs/<run_id>/:
     configuration.json, source-manifest.json, parent-audit.json,
     original-claim.json, runtime-validation.json, source.tar.gz.
   Archive members must include worker/<every manifest file> and root member
   production-config.json byte-equal to configuration.json. Hash all evidence.
   After the first verified replica, write active-publication-spec.json last:
   {run_id, config_sha256, manifest_sha256, source_archive_sha256,
    evidence_sha256: {filename: sha256, ...}}.
   Publish the normal identity-bound status.json to that stable share, including
   its publication-spec.json and evidence hashes. The collector's run, source,
   configuration, claim, interval and deadline must match exactly. Ada's relay
   verifies the full source archive, child grant and native/GMP prefix before
   starting the GitHub publisher; check ADA_PUBLISHER_ADMISSION.json and
   ada-publisher-readiness.json. Existing queue collectors keep their paths.

7. Write the new tested source archive, commands, hashes, plan and actual
   start/status evidence under
   /mnt/nfs_share/fifth42-integration-20261109/extend-20261110/boole/delegated-r1/
   with READY.json last. Keep PRODUCTION_STATUS.json current. Ada has no SSH
   login to Boole, so the new claims are reserved and ready for your local
   validation; they are not yet claimed to be queued or running on Boole.

Ada monitoring and graceful stop
-------------------------------
Compute: ada-suballocation-20261109.service
Parent lease: ada-suballocation-parent-20261109.service
Collector: /mnt/nfs_share/ada-suballocation-publishing-20261109/status.json
Protocol state: <grant directory>/coordinator-state.json

To stop the whole delegation early, stop borrower compute first, then Ada
compute, leaving final copiers running; release the parent coordinator only
after every child has stopped. Never stop that coordinator as a way to
reassign live work. Its lease expires after the common deadline cleanup.

Source, exact config, 9 interprocess/resource tests, real GPU probe results,
full old-parent audit, activation proof and verified archive accompany this
handoff. GitHub source commit is recorded separately in GITHUB.json.
