# Fifth42: CPU preparation and local pipeline scaling

This is the next Colab test after the matched L4/A100 packet replays. It measures
whether CPU preparation limits the rate at which exact work reaches the GPU.
Use the GPU runtime already connected; an A100-to-L4 switch is unnecessary for
this experiment. Record the actual GPU and compute-unit rate when available.

The experiment compares **1, 2, 4 and 8 preparation workers**, in randomized
order over three repetitions. It regenerates all nine original 256-cell windows
and requires **byte-for-byte equality** of the 23 native packets and their exact
certificates against the published, independently checked inputs. All native
task, packet, base and overflow limits stay unchanged.

The timed local pipeline includes preparation, exact certification, packet
assembly/serialization, bounded preparation ahead, native transfers/execution,
exact output verification, buffered local journal commits and the final fsync.
Each trial then reopens its journals to verify the durable cursor and hash chain;
recovery time is reported separately. Every trial replays 2,304 logical cells and
775,687,194 coefficient positions. This is benchmark work, with **zero new search
coverage** and no changes to production, reservations or ownership.

Before timing, all 42 original packets (including nonempty controls) must agree
with fresh independent GMP and the deliberately incomplete response must fail.
This exhaustive preflight is reported separately. Two serial preparation
profiles, also outside the timing trials, identify expensive arithmetic functions.

## Reproducible environment

The original planner requires Python 3.12 and pinned versions of sympy, fpylll,
cysignals, numpy and gmpy2. The notebook creates a separate Python 3.12 environment
inside its temporary runtime directory. It leaves the Colab notebook kernel alone.
The original version guards remain in place; do not remove them.

`vendor/worker/` contains 19 source files copied unchanged from the frozen worker
used to generate the original inputs. [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json)
records their identities. The notebook checks every downloaded source file and
reuses the earlier immutable source/data bundle. No campus filesystem access,
local uploads, production configuration or live device lease is needed.

For a reconstructed local bundle with these pipeline files downloaded:

```bash
python3.12 -m venv pipeline-venv
pipeline-venv/bin/python -m pip install --only-binary=:all: -r pipeline/requirements.txt
pipeline-venv/bin/python build.py --gpu
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 \
  pipeline-venv/bin/python pipeline/pipeline_bench.py \
  --backend gpu --workers 1 2 4 8 --repeats 3 --max-seconds 480
```

Worker counts that would leave no logical CPU for the coordinator are skipped
(a one-worker baseline remains available). The stream has two ready buffers,
one-window preparation batches, physical group limit 2 and eight-record journal
buffers with a 0.25-second age limit. These settings are held fixed across worker
counts. Pool/engine startup, preflight, serial profiling and recovery are separate
from the selected-window throughput timing.

## Interpretation and limits

Compare median **pipeline seconds** and logical cells per second across worker
counts. Inspect consumer waiting for prepared work, exact worker preparation/
certification time, native RPC/kernel time, journal flush time and the arithmetic
profile. Worker sums and producer/consumer stages overlap: do not add them or
label queue waiting as hardware GPU utilization.

This is a local pipeline benchmark, not the complete distributed production
service. Network delivery, remote mirrored checkpoints, production admission and
periodic GMP audit scheduling are excluded. Local fsync proves local receipt
durability only. Fresh GMP preflight covers every supplied packet but is not an
estimate of production audit overhead. Nine windows do not establish sustained
throughput. No performance adoption follows automatically from this test.

The runner has an eight-minute limit, saves failure reports, and stops on any
source, packet, certificate, native-count, exact-hit or durable-recovery mismatch.
The notebook limits the whole setup/test session to fifteen minutes. Download
`Fifth42_Pipeline_Results.zip` before releasing the runtime.
