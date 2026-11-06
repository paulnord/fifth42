#!/usr/bin/env python3
"""Create a new, isolated proposed low64 A/B source tree. Never deploy."""
import argparse, difflib, hashlib, json, shutil, subprocess, sys
from pathlib import Path

KERNEL_SHA = 'dc42b5dbfc4bfa64511acb081d0597c90e407c11efeefe81cfa6c260305a8f3b'
GPU_SHA = '5b6d7e3270ac0b9c43f42fa56af2fe1ef98c1b20b37ed147fcfd91e37bdc6977'
HELPER = '''// Proposed scratch-only low64 necessary condition. All operations unsigned.
HD inline std::uint64_t fifth_low64(std::uint64_t x) {
    const auto square=x*x;
    return square*square*x;
}
HD inline bool residual_low64_passes(S64 a,S64 b,S64 c,std::uint64_t cap) {
    const auto u=fifth_low64(static_cast<std::uint64_t>(a))
                +fifth_low64(static_cast<std::uint64_t>(b))
                -fifth_low64(static_cast<std::uint64_t>(c));
    // read_input proves cap <= INT64_MAX. Correct for cap=0 too.
    return (u+cap) <= (cap+cap);
}
'''

def main():
    if sys.flags.optimize:raise SystemExit('Do not use Python -O')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); root=a.bundle.resolve(); out=a.output.resolve()
    if out.exists() or root==out or root in out.parents:
        p.error('output must be new and outside the immutable source bundle')
    subprocess.run(['sha256sum','--status','-c','SHA256SUMS'],cwd=root,check=True)
    overlay=root/'fifth42-coordinator-overlay'
    repo=root/'fifth42-coordinator-20261105/lattice_gpu'
    original=(overlay/'src/kernel.hpp').read_text()
    assert hashlib.sha256(original.encode()).hexdigest()==KERNEL_SHA
    assert hashlib.sha256((repo/'src/scaling_gpu.cu').read_bytes()).hexdigest()==GPU_SHA
    anchor='HD inline bool evaluate('
    gate='    const auto residual=fifth64(a)+fifth64(b)+(-fifth64(c));'
    assert original.count(anchor)==1 and original.count(gate)==1
    candidate=original.replace(anchor,HELPER+anchor).replace(gate,
        '    if(mode==0&&!residual_low64_passes(a,b,c,cap))return false;\n'+gate)
    out.mkdir(parents=True)
    for name in ['baseline','low64']:
        shutil.copytree(overlay,out/name)
        shutil.copyfile(repo/'src/scaling_gpu.cu',out/name/'src/scaling_gpu.cu')
    (out/'low64/src/kernel.hpp').write_text(candidate)
    (out/'low64.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),
        fromfile='baseline/src/kernel.hpp',tofile='low64/src/kernel.hpp')))
    shutil.copyfile(repo/'engine_session.py',out/'engine_session.py')
    shutil.copytree(root/'fifth42-primitivity-20261106',out/'packet-evidence',
                    ignore=shutil.ignore_patterns('*'))
    for name in ['manifest.json','small1000.packet','controls100.packet','high8.packet','high32.packet']:
        shutil.copyfile(root/'fifth42-primitivity-20261106'/name,out/'packet-evidence'/name)
    for name in ['small1000','controls100','high8','high32']:
        shutil.copyfile(root/'fifth42-other-sieves-20261106'/(name+'.interval.json'),
                        out/'packet-evidence'/(name+'.interval.json'))
    files={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest()
           for f in sorted(out.rglob('*')) if f.is_file()}
    (out/'source-manifest.json').write_text(json.dumps(dict(status='proposed_unvalidated_cuda',files=files),indent=2)+'\n')
    print(out)

if __name__=='__main__':main()
