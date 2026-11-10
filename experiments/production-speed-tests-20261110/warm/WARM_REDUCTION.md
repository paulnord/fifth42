# Neighboring reduction seed experiment

This test preserves the exact lattice, but a different reduced basis can change
coefficient bounds and enumeration cost. A faster LLL call alone is not a pipeline
speedup. It is not enabled in production.

`warm_reduction.py` wraps the original reducer: for original row basis A and
previous unimodular transform S, reduce S*A to B=V*S*A and certify U=V*S against A.
Malformed/oversized seeds or failed warm certificates fall back to a fresh cold
reduction, which must pass its own certificate. The seed is local to one serial
stream; multiprocessing would maintain separate per-process streams. Reset when
changing region/backend. The caller must still apply all production coefficient,
int64, sphere fallback and exact enumeration guards. No transforms or native
packets may be assumed byte-identical to a cold run.

## Tests and benchmark

Set `LATTICE_SOURCE` to the pinned archive's
`lattice_prototype/compiled_experiment/lattice5_snapshot.py`, then:

```
python -m unittest -v test_warm_reduction.py
python benchmark_warm_reduction.py --source "$LATTICE_SOURCE" --precision-policy PATH/precision_policy.py --output NEW_RESULT.json
```

The benchmark requires the production pinned `gmpy2==2.2.2` and `fpylll==0.6.4`.
It creates the exact current grouped-width4 shell geometry for three regions,
uses production adaptive precision, alternates cold/warm order, and separately
records geometry, reduction time and coefficient volumes. It includes the warm
seed multiplication and certificate overhead. Output files must be new (no
overwrite). Defaults: 16 adjacent physical patches × three regions × three
repeats. Bounded maximum is 256 patches × ten repeats. No native engine, NFS,
ledger, service, publication, or production files are touched.

Six unit tests passed locally: exact row-transform certificates, reduced-basis
conditions, complete sphere point-set equality on small patches, reset,
malformed/oversized seed fallback, wrong candidate fallback and failed cold
certificate rejection (some categories share one test).

## Local exploratory result (not Cabbage)

`local-result.json` records all 18 measurements in the cloud CPU environment.
Means of reduction time per16 physical patches:

| First original cell | Cold | Warm | Cold/Warm coefficient-box points |
|---|---:|---:|---:|
| 0 | 7.19ms | 9.57ms | 701818938555156 / same |
| 3750000000 | 5.60ms | 7.18ms | 1494150 /1497648 |
| 7192000000 | 5.14ms | 8.45ms | 10868914 /10889454 |

The near-zero region's huge coefficient allowance would trigger production
fallback; it is a stress case, not a native throughput claim. These short local
measurements **do not support deploying the warm start**. At the other two
regions it was slower and slightly increased enumeration work. This result
helps prioritize larger improvements rather than assuming this idea must help.
To revisit, profile LLL against common-scaling/matrix construction, test longer
matched runs on the target host, and retain exact full-pipeline coverage checks.
