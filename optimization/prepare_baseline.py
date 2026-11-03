#!/usr/bin/env python3
"""Record the locally built, unchanged production baseline for comparison."""
from pathlib import Path
import json
from run import sha

root=Path(__file__).resolve().parent
production=root.parent
paths=('src/search_gpu.cu','src/search_cpu.cpp','src/exact.hpp','src/search_common.hpp')
(root/'docs').mkdir(exist_ok=True)
(root/'docs/baseline-manifest.json').write_text(json.dumps({
    'baseline_sources':{p:sha(production/p) for p in paths},
    'baseline_gpu_binary_sha256':sha(root/'bin/reference_gpu'),
    'baseline_cpu_binary_sha256':sha(root/'bin/reference_cpu'),
    'scope':'Production source rebuilt as a separate reference; benchmark only after production run releases its lock.'
},indent=2)+'\n')
print('Recorded production reference source and binary hashes.')
