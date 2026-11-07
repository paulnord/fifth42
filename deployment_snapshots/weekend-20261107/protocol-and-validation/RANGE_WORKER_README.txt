Validated stable-inode range-worker prototype (2026-11-07)

Entry point: range_worker.py in this directory. Evaluator: chunk_evaluator.py.
This prototype is separate from the pre-existing bundle/ prototype and does not
modify it. Tests and metadata below refer specifically to range_worker.py.
Nothing here has been launched as production work or installed as a service.

Share: /mnt/diskBox must resolve to NFS export
192.168.5.3:/volume1/clusterData. A missing/wrong mount is rejected before creating
a workspace; no local fallback. pnord and pnord/fifth42 are mode0700. The NAS
reports owner UID1024/GID100 although Boole pnord is UID1330. Permissions are
private by server identity, not necessarily between clients mapped to that same
server identity. Ada needs matching mapping or a deliberate private server ACL.

Grid: cmin=100000000001, cmax=200000000000, width8, cap42, N=11250000001.
Patch i has endpoints 9*i/(10*N),9*(i+1)/(10*N). Reserved patch indices are
half-open [first,last). Mathematical patch boundaries are inclusive in the
original geometry; physical boundary hits may need deduplication across jobs.
A job reserves an explicit, potentially large range, but commits at most256
patches per journal record; a final partial chunk is allowed. There is no default
range and no automatic claim expiration or reassignment.

Environment:
Use a separate Python3.12 environment with requirements.txt exact pins. Boole's
validated interpreter is /home/pnord/boole-results-20261107/venv312/bin/python.
Use ordinary Python; -O is rejected. No system or Ada Python was altered.
Python3.12.16; sympy1.14.0, fpylll0.6.4, cysignals1.12.5, numpy2.3.5,
gmpy2 2.2.2, mpmath1.3.0. Installation/network logs show no errors.
The virtual environment is local to Boole, not a portable shared venv.

Sources and runtime:
source/ is the pinned c36f41a2edd0a1458fdb03b5277b3ec461dea565 archive.
candidate/scaling_core.py has only the archived exact cube-bound patch;
candidate/precision_policy.py chooses outward geometry precision. The evaluator
uses both candidates, the pinned GMP/fpylll initializer and unmodified exact
prepare/certify/assemble/decode/count/overflow checks. Every returned candidate's
residual is independently checked using GMP; accepted hits are reconstructed.
The original native binary stops at100 billion. build/workspace is the separately
validated repository-supported finite200-billion build, including its arithmetic
validation record (272 cases per CPU, sanitized CPU and CUDA backend).
The manifest hashes source/worker code and the actual CPU binary, checked on
every evaluation. runtime-identity.txt hashes runtime-manifest.json canonically.
Do not overwrite an identity that has claims. A rebuild or code/configuration
change requires new identity and new journal linked to reconciled coverage.
Linux x86_64 runtime compatibility must be checked on Ada; rebuilding there would
need a new manifest and the same arithmetic and nonempty controls. No Ada changes
were performed. Current evaluator uses CPU, not a durable GPU worker.

Allocation and running (documentation only; do not launch production yet):
  python range_worker.py --root VERIFIED_TEST_OR_LATER_APPROVED_LEDGER reserve \
    --job UNIQUE_JOB --first EXPLICIT_FIRST --last EXPLICIT_LAST \
    --identity RUNTIME_SHA256 --coverage-file VERIFIED_HANDOFF_METADATA.json
  python range_worker.py --root SAME_LEDGER run --job SAME_JOB \
    --identity SAME_RUNTIME_SHA256 --max-chunks BOUNDED_COUNT -- \
    PINNED_PYTHON /absolute/path/chunk_evaluator.py \
    --manifest /absolute/path/runtime-manifest.json
Each evaluator invocation accepts one chunk JSON on stdin and returns one result.
The prototype intentionally starts a checked evaluator per chunk. This adds
startup and serial-preparation cost; its throughput is not the persistent,
16-worker pipeline benchmark. A persistent production adapter needs additional
validation before adoption. A future production process should be independently
managed outside Codex, as Ada's current search is; no manager/service/publisher
was created here.

Durability:
Every machine must use the SAME reservation ledger. The reservation file remains
a stable inode and is read/written while holding a server-coherent POSIX byte-range
lock. Overlap is rejected independent of candidate identity; adjacent ranges work.
Each job's append-only journal inode is locked for its entire run. It is never
unlinked/replaced. Hashes, immutable claim identity and contiguous chunk bounds
are verified on recovery. Appends are fsynced before atomic checkpoint replacement
and parent directory fsync. The journal is authoritative; a fully verified journal
chunk is rolled forward when a checkpoint write fails. A partial trailing record
is preserved in an orphan file, fsynced, then truncated and recomputed. Invalid
complete records fail closed. The worker does not trust stale checkpoint metadata
or use directory listings to decide reservation conflicts.
SIGTERM/SIGINT finishes the current checked chunk then stops. SIGKILL releases
kernel locks; restart reconstructs committed coverage without duplicate chunks.
Evaluator and native engine have parent-lifetime guards. Changed source identity,
unsafe transforms, incomplete/malformed evaluation or failed storage prevents
advancement. The first ratio-grid patch is an explicit unsupported native-transform
case, not a completed exclusion; no guard is bypassed or hole silently skipped.

Tests:
13 final tests passed on Boole's real NFS test area using pinned Python.
Large adjacent100-million-patch reservations are test-only and not enumerated.
Concurrent overlap, duplicate worker exclusion, SIGKILL/SIGTERM, exact restart,
partial ENOSPC writes, checkpoint EIO, tampering, malformed completion, CLI,
-O rejection, coverage-metadata linking and absent/wrong mount behavior passed.
Exact test chunks use the real candidate certificates, native counts and GMP
checks. Artifacts remain in ../tests-20261107/. Final log:
/home/pnord/boole-results-20261107/worker-tests-final.log.
Earlier test journals have earlier identities and must remain separate.
Coverage metadata is linked by claim hash; this is NOT verification of Ada's
coverage. The metadata fixture used in tests is explicitly synthetic.

Required before distributed production:
1. On Ada, verify the exact NFS mount, export permission/network reachability,
   correct effective NAS identity/ACL, pinned runtime, binary compatibility and
   sufficient CPU/share capacity. Do not remount or alter Ada as part of this test.
2. Run concurrent reservation, same-job lock, post-close visibility and durable
   recovery tests with one process on each actual client. Only Boole processes
   have been tested. Boole currently has1800-second attribute/directory caching;
   do not infer cross-client coherence from same-client tests. Consider a separate
   shorter-cache mount only after administrator review. Server lock/fsync semantics
   are required. A hard NFS outage can block indefinitely; no actual outage was
   induced here. ENOSPC/EIO/missing mount tests were injected, not NAS disruption.
3. When separately authorized, stop Ada cleanly and preserve/hash its final
   checkpoint, journal committed prefix, source identity, covered intervals and
   every gap/guard exclusion. Allocate only the verified remaining intervals.
4. Give the new code a fresh journal and link the verified coverage manifest.
   Never resume the old Ada journal under altered code. No production ranges,
   final Ada checkpoint, or real verified handoff manifest exist in this prototype.
