# Packaging verification

All checks below passed on the clean-copy reproduction paths supplied in this
archive. These runs validate reproduction and exact results, not fresh speedup
claims. Original performance evidence is retained separately and unchanged.

- Both patches applied in order to the archived base commit, and every host
  add-on manifest source hash matched.
- All 73 original experiment/delivery files matched byte-for-byte.
- Fresh native builds: all eight additional-sieve packet/mode cases and eight
  basic/cached gcd packet cases matched original exact counts and complete hits.
- UBSan rebuilt audit: 100,008 Python-bigint triples and 18,228 boundary/control
  tests passed. Original low-word controls and target-aware gcd sanitizer controls
  passed, including nonprimitive and modular-alias cases.
- All four regenerated packet hashes and certificate hashes matched, along with
  geometry counts and omitted direct bands.
- The bounded sphere script passed its eight configurations, nonempty controls,
  B=1000 independent oracle, and 13,720 signed/zero unimodular gcd cases.
- The host suite rebuilt its native dependencies and passed all 107 tests,
  including CPU and ASan/UBSan nonempty controls.

An initial packaging-only host-suite attempt exposed two missing reproduction
setup steps: building the test executables and setting the frozen source path.
The wrapper now performs both. No original experiment source was changed; the
complete corrected run is `host-tests-reproduction.log`.

The single-repeat native reruns are correctness checks. Sphere timings are
incidental outputs of the original test harness and are not a new performance
conclusion. The full timing mode and host repeated calibrations were not rerun
while packaging. No CUDA or Ada test was attempted.
