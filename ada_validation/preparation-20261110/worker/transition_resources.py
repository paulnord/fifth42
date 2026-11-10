"""Fresh idle-CPU observation for a verified, very recent owned handoff only."""
from datetime import datetime
import hashlib,json,os,subprocess,time
from pathlib import Path
IDLE_REASON='CPU load exceeds idle threshold'
def sample_busy_cores(seconds=1):
    def busy():
        fields=list(map(int,Path('/proc/stat').read_text().splitlines()[0].split()[1:9]))
        return sum(fields)-fields[3]-fields[4]
    begin=time.monotonic();first=busy();time.sleep(seconds)
    return (busy()-first)/(os.sysconf('SC_CLK_TCK')*(time.monotonic()-begin))
def recent_parent_is_stopped(config):
    path=Path(config['handoff_parent_config_file']);raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=config['handoff_parent_config_sha256']:return False
    parent=json.loads(raw);state=json.loads((Path(parent['output'])/'status.json').read_bytes())
    if state['status']!='stopped' or state['error'] is not None:return False
    age=time.time()-datetime.fromisoformat(state['updated_utc']).timestamp()
    if not 0<=age<=3600:return False
    pid=state.get('worker_pid')
    if pid and Path('/proc',str(pid)).exists():return False
    done=subprocess.run(['systemctl','--user','show',parent['service_name'],'-p','ActiveState','-p','MainPID'],capture_output=True,text=True,check=True,timeout=5)
    fields=dict(line.split('=',1) for line in done.stdout.splitlines() if '=' in line)
    return fields.get('ActiveState')=='inactive' and fields.get('MainPID')=='0'
class FreshObservation:
    def __init__(self,resource):self.resource=resource
    def __getattr__(self,name):return getattr(self.resource,name)
    def blockers(self,locks,running=False):
        return [x for x in self.resource.blockers(locks,running) if x!=IDLE_REASON]
def acquire(helpers,resources,config):
    reasons=resources.blockers(resources.lock_paths())
    if IDLE_REASON not in reasons:return helpers.acquire_leases(resources,False)
    if any(x!=IDLE_REASON for x in reasons):return helpers.acquire_leases(resources,False)
    if not recent_parent_is_stopped(config):return helpers.acquire_leases(resources,False)
    cores=sample_busy_cores()
    if cores>2 or os.getloadavg()[0]>config['running_load_limit']:return helpers.acquire_leases(resources,False)
    handles,leased=helpers.acquire_leases(FreshObservation(resources),False)
    from durable_mirror import atomic
    atomic(Path(__file__).resolve().parent/'handoff-resource-check.json',dict(status='passed',method='Recent owned worker has exited; fresh one-second CPU sample replaces its residual one-minute load only',busy_cores=cores,maximum_idle_cores=2,load_average=list(os.getloadavg()),all_other_resource_and_lease_checks_retained=True,observed_epoch=time.time()))
    return handles,leased
