#!/usr/bin/env python3
"""Bounded NFS range worker. Explicit reservations, fresh journals, no services."""
import argparse,contextlib,errno,fcntl,hashlib,json,os,re,signal,subprocess,time,sys
from pathlib import Path
SOURCE='192.168.5.3:/volume1/clusterData'
MOUNT=Path('/mnt/diskBox')
GRID=dict(cmin=100000000001,cmax=200000000000,width=8,cap=42,count=11250000001)
CHUNK=256
class Busy(RuntimeError):pass
class Conflict(RuntimeError):pass
class Integrity(RuntimeError):pass

def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def digest(obj):return hashlib.sha256(canonical(obj)).hexdigest()
def verify_share(path):
    path=Path(path).resolve()
    if not path.is_relative_to(MOUNT):raise Integrity('Workspace must be on the verified NFS mount')
    ancestor=path
    while not ancestor.exists():ancestor=ancestor.parent
    fs=json.loads(subprocess.check_output(['findmnt','--json','--target',str(ancestor),'--output','TARGET,SOURCE,FSTYPE,OPTIONS'],text=True,timeout=10))['filesystems'][0]
    if fs['target']!=str(MOUNT) or fs['source']!=SOURCE or fs['fstype'] not in ('nfs','nfs4'):
        raise Integrity('Required NFS export is not mounted; refusing local fallback')
    if 'local_lock=all' in fs['options'] or 'local_lock=posix' in fs['options'] or 'nolock' in fs['options'].split(','):
        raise Integrity('Server-coherent POSIX file locking is required')
    return ancestor.stat().st_dev

def write_all(fd,data):
    while data:
        n=os.write(fd,data)
        if n<=0:raise OSError('Short write without progress')
        data=data[n:]

def validate_result(result,first,last,identity):
    if result.get('complete') is not True or (result.get('first'),result.get('last'),result.get('identity'))!=(first,last,identity):
        raise Integrity('Incomplete/changed chunk result; no coverage committed')
    if result.get('tasks')!=last-first or type(result.get('points'))!=int or not 0<=result['points']<=250000000:
        raise Integrity('Invalid chunk task/point count')
    if not re.fullmatch('[0-9a-f]{64}',result.get('certificate_sha256','')) or not result.get('exact_checks'):
        raise Integrity('Missing exact certificate attestation')
    packets=result.get('packets')
    if not isinstance(packets,list) or not packets:raise Integrity('Missing completed packets')
    for row in packets:
        if type(row.get('points'))!=int or not 0<=row['points']<=50000000 or row.get('visited')!=row['points']:
            raise Integrity('Incomplete packet count')
        for key in ('counts_sha256','packet_sha256','response_sha256'):
            if not re.fullmatch('[0-9a-f]{64}',row.get(key,'')):raise Integrity('Missing packet provenance')
    if sum(row['points'] for row in packets)!=result['points']:raise Integrity('Point total mismatch')
    if not isinstance(result.get('hits'),list):raise Integrity('Missing exact hit set')
    for h in result['hits']:
        if len(h)!=4 or any(type(x)!=int for x in h):raise Integrity('Invalid hit format')
        a,b,c,r=h
        if not (1<=a<=b<c and GRID['cmin']<=c<=GRID['cmax'] and abs(r)<=42 and a**5+b**5-c**5==r):
            raise Integrity('Invalid exact reconstructed hit')
        if not 9*first*c<=10*GRID['count']*a<=9*last*c:raise Integrity('Hit outside reserved patch range')

class Store:
    def __init__(self,root,inject=None):
        if sys.flags.optimize:raise Integrity('Ordinary Python required; -O is forbidden')
        os.umask(0o077);self.root=Path(root).resolve();self.device=verify_share(self.root);self.inject=inject or (lambda event:None)
        self.mkdir(self.root);self.mkdir(self.root/'jobs')
    def guard(self):
        if verify_share(self.root)!=self.device:raise Integrity('Mounted filesystem identity changed')
    def mkdir(self,path):
        verify_share(path);path.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(path,0o700)
    def syncdir(self,path):
        fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(fd)
        finally:os.close(fd)
    @contextlib.contextmanager
    def locked(self,path):
        self.guard();fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600);os.fchmod(fd,0o600)
        try:
            try:fcntl.lockf(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError as e:
                if e.errno in (errno.EACCES,errno.EAGAIN):raise Busy(str(path)) from e
                raise
            # NFS POSIX lock acquisition synchronizes the stable file's cache.
            yield fd
        finally:os.close(fd)
    def readfd(self,fd):
        os.lseek(fd,0,os.SEEK_SET);out=b''
        while True:
            b=os.read(fd,1024*1024)
            if not b:return out
            out+=b
            if len(out)>256*1024*1024:raise Integrity('Journal size allowance reached')
    def append(self,fd,data,event):
        self.guard();self.inject(event);os.lseek(fd,0,os.SEEK_END);write_all(fd,data);self.inject('fsync_'+event);os.fsync(fd)
    def checkpoint(self,job,state):
        self.guard();self.inject('checkpoint');directory=self.root/'jobs'/job
        temporary=directory/('checkpoint.'+str(os.getpid())+'.'+str(time.time_ns())+'.tmp')
        fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:
            os.fchmod(fd,0o600);write_all(fd,canonical(state)+b'\n');self.inject('fsync_checkpoint');os.fsync(fd)
        finally:os.close(fd)
        self.inject('replace_checkpoint');self.guard();os.replace(temporary,directory/'checkpoint.json');self.syncdir(directory)
    def claims(self,fd):
        data=self.readfd(fd)
        if data and not data.endswith(b'\n'):raise Integrity('Incomplete reservation log; offline repair required')
        rows=[]
        for line in data.splitlines():
            try:r=json.loads(line)
            except ValueError as e:raise Integrity('Invalid reservation log') from e
            if r.get('sha256')!=digest({k:v for k,v in r.items() if k!='sha256'}) or r.get('grid')!=GRID:
                raise Integrity('Invalid reservation digest/grid')
            rows.append(r)
        return rows
    def reserve(self,job,first,last,identity,coverage=None):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',job):raise ValueError('Invalid job id')
        if type(first)!=int or type(last)!=int or not 0<=first<last<=GRID['count']:raise ValueError('Invalid half-open grid range')
        if not re.fullmatch('[0-9a-f]{64}',identity):raise ValueError('Expected immutable runtime SHA256')
        with self.locked(self.root/'reservations.jsonl') as fd:
            rows=self.claims(fd)
            for r in rows:
                if r['job']==job:
                    if (r['first'],r['last'],r['identity'],r['coverage'])==(first,last,identity,coverage):return r
                    raise Conflict('Job identity/range cannot change')
                if first<r['last'] and r['first']<last:raise Conflict('Range overlaps job '+r['job'])
            r=dict(job=job,first=first,last=last,identity=identity,coverage=coverage,grid=GRID,created_ns=time.time_ns())
            r['sha256']=digest(r);self.append(fd,canonical(r)+b'\n','reservation');self.syncdir(self.root)
            self.mkdir(self.root/'jobs'/job)
            return r
    def claim(self,job):
        with self.locked(self.root/'reservations.jsonl') as fd:
            found=[r for r in self.claims(fd) if r['job']==job]
        if len(found)!=1:raise Integrity('Unknown/ambiguous reserved job')
        return found[0]
    def recover(self,fd,claim):
        data=self.readfd(fd);lines=data.splitlines(keepends=True)
        if lines and not lines[-1].endswith(b'\n'):
            tail=lines.pop();directory=self.root/'jobs'/claim['job'];orphan=directory/('uncommitted-tail.'+str(time.time_ns())+'.bin')
            self.guard();out=os.open(orphan,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            try:os.fchmod(out,0o600);write_all(out,tail);os.fsync(out)
            finally:os.close(out)
            self.syncdir(directory);os.ftruncate(fd,len(data)-len(tail));os.fsync(fd)
        previous='0'*64;next_patch=claim['first'];chunks=0;hits=set()
        for line in lines:
            try:r=json.loads(line)
            except ValueError as e:raise Integrity('Invalid full journal record') from e
            payload={k:v for k,v in r.items() if k!='sha256'}
            if r.get('sha256')!=digest(payload) or r.get('previous')!=previous or r.get('claim_sha256')!=claim['sha256']:
                raise Integrity('Journal chain or provenance mismatch')
            if r['first']!=next_patch or r['last']!=min(next_patch+CHUNK,claim['last']) or r['sequence']!=chunks+1:
                raise Integrity('Non-contiguous/overlapping journal chunk')
            validate_result(r['result'],r['first'],r['last'],claim['identity'])
            next_patch=r['last'];chunks+=1;previous=r['sha256'];hits.update(tuple(h) for h in r['result']['hits'])
        return dict(schema=1,job=claim['job'],claim_sha256=claim['sha256'],identity=claim['identity'],grid=GRID,first=claim['first'],last=claim['last'],next_patch=next_patch,chunks=chunks,journal_sha256=previous,hits=sorted(hits),complete=next_patch==claim['last'])
    def run(self,job,identity,evaluate,stop=lambda:False,max_chunks=None):
        claim=self.claim(job)
        if identity!=claim['identity']:raise Integrity('Changed source/runtime requires a fresh job and journal')
        self.mkdir(self.root/'jobs'/job)
        with self.locked(self.root/'jobs'/job/'journal.jsonl') as fd:
            state=self.recover(fd,claim)
            # Journal is authoritative; recover a fully durable chunk even if
            # checkpoint replacement failed. Never trust a cached NFS checkpoint.
            self.checkpoint(job,state);done=0
            while state['next_patch']<claim['last'] and not stop() and (max_chunks is None or done<max_chunks):
                first=state['next_patch'];last=min(first+CHUNK,claim['last'])
                self.inject('before_evaluate');result=evaluate(first,last)
                validate_result(result,first,last,identity)
                record=dict(sequence=state['chunks']+1,claim_sha256=claim['sha256'],previous=state['journal_sha256'],first=first,last=last,result=result)
                record['sha256']=digest(record)
                self.append(fd,canonical(record)+b'\n','journal')
                state=dict(state,next_patch=last,chunks=state['chunks']+1,journal_sha256=record['sha256'],hits=sorted(set(map(tuple,state['hits']))|set(map(tuple,result['hits']))),complete=last==claim['last'])
                self.checkpoint(job,state);done+=1;self.inject('after_checkpoint')
            return state

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',required=True)
    sub=ap.add_subparsers(dest='action',required=True)
    reserve=sub.add_parser('reserve');reserve.add_argument('--job',required=True);reserve.add_argument('--first',type=int,required=True);reserve.add_argument('--last',type=int,required=True);reserve.add_argument('--identity',required=True);reserve.add_argument('--coverage-file',help='Verified handoff metadata; linked by SHA256, never imported as journal coverage')
    run=sub.add_parser('run');run.add_argument('--job',required=True);run.add_argument('--identity',required=True);run.add_argument('--max-chunks',type=int);run.add_argument('command',nargs=argparse.REMAINDER,help='Explicit evaluator command; stdin one range JSON, stdout one complete result JSON')
    args=ap.parse_args();store=Store(args.root)
    if args.action=='reserve':
        coverage=None
        if args.coverage_file:
            data=Path(args.coverage_file).read_bytes();coverage=dict(sha256=hashlib.sha256(data).hexdigest(),manifest=json.loads(data))
        print(json.dumps(store.reserve(args.job,args.first,args.last,args.identity,coverage)));return
    command=args.command
    if command and command[0]=='--':command=command[1:]
    if not command:ap.error('Explicit chunk evaluator command required')
    requested=[False]
    def stop(signum,frame):requested[0]=True
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    def evaluate(first,last):
        request=dict(first=first,last=last,grid=GRID,identity=args.identity)
        p=subprocess.run(command,input=json.dumps(request),text=True,capture_output=True,timeout=600)
        if p.returncode:raise RuntimeError('Chunk evaluator failed; no checkpoint advancement: '+p.stderr[-4096:])
        if len(p.stdout)>16*1024*1024:raise Integrity('Evaluator output allowance exceeded')
        return json.loads(p.stdout)
    print(json.dumps(store.run(args.job,args.identity,evaluate,lambda:requested[0],args.max_chunks)))
if __name__=='__main__':main()
