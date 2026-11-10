#!/usr/bin/env python3
"""Launch the reviewed search under the persistent user systemd manager."""
from datetime import datetime
import subprocess
import time

unit='fifth-lattice-overnight-20261105'
subprocess.run(['systemctl','--user','reset-failed',unit+'.service'],check=False,capture_output=True)
runtime=max(1,int(datetime.fromisoformat('2026-11-06T09:00:00-06:00').timestamp()-time.time()+120))
command=['systemd-run','--user','--unit='+unit,'--property=Nice=19','--property=MemoryMax=8G',
    '--property=CPUQuota=1600%','--property=TimeoutStopSec=20','--property=KillMode=control-group',
    '--property=RuntimeMaxSec='+str(runtime),'--property=Environment=CXX=/usr/bin/g++-13',
    '--property=StandardOutput=append:/home/pnord/fifth-lattice-gpu/overnight-unit.log',
    '--property=StandardError=append:/home/pnord/fifth-lattice-gpu/overnight-unit.log',
    '/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python',
    '/home/pnord/fifth-lattice-gpu/overnight_service.py']
subprocess.run(command,check=True)
