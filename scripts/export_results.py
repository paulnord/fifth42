#!/usr/bin/env python3
"""Export compact verified results, excluding raw checkpoints and machine IDs."""
from datetime import datetime,timezone
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import run

def main():
    entries=[]
    for name in ('cpu-B10000','cpu-B100000','gpu-B100000','gpu-B1000000','gpu-B10000000','gpu-B35000000'):
        path=ROOT/'runs'/name/'state.json'
        if not path.exists():continue
        s=json.loads(path.read_text())
        run.coverage(s)
        chunks=s['chunks'];b=s['config']['bound'];n=s['next_row']
        entry={'backend':s['config']['backend'],'target':s['config']['target'],
               'bound':b,'filter':s['config']['filter'],
               'complete':n==s['total_rows'],'rows_completed':n,'total_rows':s['total_rows'],
               'chunks_completed':len(chunks),'steps':sum(c['steps'] for c in chunks),
               'search_seconds':sum(c['search_seconds'] for c in chunks),
               'engine_wall_seconds':sum(c['wall_seconds'] for c in chunks),
               'solutions':sorted({tuple(sorted(h)) for c in chunks for h in c['hits']}),
               'last_committed_utc':s['updated_utc'],
               'source_and_binary_sha256':s['fingerprint'],
               'coverage_meaning':'full signed integer box via mod11 roles and a<=b' if n==s['total_rows'] else 'canonical z-row prefix only; not a full box',
               'covered_z_start':-11*(b//11) if n else None,
               'covered_z_stop_inclusive':11*(n-1-b//11) if n else None}
        entries.append(entry)
    if not entries:raise SystemExit('No local run states found; retained checked-in summary unchanged')
    document={'schema':1,'exported_utc':datetime.now(timezone.utc).isoformat(),
              'arithmetic':'exact signed 128-bit CPU; unsigned two-limb GPU; Python arbitrary-precision candidate verification',
              'scope':'Finite search boxes and explicitly labeled partial prefixes; no claim about all integers.',
              'runs':entries}
    dest=ROOT/'results/coverage.json';dest.parent.mkdir(exist_ok=True)
    run.atomic_json(dest,document)
    optimization=ROOT/'optimization/runs/optimized-validation.json'
    if optimization.exists():
        r=json.loads(optimization.read_text())
        keep=('cpu_emulation_status','gpu_status','tests_run','high_word_cases_checked_with_python',
              'gpu_comparisons','example_pruning_steps')
        run.atomic_json(ROOT/'results/optimization-validation.json',{k:r[k] for k in keep if k in r})
    print(f'Exported {len(entries)} verified run summaries to {dest.relative_to(ROOT)}')

if __name__=='__main__':main()
