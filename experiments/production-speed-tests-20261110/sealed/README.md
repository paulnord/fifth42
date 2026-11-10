# Sealed packet experiment (isolated, not production)

This prototype preserves process-local immutable packet text and scientific field
snapshots after the existing `buffered_pipeline.validate_cached` check. Repeated
validation compares the captured values instead of recreating packets or hashing
canonical task payloads. Disk/IPC copies are not trusted; they must pass the full
canonical validator and be resealed. Weak references release seals with their chunks.
This is ordinary in-process integrity checking, not cryptographic protection from
malicious Python code, arbitrary memory corruption, or an untrusted pickle.

## Run

```
python -m unittest -v test_sealed_packets
python benchmark_packets.py --worker /path/to/pinned/archived/worker --output packet-results.json
```

The benchmark uses real production Task/Batch/PreparedChunk classes, packet encoder,
canonical validation and registered payload hashes, but **synthetic task geometry**.
It is only a transport/validation microbenchmark: the fixture is deliberately never
passed to native search or claimed as certified scientific coverage. Real integration
must seal only output of exact certified preparation and compare packets/counts/hits.

## Validation and preliminary outcome

Eight tests pass, including 17 mutation controls, unsealed copies, bad canonical packet,
mutable fields, cap binding and weak-reference cleanup. A 1024-task /20 alternating
repeat cloud test measured baseline median 2.88ms versus sealed median 1.49ms.
The initial sealing cost was 14.46ms, so repeatedly calling `seal()` for every single
use would be a regression. Reuse must be sufficient to amortize it, or seal creation
must be integrated with the already-canonical construction (avoiding a second full
validation). No whole-pipeline gain is claimed; do not deploy this module as-is.

The current candidate still scans task fields and compares scientific state; it does
not weaken exact arithmetic certification. Timing fields are deliberately excluded.
Do not eliminate the original independent scientific certification in an integration.
