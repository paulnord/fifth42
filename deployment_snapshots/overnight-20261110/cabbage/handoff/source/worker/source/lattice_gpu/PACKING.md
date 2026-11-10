# Packing-only optimization

The normal scaling launcher now uses the optimized certificate packer:

```bash
python3 ~/fifth-lattice-gpu/scaling.py --wait
```

Use `--packing baseline` to select the earlier packer. Both retain the same
geometry, exact certificates, hashes, packet bytes, patch width, and coverage
checks. The optimization avoids the recursive dataclass copy when serializing
immutable task fields for the existing canonical JSON hash. It does not change
the certificate format or remove the parent-process identity check.

To reproduce the isolated comparison:

```bash
python3 ~/fifth-lattice-gpu/packing_benchmark.py --wait
```

This uses 16 physical CPU cores, one GPU, five alternating paired repeats at
bounds 8,000 and 32,000, and a ten-minute overall cap. Every timed variant
builds and certifies fresh geometry. One set of measurements retains the
existing worker pool and persistent engines; a separate set measures actual
cold one-pass lifetimes, including startup and shutdown. Preparation reuse
across searches and wider patches are not part of the experiment.

The measured run passed all 60 timed pipeline observations and the independent
exact oracle controls. At bound 32,000, persistent-engine GPU pipeline medians
fell from 1.494903 to 1.231908 seconds (17.6% less time); actual cold one-pass
medians fell from 1.940277 to 1.686408 seconds (13.1% less time). These are
per-search medians, not suite elapsed times. The entire suite took 53.489 seconds.

Results are saved under
`~/fifth-lattice-gpu/packing-runs/20261105T212247Z-i0gdlbsz/`.
The original baseline code and earlier run artifacts remain available. The
theoretical 1.7x ceiling for eliminating all packing is not an expected gain.
