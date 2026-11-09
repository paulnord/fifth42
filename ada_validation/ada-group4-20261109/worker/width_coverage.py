"""Certified wider physical patches over the unchanged width-8 reservation grid.

The checkpoint cursor always names the ORIGINAL fine grid. Every physical task
records the exact contiguous interval of original cells that it covers. This
uses an explicit journal schema; physical task counts are never fine-cell counts.
"""
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import os
import re
import threading
import time

import coordinator_pipeline as pipeline
import coordinator_packing
import overnight_search as night
import precision_policy
import scaling_core as core

SCHEMA='logical-width8-physical-groups-v1'


def require(ok,message):
    if not ok:raise ValueError(message)


def edge(lo,index):
    return Fraction(9*index,10*night.grid_count(lo,8)).as_integer_ratio()


def specification(lo,hi,first,last,bits,cap,geometry):
    left,right=edge(lo,first),edge(lo,last)
    actual=bits if geometry=='baseline' else precision_policy.geometry_bits(core.lattice(),lo,hi,core.lattice().Q(*left),core.lattice().Q(*right),cap)
    return (first,lo,hi,left,right,cap,actual)


def prepare_segment(args):
    lo,hi,first,last,bits,cap,geometry=args
    spec=specification(lo,hi,first,last,bits,cap,geometry)
    try:
        row=pipeline.prepare_certified(spec)
        return [(*row,first,last,spec)]
    except pipeline.GuardedPatch:
        if last-first==1:raise
        middle=first+(last-first)//2
        return prepare_segment((lo,hi,first,middle,bits,cap,geometry))+prepare_segment((lo,hi,middle,last,bits,cap,geometry))


@dataclass(frozen=True)
class Window(pipeline.Window):
    group_limit:int=1
    explicit_specs:tuple=()
    spans:tuple=()

    def specifications(self):
        require(self.explicit_specs,'Prepared grouped window has no certified specifications')
        return self.explicit_specs


def prepare_chunk(pool,window,group_limit):
    require(window.width==8 and group_limit in (1,2,4),'Unsupported reservation/grouping policy')
    args=[(window.lo,window.hi,first,min(first+group_limit,window.last),window.bits,window.cap,window.geometry_policy)
          for first in range(window.first,window.last,group_limit)]
    rows=[row for part in pool.map(prepare_segment,args,8) for row in part]
    specs=tuple(row[5] for row in rows);tasks=[row[0] for row in rows];tokens=[row[1] for row in rows]
    spans=tuple((row[3],row[4]) for row in rows)
    view=Window(window.lo,window.hi,window.first,window.last,8,window.bits,window.cap,window.geometry_policy,
                group_limit,specs,spans)
    plan,geometry,payload=coordinator_packing.assemble_with_geometry(window.hi,window.cap,specs,(),tasks,tokens)
    return pipeline.PreparedChunk(view,plan,tuple((task.id,token,task.points) for task,token in zip(tasks,tokens)),
                                  geometry,payload,{},tuple(row[2] for row in rows))


def add_coverage(record,chunk,group_limit):
    record.update(coverage_schema=SCHEMA,group_limit=group_limit,
                  logical_spans=chunk.window.spans,
                  physical_specifications=chunk.window.explicit_specs)
    return record


class TrialJournal(pipeline.TrialJournal):
    def __init__(self,directory,identity,window):
        super().__init__(directory,identity,window)
        if self.state['chunks']:
            require(self.state.get('coverage_schema')==SCHEMA,'Cannot append to a different coverage schema')
        else:
            self.state.update(coverage_schema=SCHEMA,physical_tasks=0)

    def _validate(self,record,cursor):
        w=record['window'];base=self.window
        require(record.get('coverage_schema')==SCHEMA and record.get('group_limit')==base.group_limit,'Coverage schema or grouping policy changed')
        require(all(w[k]==getattr(base,{'lo':'lo','hi':'hi'}.get(k,k)) for k in ('lo','hi','width','bits','cap','geometry_policy')),'Grouped window changed arithmetic')
        require(w['first']==cursor and cursor<w['last']<=base.last and w['width']==8,'Logical coverage gap, duplicate or overflow')
        spans=record['logical_spans'];patches=record['patches'];specs=record['physical_specifications']
        require(len(spans)==len(patches)==len(specs)>0,'Missing physical coverage specifications')
        fine=cursor
        for span,patch,spec in zip(spans,patches,specs):
            first,last=span
            require(type(first) is int and type(last) is int and first==fine and 0<last-first<=base.group_limit,'Grouped task has a gap, overlap or invalid size')
            require(last<=w['last'] and patch[0]==spec[0]==first,'Physical task identity differs from logical start')
            require(spec[1:3]==[w['lo'],w['hi']] if isinstance(spec,list) else spec[1:3]==(w['lo'],w['hi']),'Physical task shell changed')
            require(tuple(spec[3])==edge(w['lo'],first) and tuple(spec[4])==edge(w['lo'],last),'Physical patch does not exactly cover its original cells')
            require(spec[5]==w['cap'] and type(spec[6]) is int and 48<=spec[6]<=w['bits'],'Physical precision/cap changed')
            require(isinstance(patch[1],str) and re.fullmatch('[0-9a-f]{64}',patch[1]) and type(patch[2]) is int and patch[2]>0,'Invalid physical certificate/point count')
            fine=last
        require(fine==w['last'],'Physical tasks do not cover the full logical interval')
        ids=[row[0] for row in patches]
        require([row[0] for row in record['precision_bits']]==ids and [row[1] for row in record['precision_bits']]==[s[6] for s in specs],'Physical precision manifest changed')
        batches=record['batches']
        require(record.get('complete') is True and record['points']==sum(p[2] for p in patches),'Incomplete grouped coefficient coverage')
        require([p for b in batches for p in b['patch_ids']]==ids and sum(b['points'] for b in batches)==record['points'],'Physical batch coverage mismatch')
        require([tuple(c) for b in batches for c in b['native_counts']]==[(p[0],p[2],p[2]) for p in patches],'Native physical point visits are incomplete')
        for index,batch in enumerate(batches):
            require(batch['identity']['window']==w and batch['identity']['batch']==index and batch['identity']['trial']==self.identity['trial'],'Stale grouped native identity')

    def commit(self,record):
        if self.lock.closed:raise RuntimeError('Journal is closed')
        if self.poisoned:raise RuntimeError('Durable write failed; explicit recovery required')
        if threading.get_ident()!=self.owner:raise RuntimeError('Only the journal owner may commit')
        self._validate(record,self.state['next_patch'])
        raw,digest=night.encode_record(self.state['journal_sha256'],dict(record,sequence=self.state['chunks']+1))
        try:
            with self.journal.open('ab') as stream:
                stream.write(raw);stream.flush();os.fsync(stream.fileno());offset=stream.tell()
            state=dict(self.state,next_patch=record['window']['last'],chunks=self.state['chunks']+1,
                       points=self.state['points']+record['points'],
                       patches=self.state['patches']+record['window']['last']-record['window']['first'],
                       physical_tasks=self.state.get('physical_tasks',0)+len(record['patches']),
                       hits=sorted(set(map(tuple,self.state['hits']))|set(map(tuple,record['hits']))),
                       journal_offset=offset,journal_sha256=digest)
            night.atomic_json(self.checkpoint,state)
        except BaseException:
            self.poisoned=True;raise
        self.state=state
