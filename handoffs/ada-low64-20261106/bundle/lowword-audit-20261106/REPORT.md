# Independent low-word filter audit

## Result

The proposed unsigned low-64 filter is a correct necessary condition for every canonical candidate whose exact residual lies in [-42,42]. No correctness problem was found for the tested cap-42 or cap-2951 paths. The full exact residual test must remain; this is not an exact residual replacement. No Ada, production engine, checkpoint, or launch setting was changed.

## Proof and domain

Let M=2^64 and r=a^5+b^5-c^5 over mathematical integers. Every operation in `fifthlow` and its residual expression uses `U64`, so C++ unsigned arithmetic computes exactly r mod M, despite intermediate wrap. For cap C=42, every r in [-C,C] maps either to [0,C] or [M-C,M-1]. Thus `u <= cap || u >= -cap` preserves every accepted exact residual, including negative residuals. Target matching to `static_cast<U64>(t)` is likewise necessary for signed targets. Low32 and low16 masking preserve the same implication.

The host packet reader proves each coordinate reconstruction fits signed 64 bits, and shape checks impose 1 <= a <= b < c <= 200000000000 before exponentiation. The conservative bound 3*(200000000000)^5 has 190 bits, below signed I192's 191 magnitude bits. Both the modular and full arithmetic are safe over this domain. This is a positive canonical candidate-domain audit, not a proof that the supplied patches exhaust a full shell.

An actual alias demonstrates why the exact check is necessary: (a,b,c)=(8192,8192,16384) has r=-60*2^64, so low64=0 passes the cap-42 filter although the exact residual is far outside the interval. The experiment correctly rejects it afterward.

Integration must retain the original residual contract. In particular, `kernel.hpp::evaluate` also supports mode=1 with bound 5*c^2. A hard-coded cap-42 prefilter would incorrectly narrow that mode, or any cap other than 42. Apply the corresponding actual cap on mode=0; leave mode=1 unchanged unless separately derived and tested. For cap=0 the existing `lowok` admits every residue because its upper tail starts at zero. This is harmless for correctness but gives no filtering; the unsigned one-comparison form `(u + cap) <= 2*cap` handles cap=0 as well, provided 0 <= cap <= INT64_MAX and the arithmetic remains unsigned.

## Independent validation

- Rebuilt the supplied bench with g++ 14.2.0, C++17, -O3, -Wall, -Wextra.
- Reran all eight persisted packet/mode combinations with one timing repetition for correctness only. All point counts, shape counts, exact-test counts, complete hit records, and cross-variant equality results matched the original files.
- Built a separate UBSan harness that includes the actual `fifthlow`, `lowok`, and `test<0>/<1>` functions, without changing their sources.
- Checked 100,008 canonical triples against independently computed Python arbitrary-precision residual words and interval acceptance. Included maximum-base boundaries, the negative cap-42 hit (1,1,2) with residual -30, positive residual 12, and the genuine modular alias above.
- Passed 18,228 predicate/boundary and targeted-control checks, including every residual in [-C,C] for C=0,1,42,2951 and bits=16,32,64, plus signed +/-42 boundaries and all four known target controls, including (2,2,4) with residual -960.
- All executed UBSan checks passed. The harness compilation has a harmless warning because the included benchmark main is renamed and its implicit-main return is no longer special; that renamed function is never invoked.

Files: `audit.cpp`, `run_audit.py`, `audit.json`, `recheck_packets.py`, `packet-recheck.json` in this directory. The initial attempt to use Boost multiprecision could not compile because its headers are absent; Python integers supplied the independent oracle instead. No dependency installation was needed.

## Evidence and benchmark limits

The timing design is reasonable for a bounded CPU screening comparison: identical task inputs, common decode and canonical-shape checks, one pinned CPU, warm-up, 11 order-rotated repetitions, output-dependent checksum, full set equality checked outside timing. Exact arithmetic remains in every variant. Timings exclude packet generation, certification, transfer, orchestration, and result processing. Raw per-repetition timing vectors were not persisted, so uncertainty cannot be reconstructed from medians/min/max alone.

Original interval medians (baseline -> low64) were:

- small1000: 34.751 ms -> 29.390 ms, 15.43% lower time (1.182x).
- high8: 5.893 ms -> 4.217 ms, 28.44% lower time (1.397x).
- high32: 57.335 ms -> 39.808 ms, 30.57% lower time (1.440x).
- controls100: 4.154 ms -> 3.747 ms, 9.80% lower time (1.109x).

These are screening-loop CPU results, not end-to-end or GPU measurements. The audit rerun is a correctness reproduction, not a new performance claim. Low32's similar timings mean this evidence does not establish low64 as intrinsically faster than low32, though low64 has the strongest residue rejection among them.

The small1000 packet omits direct c=1..3 work. Its two interval hit records are two patch records for the single distinct triple (13,16,17), residual 12. The direct-domain negative hit (1,1,2), residual -30, is absent from that packet but covered by the independent audit. The controls100 packet also omits direct c<=7, so its target records do not include (2,2,4), residual -960; the independent control audit adds it. Do not interpret packet hit counts as complete distinct global hit counts. High8 and high32 cover the same selected a/c interval near 0.3 with c in [100000000001,200000000000], not a complete high shell.

## GPU interpretation

The candidate deserves an isolated CUDA A/B test, not immediate promotion based on these timings. On Ada, unsigned 64-bit multiplication costs, compiler instruction selection, surviving lanes per warp, branch behavior, register allocation, and occupancy can change the outcome. A low64 gate uses three modular multiplies per fifth power and can avoid most multi-limb work, but it adds work on candidates that do survive. Inspect compiled CUDA resource/instruction reports and benchmark the same certified packets with warmed-up kernels, identical launch configurations and output capacity, complete point accounting, and exact hit-set parity. Measure both kernel time and end-to-end wall time. No CUDA compiler or NVIDIA management utility was available in this audit environment, and no GPU run was attempted.
