#!/usr/bin/env python3
"""Generate a project-only CUDA 12.8 / glibc 2.43 compatibility header.

CUDA's declarations of sinpi/cospi/rsqrt lack glibc's noexcept. Suppress
only those three glibc macro invocations in CUDA translation units (including
their float/long-double expansions). The integer-only kernels use none of them.
Preserve the system header and its license; never edit /usr or install anything.
"""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parent
source = Path('/usr/include/x86_64-linux-gnu/bits/mathcalls.h')
content = source.read_text()
out, n = re.subn(r'^(__MATHCALL_VEC \((?:cospi|sinpi|rsqrt),, .*?;)$',
                 r'#if !defined(__CUDACC__)\n\1\n#endif', content, flags=re.M)
if n != 3:
    raise SystemExit('Unexpected system header; compatibility overlay needs review')
dest = root / 'compat/bits/mathcalls.h'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(out)
(root / 'compat/provenance.json').write_text(json.dumps({
    'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'change': 'Hide cospi, sinpi, rsqrt glibc declarations only under __CUDACC__',
    'patched_macro_invocations': n,
}, indent=2) + '\n')
print(f'Generated {dest}; no system files changed')
