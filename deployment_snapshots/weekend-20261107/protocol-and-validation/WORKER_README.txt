Prepared worker: /mnt/diskBox/pnord/fifth42/worker-20261107/bundle
Private workspace: /mnt/diskBox/pnord/fifth42 (mode 0700; server uid 1024 gid 100).
Only test claims exist, under tests-20261107. No production job was allocated or started.

Grid and coverage
  c in [100000000001,200000000000], cap42, width8, 11250000001 patches.
  Patch i covers exact ratio endpoints 9*i/(10*N),9*(i+1)/(10*N), as in
  overnight_search.shell_specs. Job indices are half-open [first,last).
  Neighboring geometric patches may share their boundary; job index claims do not.
  Reserve a large explicit range; checkpoint every 256 patches (final partial chunk allowed).
  No inherited coverage or full-box conclusion. Claims remain reserved permanently,
  including completed/failed claims; no time-based expiration or automatic takeover.
  New source/configuration requires a new job and deliberately reconciled coverage.
  No old Ada journal is resumed. --predecessor records a verified handoff reference;
  the program does not itself verify Ada coverage. Do that before allocating work.

Portability
  Python 3.12 with requirements.txt pins; Boole used Python 3.12.16.
  No virtualenv copied to share. Install a separate environment on each host.
  Sources, exact lattice package, CPU/CUDA sources, Boole binaries, range-validation
  evidence and SHA256 manifest are bundled. Current worker uses CPU only, conservatively.
  The benchmark's GPU gains do not describe this worker's checkpointed CPU throughput.
  Bundled Linux x86_64 binaries require compatible runtime libraries. Rebuild on an
  incompatible host, repeat arithmetic validation/nonempty controls, and regenerate
  manifest as a NEW identity before any claims. Do not overwrite a claimed bundle.
  Code checks manifest on every launch. Preserve manifest and source snapshots.

Launch shape (documentation only; production not launched):
  pinned-python /path/to/bundle/worker.py --workspace /mnt/diskBox/pnord/fifth42/jobs \
    --job HOST-RANGE-ID --first EXPLICIT_FIRST --last EXPLICIT_LAST \
    --workers 16 --predecessor VERIFIED_COVERAGE_SHA256
  Create the jobs directory mode0700 only after the cross-host gate below.
  Identical invocation resumes. STOP file in job directory or SIGTERM requests stop
  after the current chunk; SIGKILL replays any uncommitted work on restart.
  Run outside Codex via an independently managed terminal/service only when authorized.
  This preparation does not install services or publishers.

Durability and failure behavior
  One POSIX byte-range registry lock serializes claims; each job has a second run
  lock. Lock files are never removed/replaced. claims.json is replaced atomically
  under the registry lock. Use only this allocator for every machine sharing a grid.
  Journal records chain hashes and exact first/last/chunk sequence, source/config,
  point counts, packet/response hashes, certificates, exact hits and stage times.
  Journal append+fsync precedes checkpoint temp+fsync+rename+directory fsync.
  Recovery verifies the committed prefix. An uncommitted suffix is preserved in an
  orphan file, fsynced, then truncated and replayed. Failed exact/range/storage checks
  leave cursor unchanged. Oversized/unsafe transforms halt the chunk; no gap is
  silently counted as complete. The first ratio patch is a known guard exclusion.
  POSIX operations depend on honest NFS server fsync/lock semantics. A hard NFS
  outage can block I/O indefinitely; it does not create a local fallback. Do not
  launch a duplicate job while a host might still hold its job lock.

Before Ada can use the share
  Mount exactly 192.168.5.3:/volume1/clusterData at /mnt/diskBox with NFSv4 locking.
  Verify effective server UID mapping/access: the directory is server uid1024,
  mode0700, sec=sys. Ada needs the same mapped identity or a deliberately configured
  server ACL/group; do not broaden private permissions as an expedient.
  Boole has 1800-second attribute/directory cache settings. Validate concurrent
  claims, byte-range exclusion and checkpoint visibility with processes on BOTH
  machines against this same NFS export before production. Consider a separate
  appropriately configured mount with shorter caching after administrator review;
  do not remount or disrupt an existing client as part of this preparation.
  Confirm enough share space, runtime libraries, pins, and CPU availability on Ada.
  No cross-host lock/cache claim is made from Boole-only tests.
  A later clean stop of Ada must yield final checkpoint plus verified gaps and
  hashes. Link a new optimized journal to that coverage; never resume altered code
  against the old journal. Resolve guarded boundary gaps explicitly.

Tests and limitations
  worker-tests.json/log: real Boole NFS processes test concurrent overlapping and
  adjacent claims, same-job exclusion, graceful and abrupt interruption/restart,
  source/provenance changes, journal corruption, orphan replay, injected storage
  failures and wrong-export rejection. ENOSPC/fsync/rename errors are injected;
  no actual NAS outage or production filesystem manipulation was performed.
  worker-exact.log and the exact-chunk test journal validate one real 256-patch CPU
  chunk in a TEST_ONLY area, including fresh nonempty independent controls.
  No GPU production worker, scheduler, cross-host validation or publisher is installed.
