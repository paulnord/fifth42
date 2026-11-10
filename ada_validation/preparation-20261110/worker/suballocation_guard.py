"""Parent-lease protected, disjoint subclaims; no arithmetic or coverage changes."""
import errno,fcntl,hashlib,json,os,time
from pathlib import Path
import ada_export_store
GLOBAL=Path('/mnt/nfs_share/fifth42-shared-20261107')
TEST=Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada/suballocation-tests')
def require(ok,message):
    if not ok:raise RuntimeError(message)
def read(path):return json.loads(Path(path).read_bytes())
def digest(raw):return hashlib.sha256(raw).hexdigest()
def locked_by_other(path):
    fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW)
    try:
        try:fcntl.lockf(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as e:
            if e.errno in (errno.EACCES,errno.EAGAIN):return True
            raise
        fcntl.lockf(fd,fcntl.LOCK_UN);return False
    finally:os.close(fd)
def load_grant(path,expected_sha,test=False):
    path=Path(path);raw=path.read_bytes();require(digest(raw)==expected_sha,'Suballocation grant changed')
    g=json.loads(raw)
    require(g['schema']=='fifth42-parent-suballocation-v1' and g['TEST_ONLY'] is test,'Wrong suballocation schema/scope')
    parent=Path(g['parent_ledger']);child=Path(g['child_ledger'])
    require(parent.is_relative_to(TEST) if test else parent==GLOBAL,'Wrong parent ledger namespace')
    require(child.is_relative_to(parent/'suballocations') and child!=parent,'Child ledger escaped parent namespace')
    require(g['stop_epoch']>time.time() and (test or g['stop_epoch'] in (1794351600,1794438000)),'Suballocation cutoff expired/changed')
    a,z=g['assignments']['ada'],g['assignments']['boole']
    require(all(type(x) is int for x in [*a,*z,g['parent_first'],g['parent_last']]),'Noninteger suballocation boundary')
    require(g['parent_first']<=a[0]<a[1]==z[0]<z[1]==g['parent_last'],'Suballocation has a gap, overlap or overflow')
    require(g['coverage_claimed'] is False,'Allocation is not completed coverage')
    return g
def check(config,force=False,observer_role=None):
    test=config.get('TEST_ONLY') is True
    path=Path(config['suballocation_grant_file']);expected=config['suballocation_grant_sha256']
    g=load_grant(path,expected,test)
    role=config['allocation_role'];require(role in ('ada','boole'),'Unknown suballocation role')
    if not test:
        if observer_role is None:require(os.uname().nodename.split('.')[0]==role,'Wrong suballocation host')
        else:require(observer_role==role and os.uname().nodename.split('.')[0]=='ada','Invalid read-only observer role')
    require(Path(config['ledger_root'])==Path(g['child_ledger']),'Wrong child ledger')
    first,last=g['assignments'][role]
    require(first<=config['initial_patch']<config['range_end']<=last,'Worker escaped its delegated interval')
    require(config['stop_epoch']==g['stop_epoch'],'Worker changed delegated cutoff')
    state_name=g.get('coordinator_state_file','coordinator-state.json');require(Path(state_name).name==state_name,'Invalid coordinator state filename')
    state=read(Path(g['child_ledger'])/state_name)
    require(state['grant_sha256']==expected and state['stop_epoch']==g['stop_epoch'],'Coordinator generation changed')
    require(-5<=time.time()-state['updated_epoch']<=10,'Coordinator heartbeat is stale')
    require(state['status']=='active' or (role=='ada' and state['status']=='prepared'),'Suballocation is not active')
    require(state['retained_range_end']==g['assignments']['ada'][1],'Retained worker cap changed')
    if not test and role=='boole':
        require((state.get('activation_audit') or {}).get('status')=='passed','Retained native/GMP prefix has not been independently checked')
        ready_name=g.get('ready_file','READY.json');require(Path(ready_name).name==ready_name,'Invalid grant readiness filename')
        ready=read(Path(g['child_ledger'])/ready_name)
        require(ready['status']=='active_delegation_ready' and ready['grant_sha256']==expected,'Delegation handoff has not been admitted')
    require(locked_by_other(Path(g['parent_ledger'])/'jobs'/g['parent_job']/'journal.jsonl'),'Exclusive parent lease is absent')
    return g
