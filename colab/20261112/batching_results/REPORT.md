# Fifth42: Colab CPU batching results

The L4 run passed all checks. At eight preparation workers, batching four or eight
original windows improved local pipeline throughput by approximately **10–11%**
over the matched one-window baseline. **Map chunk size 8 beat 32 at every window
batch size.**

| CPU preparation batch | Map chunk | Median pipeline, three passes | Throughput vs baseline |
| ---: | ---: | ---: | ---: |
| 1 window | 8 | 1.821 s | 1.000x |
| 2 windows | 8 | 1.774 s | 1.027x |
| 4 windows | 8 | 1.652 s | 1.103x |
| 8 windows | 8 | 1.644 s | 1.108x |
| 1 window | 32 | 2.177 s | 0.837x |
| 2 windows | 32 | 1.841 s | 0.989x |
| 4 windows | 32 | 1.780 s | 1.023x |
| 8 windows | 32 | 1.699 s | 1.072x |

There were three randomized repetitions of each policy, 24 trials in total. Every
trial replayed the same nine unique windows three times: 27 window visits, 69
unchanged native requests, 6,912 logical-cell visits and 2,327,061,582 coefficient
positions. These are repeated visits, with zero new scientific search coverage.

## Choice for further Colab tests

Use **eight workers, four windows per preparation batch, and map chunks of 8** as
a conservative follow-up baseline. Eight-window batches had the fastest median,
but were only **0.48% ahead of four**, and the three-sample ranges overlap.
The largest measured serialized prepared payload was 3.66 MiB for four windows
versus 7.31 MiB for eight. These are payload measurements, not resident-RAM figures.
A sustained comparison is needed to establish a robust optimum.

The eight-window/chunk-8 policy improved throughput by 10.78% and reduced median
time by 9.73%. The four-window/chunk-8 policy improved throughput by 10.25%.
Production retains its existing multicore and preparation-batch configuration;
these Colab measurements establish no production speedup or reason to change it.

## Why this helps

Grouping four windows reduced CPU map round trips from 27 to 7 per trial; eight
windows required 4. All policies still submitted 3,456 original segment arguments
and executed the same 69 native requests. No coefficient positions, original
windows or exact checks were dropped.

With four-window/chunk-8 batching, median consumer waiting for preparation fell
from 1.158 s to 0.941 s. Kernel execution stayed approximately 53 ms across all
policies, while parent consistency checks and local writes remained material.
These stage timings overlap and are not additive or GPU utilization measurements.

A structural reason to avoid chunk 32 with single-window preparation is that each
window has 128 original segments: chunk size 32 creates only four pool work chunks
for eight available workers. This is an inference from the dispatch structure,
not a measured per-core utilization trace. Larger batches supply enough chunks,
but chunk 32 still lost to chunk 8 in this supplied sample.

The frozen scheduler also uses different ready-buffer units for single versus
multiwindow preparation, so these are complete dispatch-policy comparisons.
Map wall time includes arithmetic, IPC and deserialization; it does not isolate
serialization cost. The benchmark includes additional comparisons with the saved
packet/certificate oracle, so parent timing is not an exact production cost model.
The next useful work is a longer matched run under the intended production-like
scheduling policy before changing arithmetic or removing any checks.

## Independent verification

The report records all 42 fresh independent GMP packet checks passing, including
nonempty controls and rejection of an intentionally incomplete response. Preflight
took 40.31 s and was outside the timing trials; the whole runner took 86.69 s.

The saved-artifact reviewer independently checked **441 exported member hashes,
216 journal hash chains/checkpoints, 648 original-window visit records and 1,656
native packet receipts** against the published independent GMP oracle. It also
checked source/input identities, the executed binary's build identity, exact
packet/certificate identities, separate pass identities and complete durable
cursors. No missing/duplicated work or count/hit mismatch was found. No local GPU
rerun was needed.

## Files and reproduction

- [Raw L4 report](benchmark-l4.json)
- [Independent review](REVIEW.json)
- [Relative-path build metadata](build-l4.json)
- [Reviewer source](review_results.py)
- [Original notebook](../batching/Fifth42_Batching_Tests.ipynb)

The complete original ZIP, including all durable receipts, is preserved in text
chunks under `transport/`. Reconstruct it without overwriting an existing file:

```bash
python3 load_results_zip.py --output /tmp/Fifth42_Batching_Results.zip
```

ZIP SHA256: `5cd299005c8db278d9a3c2decedf5bd417e9010df6077e2a73d921e3c6810f23`.
Reconstruct the original input bundle with the parent directory's `load_bundle.py`,
then independently review the archive:

```bash
python3 review_results.py /tmp/Fifth42_Batching_Results.zip \
  --bundle /path/to/reconstructed-bundle --sources ../pipeline \
  --batch-sources ../batching --output /tmp/batching-review.json
```

This is one short Colab L4 session with repeated inputs. Remote network delivery,
mirrored checkpoints and production GMP audit scheduling are excluded. Compute-unit
rates/balances were not supplied, so cost efficiency remains unmeasured. Mathematical,
native and exact-result guards are unchanged; production remains unchanged.
