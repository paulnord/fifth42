"""Bounded multiwindow preparation with explicit ready depth and wait timings."""
from collections import Counter,deque
import threading,time
import buffered_pipeline as b

class DispatchPool:
    def __init__(self,pool,chunksize):self.pool,self.chunksize=pool,chunksize
    def map(self,function,items,ignored):return self.pool.map_async(function,items,self.chunksize).get(timeout=25)

class CompletedPool:
    def __init__(self,args,rows):self.args,self.rows=args,rows
    def map(self,function,items,ignored):
        b.require(function is b.coverage.prepare_segment and list(items)==self.args,'Prepared window was assigned different segment work')
        return self.rows

def segment_args(window,group_limit):
    return [(window.lo,window.hi,first,min(first+group_limit,window.last),window.bits,window.cap,window.geometry_policy)
            for first in range(window.first,window.last,group_limit)]

def prepare_many(pool,windows,group_limit,cache=True):
    prepare=b.prepare_cached if cache else b.coverage.prepare_chunk
    if len(windows)==1:
        yield prepare(pool,windows[0],group_limit);return
    arguments=[segment_args(window,group_limit) for window in windows]
    flat=[arg for group in arguments for arg in group]
    rows=pool.map(b.coverage.prepare_segment,flat,8);offset=0
    for window,args in zip(windows,arguments):
        part=rows[offset:offset+len(args)];offset+=len(args)
        yield prepare(CompletedPool(args,part),window,group_limit)
    b.require(offset==len(rows),'Prepared multiwindow segment count changed')

class ReadyQueue:
    def __init__(self,windows,prepare,*,batch=1,ready_limit=3,active_limit=1,max_item_bytes=8*1024**2,max_item_points=250_000_000):
        b.require(batch in (1,2,4) and 1<=ready_limit<=8 and 1<=active_limit<=5,'Invalid queue bounds')
        self.windows=list(windows);self.prepare=prepare;self.batch=batch;self.ready_limit=ready_limit
        self.max_outstanding=batch+ready_limit+active_limit
        self.max_item_bytes,self.max_item_points=max_item_bytes,max_item_points
        self.condition=threading.Condition();self.ready=deque();self.active={};self.inflight=0;self.outstanding=0
        self.peak=0;self.peak_ready=0;self.error=None;self.done=False;self.stopping=False;self.thread=None
        self.empty_wait=self.full_wait=self.capacity_wait=0.;self.depth_time=Counter();self.started=self.last_touch=None
        self.prepare_seconds=0.;self.preparation_batches=0;self.max_prepared_payload=0
    def touch(self):
        now=time.monotonic()
        if self.last_touch is not None:self.depth_time[len(self.ready)]+=now-self.last_touch
        self.last_touch=now
    def __enter__(self):self.start();return self
    def __exit__(self,*args):self.close()
    def start(self):
        with self.condition:
            if self.thread is None:
                self.started=self.last_touch=time.monotonic();self.thread=threading.Thread(target=self.run,daemon=True,name='measured-preparation');self.thread.start()
    def run(self):
        offset=0
        try:
            while offset<len(self.windows):
                count=min(self.batch,len(self.windows)-offset)
                with self.condition:
                    began=time.monotonic();self.condition.wait_for(lambda:self.stopping or self.outstanding+count<=self.max_outstanding)
                    self.capacity_wait+=time.monotonic()-began
                    if self.stopping:return
                    self.touch();self.inflight+=count;self.outstanding+=count;self.peak=max(self.peak,self.outstanding)
                group=self.windows[offset:offset+count];offset+=count;began=time.monotonic();produced=0
                for chunk in self.prepare(group):
                    b.require(chunk.payload_bytes<=self.max_item_bytes and chunk.plan.points<=self.max_item_points,'Prepared item exceeds memory/point budget')
                    self.max_prepared_payload=max(self.max_prepared_payload,chunk.payload_bytes)
                    with self.condition:
                        waiting=time.monotonic();self.condition.wait_for(lambda:self.stopping or len(self.ready)<self.ready_limit)
                        self.full_wait+=time.monotonic()-waiting
                        if self.stopping:return
                        self.touch();self.ready.append(chunk);self.inflight-=1;produced+=1
                        self.peak_ready=max(self.peak_ready,len(self.ready));self.condition.notify_all()
                b.require(produced==count,'Preparation did not produce each original window')
                self.prepare_seconds+=time.monotonic()-began;self.preparation_batches+=1
        except BaseException as exc:
            with self.condition:self.error=exc
        finally:
            with self.condition:self.done=True;self.condition.notify_all()
    def __iter__(self):self.start();return self
    def __next__(self):return self.get()
    def get(self):
        self.start()
        with self.condition:
            began=time.monotonic();self.condition.wait_for(lambda:self.ready or self.done or self.stopping)
            self.empty_wait+=time.monotonic()-began
            if not self.ready:
                if self.error:raise self.error
                raise StopIteration
            self.touch();chunk=self.ready.popleft();self.active[id(chunk)]=chunk;self.condition.notify_all();return chunk
    def ack(self,chunk):
        with self.condition:
            b.require(self.active.pop(id(chunk),None) is chunk,'Unknown/duplicate prepared-buffer release')
            self.touch();self.outstanding-=1;self.condition.notify_all()
    def snapshot(self):
        with self.condition:
            self.touch();elapsed=time.monotonic()-self.started if self.started else 0
            return dict(ready=len(self.ready),inflight=self.inflight,active=len(self.active),outstanding=self.outstanding,
               peak_outstanding=self.peak,peak_ready=self.peak_ready,ready_limit=self.ready_limit,
               reserved_bytes=self.outstanding*self.max_item_bytes,peak_reserved_bytes=self.peak*self.max_item_bytes,
               max_outstanding=self.max_outstanding,consumer_wait_empty_seconds=self.empty_wait,
               producer_wait_full_seconds=self.full_wait,producer_wait_capacity_seconds=self.capacity_wait,
               ready_depth_seconds=dict(self.depth_time),mean_ready_depth=sum(depth*seconds for depth,seconds in self.depth_time.items())/max(elapsed,1e-9),
               elapsed_seconds=elapsed,preparation_batches=self.preparation_batches,prepare_wall_seconds=self.prepare_seconds,
               maximum_prepared_payload_bytes=self.max_prepared_payload)
    def close(self):
        with self.condition:self.touch();self.stopping=True;self.condition.notify_all()
        if self.thread is not None:
            self.thread.join(30)
            if self.thread.is_alive():raise TimeoutError('Preparation did not stop within its resource bound')
        with self.condition:
            self.touch();self.ready.clear();self.active.clear();self.inflight=self.outstanding=0
