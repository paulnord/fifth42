"""Bounded, sequential requests to one persistent CPU or CUDA engine."""
import json
import os
import selectors
import subprocess
import time

class EngineSession:
    def __init__(self,command,backend,deadline,environment=None):
        self.deadline=deadline;self.backend=backend;self.request_id=0
        self.buffer=bytearray();self.stderr=bytearray();self.closed=False
        self.selector=selectors.DefaultSelector()
        start=time.perf_counter()
        self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,bufsize=0,env=environment)
        for stream,label in ((self.process.stdout,'stdout'),(self.process.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False);self.selector.register(stream,selectors.EVENT_READ,label)
        try:
            ready=self._line(min(deadline,time.monotonic()+30))
            if ready.get('ready') is not True or ready.get('backend')!=backend or ready.get('persistent') is not True:
                raise RuntimeError('Persistent engine startup handshake failed')
            self.ready=ready;self.startup_seconds=time.perf_counter()-start
        except BaseException:
            self.close();raise

    def _line(self,deadline):
        while True:
            newline=self.buffer.find(b'\n')
            if newline>=0:
                raw=bytes(self.buffer[:newline]);del self.buffer[:newline+1]
                return json.loads(raw)
            if len(self.buffer)>64*1024*1024:raise RuntimeError('Engine response exceeds the finite buffer allowance')
            left=deadline-time.monotonic()
            if left<=0:raise TimeoutError('Persistent engine request deadline reached')
            events=self.selector.select(min(.25,left))
            for key,_ in events:
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk:
                    self.selector.unregister(key.fileobj)
                    if key.data=='stdout':raise RuntimeError('Engine closed its output: '+self.stderr.decode(errors='replace'))
                elif key.data=='stdout':self.buffer.extend(chunk)
                else:
                    self.stderr.extend(chunk)
                    if len(self.stderr)>8192:del self.stderr[:-8192]

    def run(self,packet,timeout=60):
        if self.closed:raise RuntimeError('Engine session is closed')
        self.request_id+=1;data=packet.encode()
        if len(data)>16*1024*1024:raise ValueError('Packet frame exceeds the finite byte allowance')
        deadline=min(self.deadline,time.monotonic()+timeout)
        request=f'RUN {self.request_id} {len(data)}\n'.encode()+data
        # Use a writer deadline as well as a reader deadline. The engine reads
        # each whole frame before producing a response, avoiding pipe deadlocks.
        fd=self.process.stdin.fileno();os.set_blocking(fd,False)
        offset=0;start=time.perf_counter()
        try:
            while offset<len(request):
                if time.monotonic()>=deadline:raise TimeoutError('Engine request write deadline reached')
                try:offset+=os.write(fd,request[offset:])
                except BlockingIOError:
                    if self.process.poll() is not None:raise RuntimeError('Engine exited while reading a request')
                    time.sleep(.002)
            response=self._line(deadline)
        except BaseException:
            self.close();raise
        if response.get('request_id')!=self.request_id:
            raise RuntimeError('Engine returned a stale or mismatched request')
        return response,time.perf_counter()-start

    def close(self):
        if self.closed:return
        self.closed=True
        process=self.process
        if process.poll() is None:
            try:os.write(process.stdin.fileno(),b'QUIT\n')
            except OSError:pass
            try:process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill();process.wait(timeout=2)
        self.selector.close()
        for stream in (process.stdin,process.stdout,process.stderr):
            if stream is not None:stream.close()

    def __enter__(self):return self
    def __exit__(self,*args):self.close()
