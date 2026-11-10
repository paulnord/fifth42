#!/usr/bin/env python3
"""Stage a private pip-CUDA LTO layout without modifying the original install."""
import argparse,pathlib,shutil
p=argparse.ArgumentParser();p.add_argument('cuda_root');p.add_argument('destination');a=p.parse_args()
src=pathlib.Path(a.cuda_root).resolve(strict=True);dst=pathlib.Path(a.destination).absolute()
if dst.exists():raise SystemExit('destination must be new')
nvvm=next((x for x in [src/'nvvm/lib64/libnvvm.so',src/'lib/libnvvm.so.4',src/'lib64/libnvvm.so.4'] if x.is_file()),None)
if nvvm is None:raise SystemExit('matching libnvvm missing; install matching nvidia-nvvm package, do not mix toolkits')
for x in ['bin/nvcc','bin/nvcc.profile','nvvm/bin/cicc','nvvm/libdevice/libdevice.10.bc']:
 if not (src/x).is_file():raise SystemExit('missing '+str(src/x))
dst.mkdir(parents=True)
for x in src.iterdir():
 if x.name not in ('bin','nvvm'):(dst/x.name).symlink_to(x,target_is_directory=x.is_dir())
(dst/'bin').mkdir()
for x in (src/'bin').iterdir():
 if x.name in ('nvcc','nvcc.profile'):shutil.copy2(x,dst/'bin'/x.name)
 else:(dst/'bin'/x.name).symlink_to(x,target_is_directory=x.is_dir())
(dst/'nvvm/lib64').mkdir(parents=True)
for x in (src/'nvvm').iterdir():
 if x.name!='lib64':(dst/'nvvm'/x.name).symlink_to(x,target_is_directory=x.is_dir())
(dst/'nvvm/lib64/libnvvm.so').symlink_to(nvvm.resolve())
print(dst/'bin/nvcc')
