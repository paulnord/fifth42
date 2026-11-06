#!/usr/bin/env python3
"""Rebuild in a fresh local copy. Never mutate bundled evidence or contact Ada."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PRIM = 'fifth42-primitivity-20261106'
OTHER = 'fifth42-other-sieves-20261106'
AUDIT = 'lowword-audit-20261106'
REPO = 'fifth42-coordinator-20261105'
OVERLAY = 'fifth42-coordinator-overlay'
CASES = [('small1000', '-42,42'), ('high8', '-42,42'),
         ('high32', '-42,42'), ('controls100', '12,384,2951,-960')]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['native', 'packets', 'sphere', 'host-tests', 'timings'])
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--compiler', default='g++')
    args = ap.parse_args()
    out = args.output.resolve()
    if out.exists():
        ap.error('output already exists; choose a new directory to preserve prior evidence')
    if out == ROOT or ROOT in out.parents:
        ap.error('output must be outside the immutable bundle')
    out.mkdir(parents=True)
    for folder in [PRIM, OTHER, AUDIT, OVERLAY, REPO]:
        shutil.copytree(ROOT / folder, out / folder)
    log = (out / 'reproduction.log').open('w', buffering=1)
    summary = {'mode': args.mode, 'status': 'running', 'checks': []}

    def run(command, stdin=None, env=None):
        command = list(map(str, command))
        log.write('$ ' + ' '.join(command) + '\n')
        print('$ ' + ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=out, input=stdin, text=True, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.write(result.stdout)
        result.check_returncode()
        return result.stdout

    def compile_(source, dest, sanitize=False):
        flags = ['-O1', '-g', '-fsanitize=undefined', '-fno-sanitize-recover=all'] if sanitize else ['-O3']
        run([args.compiler, *flags, '-std=c++17', '-Wall', '-Wextra', out / source, '-o', out / dest])

    def script(folder, filename):
        return run([sys.executable, out / folder / filename])

    try:
        if args.mode in ('native', 'timings'):
            compile_(PRIM + '/bench.cpp', PRIM + '/bench')
            compile_(PRIM + '/bench_cached.cpp', PRIM + '/bench_cached')
            compile_(OTHER + '/bench.cpp', OTHER + '/bench')
        if args.mode == 'native':
            compile_(OTHER + '/bench.cpp', AUDIT + '/bench-rebuilt')
            compile_(OTHER + '/lowword_checks.cpp', OTHER + '/lowword_checks', True)
            compile_(AUDIT + '/audit.cpp', AUDIT + '/audit', True)
            compile_(PRIM + '/bench_cached.cpp', PRIM + '/bench_ubsan', True)
            script(AUDIT, 'recheck_packets.py')
            script(AUDIT, 'run_audit.py')
            script(OTHER, 'checks.py')
            run([out / OTHER / 'lowword_checks'])
            for case, targets in CASES:
                packet = (out / PRIM / (case + '.packet')).read_text()
                for binary, suffix in [('bench', '.results.json'), ('bench_cached', '.cached.results.json')]:
                    actual = json.loads(run([out / PRIM / binary, targets, '1'], packet))
                    prior = json.loads((ROOT / PRIM / (case + suffix)).read_text())
                    for key in ['all', 'nonprimitive', 'shape', 'shape_nonprimitive',
                                'mods', 'mods_nonprimitive', 'hit_records',
                                'all_variant_hit_sets_equal', 'all_gcd_mappings_equal', 'hits']:
                        if actual[key] != prior[key]:
                            raise AssertionError((case, binary, key))
                    summary['checks'].append({'packet': case, 'binary': binary, 'exact_parity': True})
                    (out / PRIM / (case + '.' + binary + '.recheck.json')).write_text(json.dumps(actual, indent=2))
            run([out / PRIM / 'bench_ubsan', '12,384,2951,-960', '1'],
                (out / PRIM / 'controls100.packet').read_text())
            summary['independent_audit'] = json.loads((out / AUDIT / 'audit.json').read_text())
            summary['additional_sieve_packets'] = json.loads((out / AUDIT / 'packet-recheck.json').read_text())
        elif args.mode == 'timings':
            script(PRIM, 'run_bench.py')
            script(PRIM, 'run_cached.py')
            script(OTHER, 'run.py')
        elif args.mode == 'packets':
            script(PRIM, 'prepare.py')
            actual = json.loads((out / PRIM / 'manifest.json').read_text())
            prior = json.loads((ROOT / PRIM / 'manifest.json').read_text())
            for case in prior:
                for key in ['patches', 'points', 'direct', 'sha256', 'certificate_sha256']:
                    if actual[case][key] != prior[case][key]:
                        raise AssertionError((case, key))
                packet_hash = hashlib.sha256((out / PRIM / (case + '.packet')).read_bytes()).hexdigest()
                if packet_hash != prior[case]['sha256']:
                    raise AssertionError((case, 'actual_packet_bytes'))
                summary['checks'].append({'packet': case, 'packet_and_certificate_hashes_equal': True})
        elif args.mode == 'sphere':
            script(PRIM, 'sphere_test.py')
            summary['sphere_status'] = json.loads((out / PRIM / 'sphere-results.json').read_text())['status']
        elif args.mode == 'host-tests':
            gpu = out / REPO / 'lattice_gpu'
            run(['make', '-C', gpu, '-f', 'scaling.mk', 'CXX=' + args.compiler,
                 'bin/scaling_cpu', 'bin/scaling_cpu_sanitize', 'bin/scaling_oracle'])
            environment = dict(os.environ, SCALING_LATTICE_SOURCE=str(out / REPO / 'lattice_prototype'))
            run([sys.executable, '-m', 'unittest', 'discover', '-s', gpu / 'tests', '-v'], env=environment)
        summary['status'] = 'passed'
    except Exception as exc:
        summary['status'] = 'failed'
        summary['error'] = str(exc)
        raise
    finally:
        (out / 'validation.json').write_text(json.dumps(summary, indent=2) + '\n')
        log.close()
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
