# ADA four133 extension review snapshot

Current run: [status report](../ADA_STATUS.md) and [machine-readable snapshot](../status.json).

These files snapshot `~/four133-eight-hour` on ADA. The active job uses its own frozen code in `jobs/B10800000-20261104T184003Z/code`; publication does not change it. `PROOF.md`, `src/search.cpp`, `math133.py`, `audit.py`, and `run.py` are byte-for-byte copies of that job's frozen files. Other scripts, tests, and saved reports come from the preparation workspace. The executable itself remains on ADA; its hash is recorded in the evidence.

`plan.json` is the original prelaunch plan and retains its historical "not started" wording. Use `../status.json` for the dated running status. `snapshot-manifest.json` hashes every published file in this directory except itself.

- [General finite-box proof](PROOF.md)
- [Engine](src/search.cpp), [independent counts](math133.py), [chunk audit](audit.py), [coordinator](run.py)
- [Oracle and sanitizer results](validation.json), [archived-engine comparison](baseline-validation.json), [coordinator checks](runner-validation.json)
- [Prior full-archive verification](prior-verification.json)
- [Stratified calibration](calibration/B10800000/results.json), [production-size chunk calibration](calibration/B10800000-long-chunks/results.json), [worker comparison](worker-scaling.json)
- [Thermal samples](temperature.csv), [thermal summary](temperature-summary.json)

To rebuild the new engine for bounded tests, in a disposable copy of this directory:

```sh
g++-13 -std=c++17 -O3 -Wall -Wextra -Werror src/search.cpp -o search
g++-13 -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -D_GLIBCXX_ASSERTIONS src/search.cpp -o search-sanitized
python3 tests/test_search.py
python3 tests/test_runner.py
```

The baseline comparison additionally needs `old-reference` freshly built from the pinned archived source. `tests/test_baseline.py` and `verify_prior.py` retain the ADA workspace layout: this directory's sibling `four133-handoff/frozen` holds the extracted original chain; `four133-handoff/fresh-audits` holds disposable audit copies. That full archived evidence is on the handoff branch, and is not duplicated here. The original workspace instructions are in [ADA_README.md](ADA_README.md).

The thermal CSV preserves every value and timestamp; its line endings are normalized to LF. No raw production logs, resumable checkpoints, executables, or new search launch are part of this commit.
