"""Shared-memory GPU proposals; unchanged exact CPU certification and fallback."""
from pathlib import Path
from types import SimpleNamespace
from collections import Counter
import ctypes,multiprocessing as mp,queue,sys,threading,time
from multiprocessing import shared_memory
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'worker'),str(ROOT/'worker/source/lattice_gpu'),str(ROOT/'gpu_candidate')]
import candidate_reduction as candidate
import runtime_initialize,scaling_core as core,width_coverage as coverage,scheduling
DTYPE=np.dtype([('u','<i8',(9,)),('status','<i4'),('steps','<i4')])
assert DTYPE.itemsize==ctypes.sizeof(candidate.Output)==80
_MEM=[];_INPUT=_OUTPUT=_EVENTS=_READY=None;_SLOT=0;_LLL=True
def initialize(source,cpus,names,workers,capacity,events,ready,slots,require_lll=True):
 global _INPUT,_OUTPUT,_EVENTS,_READY,_SLOT,_LLL
 runtime_initialize.initialize(source,cpus)
 _MEM.extend(shared_memory.SharedMemory(name=name) for name in names)
 _INPUT=np.ndarray((workers,capacity,18),dtype=np.float64,buffer=_MEM[0].buf)
 _OUTPUT=np.ndarray((workers,capacity),dtype=DTYPE,buffer=_MEM[1].buf)
 _EVENTS,_READY,_LLL=events,ready,require_lll
 _SLOT=slots.get(timeout=2) # Unique lifetime ownership; replacement workers fail closed.
def prepare_block(arguments):
 start=time.perf_counter();cpu_start=time.process_time();prepared=[];event=_EVENTS[_SLOT];event.clear()
 for i,args in enumerate(arguments):
  lo,hi,first,last,bits,cap,geometry=args;spec=coverage.specification(*args)
  try:
   patch,a=candidate.patch_basis(spec);dd=candidate.double_double(a)
   prepared.append((args,spec,patch,a,None));_INPUT[_SLOT,i]=dd
  except (ValueError,ArithmeticError) as exc:
   prepared.append((args,spec,None,None,str(exc)));_INPUT[_SLOT,i]=np.array([v for i in range(3) for j in range(3) for v in (float(i==j),0.)])
 geometry_seconds=time.perf_counter()-start;_READY.put((_SLOT,len(arguments)))
 began=time.perf_counter()
 if not event.wait(30):raise TimeoutError('GPU preparation response timed out')
 wait_seconds=time.perf_counter()-began;parts=[];reasons=Counter();accepted=0;certify_seconds=0
 for i,(args,spec,patch,a,error) in enumerate(prepared):
  proposal=_OUTPUT[_SLOT,i]
  if int(proposal['status'])==99:raise RuntimeError('GPU preparation service failed')
  began=time.perf_counter()
  try:
   if error is not None:raise ValueError(error)
   if int(proposal['status']):raise ValueError(candidate.STATUS.get(int(proposal['status']),'unknown GPU status'))
   u=tuple(tuple(int(v) for v in proposal['u'][3*j:3*j+3]) for j in range(3))
   task,token=candidate.certify_transform(spec,u,patch,a,require_lll=_LLL)
   elapsed=time.perf_counter()-began;certify_seconds+=elapsed
   parts.append([(task,token,(geometry_seconds/len(arguments),0.,elapsed,0.),args[2],args[3],spec)]);accepted+=1
  except (ValueError,ArithmeticError) as exc:
   reasons[str(exc)]+=1;parts.append(coverage.prepare_segment(args));certify_seconds+=time.perf_counter()-began
 return dict(parts=parts,accepted=accepted,fallbacks=dict(reasons),geometry_seconds=geometry_seconds,wait_seconds=wait_seconds,certify_seconds=certify_seconds,cpu_seconds=time.process_time()-cpu_start)
class GPUStage:
 def __init__(self,workers,capacity=128,require_lll=True):
  self.workers,self.capacity,self.require_lll=workers,capacity,require_lll;ctx=mp.get_context('spawn')
  self.memory=[shared_memory.SharedMemory(create=True,size=workers*capacity*18*8),shared_memory.SharedMemory(create=True,size=workers*capacity*DTYPE.itemsize)]
  self.inputs=np.ndarray((workers,capacity,18),dtype=np.float64,buffer=self.memory[0].buf)
  self.outputs=np.ndarray((workers,capacity),dtype=DTYPE,buffer=self.memory[1].buf);self.outputs['status']=99
  self.events=[ctx.Event() for _ in range(workers)];self.ready=ctx.Queue();self.slots=ctx.Queue()
  for slot in range(workers):self.slots.put(slot)
  self.stop=threading.Event();self.error=None;self.thread=None;self.gpu=None
  self.metrics=dict(gpu_batches=0,gpu_proposals=0,kernel_ms=0.,cuda_transfer_and_kernel_ms=0.,accepted=0,fallbacks={},worker_geometry_seconds=0.,worker_wait_seconds=0.,worker_certify_seconds=0.,worker_cpu_seconds=0.)
 def initargs(self,source,cpus):return(source,cpus,[p.name for p in self.memory],self.workers,self.capacity,self.events,self.ready,self.slots,self.require_lll)
 def start(self):
  self.gpu=candidate.GPUCandidates(capacity=self.workers*self.capacity);self.thread=threading.Thread(target=self.serve,daemon=True);self.thread.start()
 def serve(self):
  try:
   while not self.stop.is_set():
    try:first=self.ready.get(timeout=.05)
    except queue.Empty:continue
    messages=[first];end=time.monotonic()+.003
    while len(messages)<self.workers and time.monotonic()<end:
     try:messages.append(self.ready.get(timeout=max(.00001,end-time.monotonic())))
     except queue.Empty:break
    if len({slot for slot,_ in messages})!=len(messages) or any(type(slot) is not int or type(n) is not int or not 0<=slot<self.workers or not 1<=n<=self.capacity for slot,n in messages):raise ValueError('Invalid or duplicate GPU preparation request')
    count=sum(n for _,n in messages);flat=np.empty((count,18),dtype=np.float64);at=0
    for slot,n in messages:flat[at:at+n]=self.inputs[slot,:n];at+=n
    out,timing=self.gpu.reduce_flat(flat,count,raw=True);view=np.frombuffer(out,dtype=DTYPE,count=count);at=0
    for slot,n in messages:self.outputs[slot,:n]=view[at:at+n];at+=n;self.events[slot].set()
    self.metrics['gpu_batches']+=1;self.metrics['gpu_proposals']+=count
    for key in ['kernel_ms','cuda_transfer_and_kernel_ms']:self.metrics[key]+=timing[key]
  except BaseException as exc:
   self.error=exc;self.outputs['status']=99
   for event in self.events:event.set()
 def dispatch(self,pool,arguments):
  size=max(1,min(self.capacity,(len(arguments)+self.workers-1)//self.workers))
  blocks=[arguments[i:i+size] for i in range(0,len(arguments),size)]
  pids=tuple(p.pid for p in pool._pool);deadline=time.monotonic()+25
  pending=pool.map_async(prepare_block,blocks,1)
  while not pending.ready():
   if tuple(p.pid for p in pool._pool)!=pids or any(not p.is_alive() for p in pool._pool):raise RuntimeError('Preparation worker died or was replaced')
   if time.monotonic()>deadline:raise TimeoutError('GPU dispatch exceeded25second bound')
   if self.error:raise RuntimeError('GPU preparation service failed') from self.error
   pending.wait(.05)
  rows=pending.get();parts=[]
  for row in rows:
   parts.extend(row['parts']);self.metrics['accepted']+=row['accepted']
   for key,value in row['fallbacks'].items():self.metrics['fallbacks'][key]=self.metrics['fallbacks'].get(key,0)+value
   for src,dst in [('geometry_seconds','worker_geometry_seconds'),('wait_seconds','worker_wait_seconds'),('certify_seconds','worker_certify_seconds'),('cpu_seconds','worker_cpu_seconds')]:self.metrics[dst]+=row[src]
  if self.error:raise RuntimeError('GPU preparation service failed') from self.error
  return parts
 def close(self):
  self.stop.set()
  if self.thread:self.thread.join(5);assert not self.thread.is_alive()
  if self.gpu:self.gpu.close()
  del self.inputs,self.outputs
  for p in self.memory:p.close();p.unlink()
  self.ready.cancel_join_thread();self.ready.close();self.slots.cancel_join_thread();self.slots.close()
class GPUPool:
 def __init__(self,pool,stage,chunksize):self.pool,self.stage,self.chunksize=pool,stage,chunksize
 def map(self,function,items,ignored):
  if function is coverage.prepare_segment:return self.stage.dispatch(self.pool,list(items))
  return self.pool.map(function,items,self.chunksize)
class BulkStream:
 """Bounded preparation batches; execution/coverage remain one window at a time."""
 def __init__(self,windows,prepare_many,batch_windows):
  def groups():
   pending=[]
   for window in windows:
    pending.append(window)
    if len(pending)==batch_windows:yield tuple(pending);pending=[]
   if pending:yield tuple(pending)
  def prepare(groups):
   for group in groups:
    chunks=tuple(prepare_many(group));yield SimpleNamespace(chunks=chunks,payload_bytes=sum(c.payload_bytes for c in chunks),plan=SimpleNamespace(points=sum(c.plan.points for c in chunks)))
  self.queue=scheduling.ReadyQueue(groups(),prepare,batch=1,ready_limit=3 if batch_windows==1 else 1,active_limit=1,max_item_bytes=8*1024**2 if batch_windows==1 else 12*1024**2,max_item_points=core.MAX_TOTAL_POINTS*batch_windows)
  self.batch_windows=batch_windows;self.current=None;self.index=0
 def __enter__(self):self.queue.start();return self
 def __exit__(self,*args):self.close()
 def __iter__(self):return self
 def __next__(self):
  if self.current is None:self.current=self.queue.get();self.index=0
  return self.current.chunks[self.index]
 def ack(self,chunk):
  assert self.current.chunks[self.index] is chunk;self.index+=1
  if self.index==len(self.current.chunks):self.queue.ack(self.current);self.current=None
 def snapshot(self):return dict(self.queue.snapshot(),preparation_batch_windows=self.batch_windows,queue_units='bounded preparation batches; native requests and journals stay 256 logical cells')
 def close(self):self.queue.close();self.current=None
