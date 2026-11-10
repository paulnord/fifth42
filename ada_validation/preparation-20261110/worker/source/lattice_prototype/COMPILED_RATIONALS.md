# Optional compiled exact rationals: bounded experiment

## Finding

GMP's exact rational arithmetic is a practical additional improvement. The
isolated gmpy2 2.2.2 experiment is about 1.7–2.0 times faster than Python Fraction
for these complete bounded searches, without changing geometry, candidates,
result sets, budgets, or exact exclusion rules. It remains opt-in and does not
change the default/reference modules. This is a bounded prototype result, not a
production-scale performance claim or a proof outside the stated bounds.

Five warm paired runs, alternating which arithmetic engine runs first:

| Search | Mode | Fraction median | GMP mpq median | Speedup |
|---|---|---:|---:|---:|
| signed target42, bound100 | prune | 0.2811 s | 0.1465 s | 1.92× |
| signed target42, bound100 | interval | 0.3324 s | 0.1769 s | 1.88× |
| signed target42, bound1000 | prune | 2.4130 s | 1.2856 s | 1.88× |
| signed target42, bound1000 | interval | 3.1227 s | 1.8256 s | 1.71× |
| positive residuals 12/384, bound34 | prune | 0.1224 s | 0.0721 s | 1.70× |
| positive residuals 12/384, bound34 | interval | 0.1372 s | 0.0759 s | 1.81× |
| positive residual2951, bound100 | prune | 0.2949 s | 0.1495 s | 1.97× |
| positive residual2951, bound100 | interval | 0.3278 s | 0.1792 s | 1.83× |

These are local wall-clock samples, not controlled dedicated-machine timing.
All use published fpylll 0.6.4 for LLL, width 2, 48-bit dyadic root enclosures,
and moduli (25,31,61). In this snapshot prune is faster than interval; this
experiment does not establish a universal winning enumeration mode.

## Exact validation

- Every planned patch's parameters, original rational basis, reduced basis,
  integer unimodular transform, Gram–Schmidt coefficients and norms match
  Fraction exactly: 58 patches at signed bound100, 463 at signed bound1000,
  27 for residuals12/384, and 56 for residual2951. Serialized exact geometry
  hashes are recorded in the benchmark JSON.
- Every result field, shell, search counter and filter counter matches,
  excluding elapsed seconds. All runs return complete bounded coverage.
- All result sets match the independent direct oracle. Both signed target42
  searches have no hits. Nonempty positive controls are (13,16,17,12),
  (26,32,34,384), and (42,71,72,2951).
- Five focused regression tests cover source-snapshot/live-code behavioral
  equality (AST comparison ignoring docstrings), default-module isolation, 54 exact
  outward-root cases, exhausted node/patch/time budgets, and exact sphere
  boundary inclusion. All pass.
- No floating arithmetic is introduced in geometry, exclusions, enumeration or
  residual tests. Existing fpylll reduction may use approximate internals;
  its integer unimodular output is still certified by exact arithmetic.

Two additional published large fixtures were verified with exact residual targets,
160-bit root enclosures and prune mode: (13852184,27401825,27580409) with
residual -359711619643000, and (21137517920,21483066250,24482314857) with
residual -75381811685198766057. Each was found with exactly identical patch
geometry, reduced geometry, result sets and counters under Fraction and mpq.
Single-run Fraction/mpq times were 0.00973/0.00301 s and 0.11226/0.02952 s.
These are **fixture-selected single patches only, NOT complete large shells**;
they do not imply bounded global coverage at those magnitudes or target42 hits.
The selected-patch results are in `results/compiled-mpq-large-controls.json`.

## Isolation and limitations

`compiled_experiment/benchmark_mpq.py` loads frozen copies of the two prototype
modules under private module names. Only those private instances have their Q
constructor replaced by `gmpy2.mpq`; the filter instance points to the matching
private lattice instance. This is an explicitly experimental dependency-
substitution harness, not a production global monkeypatch or a default path.
It registers private module names for dataclass introspection. The ordinary
`lattice5` and `modular_filters` modules remain unchanged, tested explicitly.

Frozen source snapshots ensure later parent edits do not silently alter these
measurements. Revalidate against newer source before integrating an explicit
arithmetic backend. No FLINT adapter was pursued after GMP proved useful.
No ADA work, production run, or external publication was performed.

## Profile

The mpq interval bound1000 profile takes 1.627 s under cProfile. Remaining
cumulative costs include recursive enumeration (1.224 s), allowed-residue
construction (0.333 s), exact Gram–Schmidt (0.187 s), and LLL (0.090 s).
Python Fraction/gcd overhead is removed from the hot path; C arithmetic costs
are attributed within callers. Profiles are diagnostic, not benchmark samples.

## Dependency provenance and licenses

- Optional dependency: gmpy2 **2.2.2**, retrieved with pip from PyPI.
- Published source: https://github.com/gmpy2/gmpy2 ; package:
  https://pypi.org/project/gmpy2/2.2.2/
- Installed wheel: `gmpy2-2.2.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`.
- Downloaded wheel SHA-256:
  `3cb1c389fed4e572255ecc2f8053de7e0f05d7d270e953258d44667f136d454e`.
- Wheel metadata declares **LGPL-3.0+**. The exact installed METADATA and
  upstream COPYING/COPYING.LESSER are preserved in `compiled_experiment/`.
- Runtime reports GMP 6.3.0, MPFR 4.2.1, MPC 1.3.1 bundled in the wheel. Only
  exact mpq arithmetic is used here. GMP is dual LGPLv3+/GPLv2+; MPFR and MPC
  use LGPLv3+. Any redistribution must retain the applicable notices and
  comply with source/relinking obligations. This experiment does not package
  or publish these third-party binaries.
- Installed outside the deliverable in sibling `fifth_lattice_compiled_deps`;
  existing fpylll dependencies remain in sibling `fifth_lattice_deps`.

## Reproduce

From the artifact directory, using an isolated virtual environment:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-fpylll.txt -r compiled_experiment/requirements.txt
python compiled_experiment/test_mpq.py
python compiled_experiment/benchmark_mpq.py
python compiled_experiment/large_controls_mpq.py
```

Files: `results/compiled-mpq-benchmark.json`,
`results/profile-{fraction,mpq}-interval-1000.txt` (binary .prof files are regenerated locally and omitted from the text-only archive),
`compiled_experiment/benchmark_mpq.py`, `compiled_experiment/test_mpq.py`.
The benchmark records all five raw times per variant, exact geometry hashes,
full counters, result sets, and validation flags.

Snapshot SHA-256 values (also in `compiled_experiment/SHA256SUMS`):

- lattice5_snapshot.py: `89c55504aa70a41f16cc3d2b4d39d8a563af499221ede48d725bc32ce1ff03eb`
- modular_filters_snapshot.py: `148e57bd88808f5e383334d10df9fb3c470fbca4b8c6d8a1a38a161f12b5371d`

At validation, lattice5 was byte-identical; the only modular_filters difference
was the search_patch docstring listing all five supported modes. The AST
regression test guards against behavioral drift in either live source.
