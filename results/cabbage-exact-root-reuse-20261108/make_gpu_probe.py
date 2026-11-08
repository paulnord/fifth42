from pathlib import Path
p=Path('/home/pnord/scratch/saved-root-pAjTHBhR/cpu')
s=(p/'run_probe.py').read_text()
s=s.replace("binaries=['scaling_cpu','scaling_cpu_ubsan']", "binaries=['scaling_gpu']")
s=s.replace("str(ROOT/'native/bin'/binary),'--threads','1'],'emulated'", "str(ROOT/'candidate/source/lattice_gpu/bin'/binary)],'gpu'")
s=s.replace("core.decode_batch(batch,response,'emulated')", "core.decode_batch(batch,response,'gpu')")
s=s.replace("[str(ROOT/'native/bin/scaling_cpu'),'--threads','1'],'emulated'", "[str(ROOT/'candidate/source/lattice_gpu/bin/scaling_gpu')],'gpu'")
s=s.replace("no_cuda=True", "no_cuda=False,cuda_executed=True")
s=s.replace("'Local native CPU engine, not CUDA.'", "'CUDA 13.2 RTX 3060; identical enumeration binary for both host-source variants.'")
insert='''
# Scratch-only instrumentation: preserve every exact native count/hit and timing.
import atexit
GPU_RESPONSES=[]
OriginalSession=engine_session.EngineSession
class RecordedSession(OriginalSession):
    def __init__(self,*args,**kwargs):
        active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip()
        if active: raise RuntimeError('GPU resource conflict: '+active)
        super().__init__(*args,**kwargs)
        self.gpu_pid=self.process.pid
    def run(self,packet,timeout=30):
        active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True).strip().splitlines()
        if any(int(pid)!=self.gpu_pid for pid in active):
            self.close()
            raise RuntimeError('GPU resource conflict: '+str(active))
        response,wall=super().run(packet,timeout=min(timeout,30))
        GPU_RESPONSES.append(dict(packet_sha256=hashlib.sha256(packet.encode()).hexdigest(),wall_seconds=wall,response=response))
        return response,wall
engine_session.EngineSession=RecordedSession
atexit.register(lambda:Path(os.environ['GPU_LOG']).write_text(json.dumps(GPU_RESPONSES,indent=2)+'\\n'))
'''
s=s.replace('def stable(x):',insert+'\ndef stable(x):')
(p/'gpu_probe.py').write_text(s)
