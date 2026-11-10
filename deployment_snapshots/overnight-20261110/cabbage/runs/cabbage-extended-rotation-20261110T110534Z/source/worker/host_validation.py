"""Finite host-only integration checks while the existing GPU search continues."""
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'source/lattice_gpu'))
import coordinator_pipeline as pipeline
import overnight_search as night
import packing_opt
import precision_policy
import scaling_core as core


class SerialPool:
    def map(self, function, values, chunksize=1):
        return list(map(function, values))


class ReferenceEngine:
    backend = 'emulated'

    def run(self, packet, timeout=30):
        began = time.monotonic()
        result = subprocess.run([str(ROOT / 'bin/gmp_reference')], input=packet,
                                text=True, capture_output=True, timeout=timeout, check=True)
        return json.loads(result.stdout), time.monotonic() - began


def resources():
    if os.getloadavg()[0] >= 17:
        raise RuntimeError('Host validation defers above the running preparation budget')
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    if int(memory['MemAvailable'].split()[0]) < 4 * 1024**2:
        raise RuntimeError('Host validation defers below 4 GiB available memory')


def brute(bound, cap):
    fifth = [i**5 for i in range(bound + 1)]
    return {(a, b, c, fifth[a] + fifth[b] - fifth[c])
            for c in range(1, bound + 1) for b in range(1, c) for a in range(1, b + 1)
            if abs(fifth[a] + fifth[b] - fifth[c]) <= cap}


def controls():
    results = []
    engine = ReferenceEngine()
    for bound, cap in ((34, 42), (100, 2951)):
        specs, direct = core.specs(bound, cap, 8)
        expected = brute(bound, cap)
        assert expected
        for policy in ('baseline', 'adaptive'):
            resources()
            lattice = core.lattice()
            selected = specs if policy == 'baseline' else [
                (*s[:-1], precision_policy.geometry_bits(lattice, s[1], s[2],
                 lattice.Q(*s[3]), lattice.Q(*s[4]), s[5])) for s in specs]
            tasks = [core.prepare_task(spec) for spec in selected]
            plan = packing_opt.assemble(bound, cap, selected, direct, tasks,
                                        [core.certify_task(task) for task in tasks])
            hits = set(plan.direct_hits)
            for batch in plan.batches:
                response, _ = engine.run(batch.packet)
                pipeline.validate_response_types(response)
                hits.update(core.decode_batch(batch, response, 'emulated'))
            assert hits == expected
            results.append(dict(bound=bound, cap=cap, geometry_policy=policy,
                                hits=len(hits), independent_brute_force_equal=True))
    return results


def main():
    if sys.flags.optimize:
        raise RuntimeError('Ordinary Python required')
    began = time.monotonic()
    night.initialize(ROOT / 'source/lattice_prototype')
    destination = ROOT / 'host-validation'
    destination.mkdir(exist_ok=False)
    control_results = controls()
    captured = json.loads(Path('/home/pnord/fifth-switch-preflight-20261107/audit/'
                               '20261106T230428Z-captured-checkpoint.json').read_bytes())
    first = captured['next_patch']
    cases = [(first, 256), (first + 4096, 256), (6250000000, 1),
             (10625000000, 1), (11250000000, 1)]
    results = []
    for start, count in cases:
        expected = None
        timings = {'baseline': [], 'adaptive': []}
        for repeat in range(3):
            for policy in (('baseline', 'adaptive') if repeat % 2 == 0 else ('adaptive', 'baseline')):
                resources()
                window = pipeline.Window(100000000001, 200000000000, start,
                                         start + count, 8, 222, 42, policy)
                clock = time.monotonic()
                chunk = pipeline.prepare_chunk(SerialPool(), window, 'packed')
                prepared = time.monotonic() - clock
                record = pipeline.execute_chunk(chunk, ReferenceEngine(), trial='host-only', coordinator=0)
                hits = sorted(map(tuple, record['hits']))
                if expected is None:
                    expected = hits
                assert hits == expected
                timings[policy].append(prepared)
                row = dict(first=start, last=start + count, repeat=repeat, geometry_policy=policy,
                           prepare_certify_pack_seconds=prepared, points=record['points'], hits=hits,
                           selected_bits=sorted(set(p[1] for p in record['precision_bits'])),
                           exact_native_gmp_counts_and_reconstruction_passed=True,
                           certificate_sha256=record['certificate_sha256'])
                results.append(row)
                if repeat == 0 and start == first and policy == 'adaptive':
                    with pipeline.TrialJournal(destination / 'journal-check',
                         dict(trial='host-only', source_identity='host-validation'), window) as journal:
                        bad = dict(record, precision_bits=[])
                        try:
                            journal.commit(bad)
                        except ValueError:
                            pass
                        else:
                            raise AssertionError('Missing adaptive precision manifest committed')
                        assert journal.state['chunks'] == 0
                        journal.commit(record)
                        assert journal.state['next_patch'] == start + count
                    with pipeline.TrialJournal(destination / 'journal-check',
                         dict(trial='host-only', source_identity='host-validation'), window) as journal:
                        assert journal.state['chunks'] == 1
        medians = {name: statistics.median(values) for name, values in timings.items()}
        print(json.dumps(dict(first=start, last=start + count, medians=medians,
                              host_prepare_ratio=medians['baseline'] / medians['adaptive'])), flush=True)
    guard_cases = []
    for policy in ('baseline', 'adaptive'):
        try:
            pipeline.prepare_chunk(SerialPool(), pipeline.Window(
                100000000001, 200000000000, 0, 1, 8, 222, 42, policy), 'packed')
        except (ValueError, pipeline.GuardedPatch) as error:
            guard_cases.append(dict(geometry_policy=policy, excluded_patch=0, error=str(error)))
        else:
            raise AssertionError('Expected first-patch transform guard did not reject')
    report = dict(status='passed', host=os.uname().nodename, controls=control_results,
                  trials=results, first_patch_guard=guard_cases, seconds=time.monotonic() - began,
                  no_gpu_execution=True, production_coverage=False,
                  limitations=['Host preparation timings with one process; no GPU/service speedup claim.',
                               'Selected high-shell patches, supported nonempty independent controls.',
                               'Historical coefficients are not recomputed.'])
    with (destination / 'report.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('trials', 'controls')}), flush=True)


if __name__ == '__main__':
    main()
