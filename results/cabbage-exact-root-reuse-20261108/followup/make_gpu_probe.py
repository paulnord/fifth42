from pathlib import Path
root=Path(__file__).resolve().parent
s=(root/'run_probe.py').read_text()
s=s.replace("binaries=['scaling_cpu','scaling_cpu_ubsan']", "binaries=['scaling_gpu']")
s=s.replace("str(ROOT/'native/bin'/binary),'--threads','1'],'emulated'", "str(ROOT/'device/bin'/binary)],'gpu'")
s=s.replace("core.decode_batch(batch,response,'emulated')", "core.decode_batch(batch,response,'gpu')")
s=s.replace("[str(ROOT/'native/bin/scaling_cpu'),'--threads','1'],'emulated'", "[str(ROOT/'device/bin/scaling_gpu')],'gpu'")
s=s.replace("no_cuda=True", "no_cuda=False,cuda_executed=True")
s=s.replace("'Local native CPU engine, not CUDA.'", "'RTX 3060 CUDA 13.2; shared enumeration binary; host-source baseline/candidate variants.'")
s=s.replace("'Four allowed cloud CPUs; not Ada topology or hardware.'", "'Four Cabbage logical CPUs; not Ada topology or hardware.'")
s=s.replace("record=pipeline.execute_chunk(chunk,pipeline.OwnedEngine(session),trial='validation',coordinator=0)","record=pipeline.execute_chunk(chunk,pipeline.OwnedEngine(session),trial='validation',coordinator=0)")
s=s.replace("geometry=chunk.geometry_sha256,certificates=chunk.plan.certificate_sha256,hits=record['hits']))", "geometry=chunk.geometry_sha256,certificates=chunk.plan.certificate_sha256,hits=record['hits'],counts=[batch['native_counts'] for batch in record['batches']],native_hits=[batch['native_hit_records'] for batch in record['batches']]))")
s=s.replace("packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in chunk.plan.batches],hits=record['hits']))", "packets=[hashlib.sha256(b.packet.encode()).hexdigest() for b in chunk.plan.batches],hits=record['hits'],native_counts=[batch['native_counts'] for batch in record['batches']],native_hits=[batch['native_hit_records'] for batch in record['batches']]))")
s=s.replace("rows=rows,queue=stream.snapshot(),", "rows=rows,queue=stream.snapshot(),native_engine_seconds=sum(x['response']['engine_seconds'] for x in GPU_RESPONSES),cuda_kernel_seconds=sum(x['response']['kernel_seconds'] for x in GPU_RESPONSES),gpu_rpc_seconds=sum(x['wall_seconds'] for x in GPU_RESPONSES),native_records_sha256=digest([dict(packet_sha256=x['packet_sha256'],counts=x['response']['counts'],hits=sorted(x['response']['hits'],key=lambda h:(h['task'],h['linear']))) for x in GPU_RESPONSES]),")
insert='''
# Record raw engine output. Resource monitoring runs in resource_runner.py,
# outside the timed process. No nvidia-smi subprocess in the timed chunk loop.
import atexit
GPU_RESPONSES=[]
OriginalSession=engine_session.EngineSession
class RecordedSession(OriginalSession):
    def __init__(self,*args,**kwargs):
        active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip()
        if active:raise RuntimeError('GPU resource conflict: '+active)
        super().__init__(*args,**kwargs)
    def run(self,packet,timeout=30):
        response,wall=super().run(packet,timeout=min(timeout,30))
        GPU_RESPONSES.append(dict(packet_sha256=hashlib.sha256(packet.encode()).hexdigest(),wall_seconds=wall,response=response))
        if response.get('box_complete') is not True:raise RuntimeError('Native GPU rejection: '+str(response))
        return response,wall
engine_session.EngineSession=RecordedSession
atexit.register(lambda:Path(os.environ['GPU_LOG']).write_text(json.dumps(GPU_RESPONSES,indent=2)+'\\n'))
'''
s=s.replace('def stable(x):',insert+'\ndef stable(x):')
(root/'gpu_probe.py').write_text(s)
