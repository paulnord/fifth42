from pathlib import Path
import shutil,hashlib,json,subprocess
old=Path('/home/pnord/scratch/saved-root-pAjTHBhR/cpu')
root=Path.cwd()
for v in ('baseline','candidate'):shutil.copytree(old/v,root/v,ignore=shutil.ignore_patterns('bin','__pycache__'))
shutil.copytree(old/'native',root/'native',ignore=shutil.ignore_patterns('bin'))
(root/'native/bin').mkdir()
shutil.copyfile(old/'native/bin/gmp_reference',root/'native/bin/gmp_reference')
shutil.copytree(root/'baseline/source/lattice_gpu/src',root/'device/src')
shutil.copytree(root/'baseline/source/lattice_gpu/vendor',root/'device/vendor')
(root/'device/bin').mkdir()
path=root/'device/src/kernel.hpp';before=path.read_text()
assert before.count('LATTICE_MAX_BASE=100000000000ULL')==1
B=200_000_000_000
assert 3*B**5+2**63 < 2**191
path.write_text(before.replace('LATTICE_MAX_BASE=100000000000ULL','LATTICE_MAX_BASE=200000000000ULL'))
assert path.read_bytes()==(old/'native/src/kernel.hpp').read_bytes()
(root/'range-extension.patch').write_text(subprocess.run(['diff','-u','--label','a/src/kernel.hpp','--label','b/src/kernel.hpp',str(root/'baseline/source/lattice_gpu/src/kernel.hpp'),str(path)],capture_output=True,text=True).stdout)
(root/'range-proof.json').write_text(json.dumps(dict(max_base=B,lhs=3*B**5+2**63,rhs=2**191,inequality='3*B^5+2^63 < 2^191',passes=True,source='same guard change as overnight_search.extend_arithmetic_range',matches_previously_validated_native_header=True),indent=2)+'\n')
for name in ('scaling_cpu.cpp','io.hpp','stream_io.hpp'):
 assert (root/'device/src'/name).read_bytes()==(root/'native/src'/name).read_bytes()
for v in ('baseline','candidate'):
 for p in (root/v/'source/lattice_gpu/src').glob('*'):
  if p.is_file():assert p.read_bytes()==(root/'baseline/source/lattice_gpu/src'/p.name).read_bytes()
print('Scratch range extension matches pinned CPU-native header exactly; root-source variants unchanged.')
