"""Small exact controls, not representative production performance inputs."""
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
for name,n,j,cap in [('empty',0,0,42),('single',1,3,42),('odd3',3,4,42),('even4',4,8,42),('many64',64,3,42),('nohits',2,3,0)]:
    s='LATTICE_GPU_V1 0 %d %d\n'%(cap,n)
    for i in range(n):s+='%d 1 20 %d %d %d\n1 0 0 0 1 0 0 0 1\n'%(i,j,j,j)
    (a.output/(name+'.packet')).write_text(s)
