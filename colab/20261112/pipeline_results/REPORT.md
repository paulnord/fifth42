# Fifth42: Colab CPU preparation and pipeline results

The L4 pipeline run passed. Increasing CPU preparation workers improved this
local selected-window pipeline by **3.38x**, relative to one Colab worker.
GPU kernel time stayed approximately constant at 18 ms.

| Preparation workers | Median local pipeline | Logical cells/second | Speedup vs one |
| ---: | ---: | ---: | ---: |
| 1 | 2.050 s | 1,124 | 1.00x |
| 2 | 1.145 s | 2,012 | 1.79x |
| 4 | 0.712 s | 3,235 | 2.88x |
| 8 | 0.606 s | 3,800 | 3.38x |

Each trial regenerated the same nine windows, 23 byte-identical native packets,
matching certificate identities and 775,687,194 positions over 2,304 logical
cells. There were three randomized repetitions per worker count. Python 3.12.3,
all original dependency pins and native mathematical limits were retained.

## What limits the run

At eight workers, the median consumer wait for prepared work was **0.376 s**,
compared with **0.0178 s** of kernel execution and **0.0321 s** of native RPC.
Mean ready depth was only 0.005, and peak ready depth was one in every trial.
Preparation and its coordination are the main limit in this configuration.
These overlapping timings are not additive, and queue waiting is not a GPU
utilization counter.

Eight workers delivered 17.45% more throughput than four. It was the fastest
count tested, not a demonstrated global optimum. Aggregate preparation and
certification worker CPU time rose from about 1.75 s at four workers to 2.28 s
at eight; parent consistency checks also rose from about 68 ms to 122 ms.
More processes therefore have diminishing returns and measurable overhead.

The separate serial arithmetic profile spent about equal time in preparation
and independent certification. Cumulative matrix multiplication time was about
140 ms, coefficient-bound construction 132 ms, and LLL reduction 110 ms across
two profiled windows. Fifth-root enclosure time was only 12 ms. These cumulative
function times overlap and must not be summed.

Use eight workers as the starting point for the next Colab experiment. The next
useful comparison is CPU preparation in larger groups of windows, measuring
process-pool dispatch, serialization and coordinator costs while retaining the
same per-window certificates, native requests and durable receipts. Production
already has its own multicore/preparation-batch configuration; this experiment
establishes no production speedup or need to change it. A compiled arithmetic
candidate still needs a matched pipeline comparison before adoption.

## Verification

The report records successful fresh independent GMP checks on all 42 original
packets, nonempty controls, and rejection of an intentionally incomplete response.
Fresh preflight took 40.14 s and was excluded from the speed comparisons. The
whole runner took 56.54 s.

An independent saved-artifact review checked all 81 exported member hashes,
source/data identities, native binary identity, **36 journal hash chains and
checkpoints, 108 exact window records, and 276 native packet receipts** against
the published independent GMP oracle. No missing/duplicated windows, changed
packet/certificate identities, incomplete counts or cursor mismatches were found.
No local GPU rerun was needed. This was benchmark replay with zero new scientific
search coverage; production remains unchanged.

## Files and reproduction

- [Raw pipeline report](benchmark-l4.json)
- [Independent artifact review](REVIEW.json)
- [Relative-path build metadata](build-l4.json)
- [Review program](review_results.py)
- [Original notebook](../pipeline/Fifth42_Pipeline_Tests.ipynb)

The complete original ZIP, including its profile and all durable journals, is
preserved as text chunks under `transport/` to meet the repository file limits.
Reconstruct it without overwriting an existing file:

```bash
python3 load_results_zip.py --output /tmp/Fifth42_Pipeline_Results.zip
```

Its SHA256 is `6b813382aa78d96c6d26045d9006cabc61f0610d8e235947fa0e4ae43bb0a1c6`.
To independently review it, reconstruct the original input bundle using the
parent directory's `load_bundle.py`, then run:

```bash
python3 review_results.py /tmp/Fifth42_Pipeline_Results.zip \
  --bundle /path/to/reconstructed-bundle \
  --sources ../pipeline --output /tmp/pipeline-review.json
```

## Limits

One short Colab L4 session with three repetitions per worker count is not a
sustained production throughput test. Pool/engine startup, serial profiling and
recovery were separate from timing. Network delivery, remote mirrored checkpoints
and production GMP audit scheduling were excluded. Local fsync verifies only
local receipt durability. Compute-unit rates and balances were not supplied, so
cost efficiency remains unmeasured. The 3.38x comparison uses one Colab worker as
its baseline and does not describe a gain over the existing distributed search.
