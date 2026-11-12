# Fifth42: matched L4 and A100 prepared-packet replays

The A100 run passed all 42 original packet checks against independent GMP,
including fresh GMP reproduction and rejection of an incomplete response. The
archive records NVIDIA A100-SXM4-40GB. Source/data hashes and packet sizes match
the L4 baseline. Both used CUDA 13.0, GCC 13.3, native-architecture rebuilds and
seven repetitions per case.

| Median measurement | L4, second session | A100 |
| --- | ---: | ---: |
| Production-sized replay, 23 requests / 775,687,194 positions | 35.404 ms | 36.840 ms |
| Production-sized GPU kernel | 17.612 ms | 18.856 ms |
| Production-sized engine RPC | 23.981 ms | 25.453 ms |
| Tiny replay, 16 separate requests | 4.092 ms | 6.092 ms |
| Tiny replay, one combined request | 0.727 ms | 0.730 ms |
| Tiny separate/combined replay ratio | 5.63x | 8.34x |

A100 took 4.06% longer for the production-sized replay and 7.06% longer in its
kernel measurement. The larger tiny-batching ratio on A100 reflects slower
separate requests; combined tiny replay was approximately equal. Production-sized
requests remain byte-identical after batching, so no batching gain applies there.

Retain L4 as the validated replay backend. These observations give no reason to
prefer A100 for this supplied packet replay. Measure CPU preparation and full
pipeline throughput before changing production hardware.

The three L4 sessions had median production-sized replay times of 35.415,
35.404 and 35.364 ms. There is one A100 session. These are short replays on
different cloud VMs, not sustained throughput tests or a universal hardware ranking.
CPU planning, network delivery, durable journals and cloud checkpoints are
excluded. Compute-unit rates/balances were not supplied, so cost efficiency
cannot be compared. There is zero new scientific search coverage.

[Raw A100 report](results/benchmark-a100.json) ·
[A100 artifact review](results/colab-a100-review.json) ·
[Raw L4 baseline](results/benchmark-l4-r2.json) ·
[Reproduction instructions](A100_COMPARISON.txt)
