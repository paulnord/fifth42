import ctypes,os,signal,subprocess,sys,tempfile,time,unittest
from pathlib import Path
import search_supervisor as guard

@unittest.skipUnless(sys.platform == 'linux', 'Linux process groups required')
class CleanupTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.libc = ctypes.CDLL(None, use_errno=True)
        if cls.libc.prctl(36, 1, 0, 0, 0):
            raise unittest.SkipTest('Cannot enable test-process child subreaper')

    def test_running_leader_stopped(self):
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)
        try:
            guard.stop_owned(child)
            self.assertIsNotNone(child.poll())
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()

    def test_exited_leader_term_resistant_descendant_stopped(self):
        descendant = None
        with tempfile.TemporaryDirectory(prefix='ada-guard-test-') as tmp:
            marker = Path(tmp) / 'ready'
            worker = 'import os,signal,time; from pathlib import Path; signal.signal(signal.SIGTERM,signal.SIG_IGN); Path(' + repr(str(marker)) + ').write_text(str(os.getpid())); time.sleep(60)'
            leader = 'import subprocess,sys,time; from pathlib import Path; subprocess.Popen([sys.executable,"-c",' + repr(worker) + ']); p=Path(' + repr(str(marker)) + ');\nwhile not p.exists(): time.sleep(.01)'
            child = subprocess.Popen([sys.executable, '-c', leader], start_new_session=True)
            try:
                child.wait(timeout=5)
                descendant = int(marker.read_text())
                guard.stop_owned(child)
                deadline = time.monotonic() + 3
                while time.monotonic() < deadline:
                    pid, status = os.waitpid(descendant, os.WNOHANG)
                    if pid:
                        descendant = None
                        self.assertTrue(os.WIFSIGNALED(status))
                        self.assertEqual(os.WTERMSIG(status), signal.SIGKILL)
                        break
                    time.sleep(0.01)
                self.assertIsNone(descendant, 'Descendant survived owned-group cleanup')
            finally:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                child.wait(timeout=3)
                if descendant:
                    os.waitpid(descendant, 0)
