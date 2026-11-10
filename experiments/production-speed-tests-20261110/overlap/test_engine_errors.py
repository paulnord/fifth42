#!/usr/bin/env python3
"""Framed-engine safety gate: capacity failure, malformed payload, recovery."""
import argparse
from pathlib import Path
from bench_overlap import Engine,canonical
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--controls',type=Path,required=True);a=p.parse_args()
e=Engine(a.engine,1)
try:
    for payload in [(a.controls/'many64.packet').read_bytes(), b'LATTICE_GPU_V1 0 42 0\nEXTRA\n']:
        row,_=e.run(payload)
        assert row.get('box_complete') is False and 'error' in row,row
        row,_=e.run((a.controls/'empty.packet').read_bytes())
        assert canonical(row)==dict(points=0,counts=[],hits=[]),row
    row,_=e.run((a.controls/'single.packet').read_bytes())
    assert len(canonical(row)['hits'])==1,row
    print('passed: capacity failure, malformed input, subsequent clean requests')
finally:e.close()
