"""Independent stop interface; final-copy units may finish afterwards."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parent
binding=R/'active-configuration.json'
if binding.exists():
 c=json.loads(Path(json.loads(binding.read_bytes())['config']).read_bytes())
 subprocess.run(['systemctl','--user','stop',c['service_name']],check=True,timeout=12)
subprocess.run(['systemctl','--user','stop','cabbage-extended-controller-20261109.service'],check=True,timeout=15)
