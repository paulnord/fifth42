#!/usr/bin/env python3
"""Local-only guard tests: mocked service reads and synthetic owned process groups."""
import ctypes
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('ada_guard_tested', Path(__file__).with_name('ada_guard.py'))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def result(stdout='', code=0):
    return subprocess.CompletedProcess([], code, stdout, '')


class ServiceTests(unittest.TestCase):
    def test_loaded_inactive_dead_and_no_search_passes(self):
        with mock.patch.object(guard.subprocess, 'run', side_effect=[
            result('LoadState=loaded\nActiveState=inactive\nSubState=dead\n'), result('1 init\n')]):
            guard.finished_service('synthetic.service')

    def test_false_finished_states_fail_closed(self):
        states = [
            'LoadState=not-found\nActiveState=inactive\nSubState=dead\n',
            'LoadState=loaded\nActiveState=active\nSubState=running\n',
            'LoadState=loaded\nActiveState=failed\nSubState=failed\n',
            'LoadState=loaded\nActiveState=inactive\n',
            '',
        ]
        for state in states:
            with self.subTest(state=state), mock.patch.object(guard.subprocess, 'run', return_value=result(state)):
                with self.assertRaises(RuntimeError):
                    guard.finished_service('synthetic.service')
        with mock.patch.object(guard.subprocess, 'run', return_value=result(
                'LoadState=loaded\nActiveState=inactive\nSubState=dead\n', 1)):
            with self.assertRaises(RuntimeError):
                guard.finished_service('synthetic.service')

    def test_lingering_search_and_publisher_fail_closed(self):
        for name in ('overnight_service.py', 'overnight_search.py', 'github_status.py'):
            with self.subTest(name=name), mock.patch.object(guard.subprocess, 'run', side_effect=[
                result('LoadState=loaded\nActiveState=inactive\nSubState=dead\n'),
                result(f'999999 python /synthetic/{name}\n')]):
                with self.assertRaises(RuntimeError):
                    guard.finished_service('synthetic.service')


@unittest.skipUnless(sys.platform == 'linux', 'Linux process groups required')
class CleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Adopt/reap our own synthetic orphan instead of leaving a zombie to PID 1.
        cls.libc = ctypes.CDLL(None, use_errno=True)
        if cls.libc.prctl(36, 1, 0, 0, 0):
            raise unittest.SkipTest('Cannot enable test-process child subreaper')

    def test_running_leader_stopped(self):
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)
        try:
            guard.stop_group(child)
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
                guard.stop_group(child)
                deadline = time.monotonic() + 3
                while time.monotonic() < deadline:
                    pid, status = os.waitpid(descendant, os.WNOHANG)
                    if pid:
                        descendant = None
                        self.assertTrue(os.WIFSIGNALED(status))
                        self.assertEqual(os.WTERMSIG(status), signal.SIGKILL)
                        break
                    time.sleep(.01)
                self.assertIsNone(descendant, 'Descendant survived owned-group cleanup')
            finally:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                child.wait(timeout=3)
                if descendant:
                    os.waitpid(descendant, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
