"""GPU proposes U; exact existing CPU certificates alone admit tasks."""
from pathlib import Path
import ctypes,hashlib,math,sys,time
from math import prod
WORKER=Path(__file__).resolve().parent.parent/'worker'
sys.path[:0]=[str(WORKER),str(WORKER/'source/lattice_gpu')]
import scaling_core as core
import exact_host_opt as host
import overnight_search as night
import runtime_initialize
STATUS={0:'candidate',1:'iteration_budget',2:'integer_overflow_or_oversize_quotient',3:'ill_conditioned_or_nonpositive_norm',4:'nonfinite_input'}
def initialize():runtime_initialize.initialize(WORKER/'source/lattice_prototype')
def patch_basis(spec):
 ident,lo,hi,left,right,cap,bits=spec;l=core.lattice();patch=l.make_patch(lo,hi,l.Q(*left),l.Q(*right),cap,bits);return patch,patch.basis()
def double_double(matrix):
 l=core.lattice();values=[]
 for row in matrix:
  for value in row:
   high=float(value)
   if not math.isfinite(high) or (high==0 and value!=0):raise ValueError('floating-input-unrepresentable')
   low=float(value-l.Q(high))
   if not math.isfinite(low):raise ValueError('floating-input-unrepresentable')
   values.extend([high,low])
 return values
def is_exact_lll(b):
 l=core.lattice();mu,norms=l.gram_schmidt(b)
 return all(abs(mu[i][j])<=l.Q(1,2) for i in range(3) for j in range(i)) and all(norms[k]>=(l.Q(3,4)-mu[k][k-1]**2)*norms[k-1] for k in (1,2))
def certify_transform(spec,u,patch=None,a=None,require_lll=True):
 # CPU recomputes B from the integer proposal. No GPU basis/bound is trusted.
 if len(u)!=3 or any(len(row)!=3 for row in u):raise ValueError('Invalid transform shape')
 if any(type(v) is not int or abs(v)>core.MAX_I64 for row in u for v in row):raise ValueError('Invalid integer transform')
 l=core.lattice()
 if abs(l.det3(u))!=1:raise ValueError('Transform is not unimodular')
 if patch is None or a is None:patch,a=patch_basis(spec)
 b=l.matmul(u,a)
 if require_lll and not is_exact_lll(b):raise ValueError('Exact LLL performance gate failed')
 j=host.bounds(patch,b,u);ident,lo,hi,left,right,cap,bits=spec
 task=core.Task(ident,lo,hi,left,right,cap,bits,tuple(tuple(row) for row in u),j,prod(2*x+1 for x in j),core.wire(a),core.wire(b))
 if not night.native_safe(task):raise ValueError('Native range/point guard rejected candidate')
 token=host.certify_task(task) # Existing independent reconstruction and checks.
 return task,token
class Output(ctypes.Structure):_fields_=[('u',ctypes.c_int64*9),('status',ctypes.c_int32),('steps',ctypes.c_int32)]
def flat_buffer(values,count,capacity):
 """Validate shape/dtype and retain an owning reference for the native call."""
 if type(count) is not int or not 1<=count<=capacity:raise ValueError('GPU batch outside capacity')
 try:view=memoryview(values)
 except TypeError:
  if len(values)!=18*count:raise ValueError('Expected 18 doubles per input basis')
  data=(ctypes.c_double*(18*count))(*values);return data,data
 if not view.c_contiguous:raise ValueError('Input doubles must be contiguous')
 if view.format not in ('d','=d','<d') or view.itemsize!=8:raise ValueError('Input must use native little-endian float64')
 if view.nbytes!=18*count*8:raise ValueError('Expected 18 doubles per input basis')
 array=ctypes.c_double*(18*count)
 data=array.from_buffer_copy(view) if view.readonly else array.from_buffer(view)
 return data,view
class GPUCandidates:
 def __init__(self,library=None,capacity=65536,maxsteps=512):
  self.library=ctypes.CDLL(str(library or Path(__file__).with_name('libgpu_lll.so')))
  lib=self.library;lib.gpu_lll_create.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int)];lib.gpu_lll_create.restype=ctypes.c_void_p
  lib.gpu_lll_run.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(Output),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)];lib.gpu_lll_run.restype=ctypes.c_int
  lib.gpu_lll_destroy.argtypes=[ctypes.c_void_p];lib.gpu_lll_error.argtypes=[ctypes.c_int];lib.gpu_lll_error.restype=ctypes.c_char_p
  error=ctypes.c_int();self.context=lib.gpu_lll_create(capacity,maxsteps,ctypes.byref(error));self.capacity=capacity
  if not self.context:raise RuntimeError(lib.gpu_lll_error(error.value).decode())
 def close(self):
  if self.context:self.library.gpu_lll_destroy(self.context);self.context=None
 def __enter__(self):return self
 def __exit__(self,*args):self.close()
 def reduce(self,bases):
  if not 1<=len(bases)<=self.capacity:raise ValueError('GPU batch outside capacity')
  values=[x for basis in bases for x in double_double(basis)];array=(ctypes.c_double*len(values))(*values);out=(Output*len(bases))();kernel=ctypes.c_double();wall=ctypes.c_double()
  error=self.library.gpu_lll_run(self.context,array,len(bases),out,ctypes.byref(kernel),ctypes.byref(wall))
  if error:raise RuntimeError(self.library.gpu_lll_error(error).decode())
  return [dict(U=tuple(tuple(int(row.u[3*i+j]) for j in range(3)) for i in range(3)),status=STATUS.get(row.status,'unknown'),status_code=row.status,steps=row.steps) for row in out],dict(kernel_ms=kernel.value,cuda_transfer_and_kernel_ms=wall.value)
 def reduce_flat(self,dd_values,count,*,raw=False):
  """Consume precomputed [basis][entry][high,low] float64 buffers.

  Writable contiguous memory (including NumPy shared-memory views) is passed
  without a Python conversion/copy. raw=True returns the owning ctypes output
  array so a caller can expose its structured buffer without per-U Python ints.
  """
  array,owner=flat_buffer(dd_values,count,self.capacity);out=(Output*count)();kernel=ctypes.c_double();wall=ctypes.c_double()
  if not self.context:raise RuntimeError('GPU context is closed')
  error=self.library.gpu_lll_run(self.context,array,count,out,ctypes.byref(kernel),ctypes.byref(wall))
  if error:raise RuntimeError(self.library.gpu_lll_error(error).decode())
  timing=dict(kernel_ms=kernel.value,cuda_transfer_and_kernel_ms=wall.value)
  if raw:return out,timing
  return [dict(U=tuple(tuple(int(row.u[3*i+j]) for j in range(3)) for i in range(3)),status=STATUS.get(row.status,'unknown'),status_code=row.status,steps=row.steps) for row in out],timing
def prepare_batch(specifications,gpu):
 # This sequential host wrapper preserves the two geometry constructions of
 # the current preparation/certification path. Parallel host phases may call
 # patch_basis/finalize independently; their IPC must be measured separately.
 started=time.perf_counter();prepared=[];admitted=[];records=[];pending=[]
 for index,spec in enumerate(specifications):
  patch,a=patch_basis(spec)
  try:double_double(a);pending.append((index,spec,patch,a))
  except ValueError as exc:records.append(dict(index=index,status='cold_fallback',reason=str(exc)));admitted.append((index,*_cold(spec)))
 geometry=time.perf_counter()-started
 stats=dict(kernel_ms=0,cuda_transfer_and_kernel_ms=0)
 if pending:
  proposals,stats=gpu.reduce([x[3] for x in pending])
  for (index,spec,patch,a),proposal in zip(pending,proposals):
   try:
    if proposal['status_code']:raise ValueError(proposal['status'])
    task,token=certify_transform(spec,proposal['U'],patch,a)
    admitted.append((index,task,token));records.append(dict(index=index,status='gpu_admitted',steps=proposal['steps'],points=task.points,U=proposal['U']))
   except (ValueError,ArithmeticError) as exc:
    task,token=_cold(spec);admitted.append((index,task,token));records.append(dict(index=index,status='cold_fallback',reason=str(exc),gpu_status=proposal['status'],steps=proposal['steps'],points=task.points))
 admitted.sort();records.sort(key=lambda x:x['index']);stats.update(host_geometry_seconds=geometry,total_seconds=time.perf_counter()-started)
 return [(task,token) for _,task,token in admitted],records,stats
def _cold(spec):
 task=host.prepare_task(spec)
 if not night.native_safe(task):raise ValueError('Cold task also requires existing guarded subdivision/sphere fallback')
 return task,host.certify_task(task)
