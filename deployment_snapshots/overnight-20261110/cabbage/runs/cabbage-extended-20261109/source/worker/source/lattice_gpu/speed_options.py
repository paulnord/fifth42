"""Opt-in initialization for a NEW process using certified exact host arithmetic.

The initializer preserves Task/certificate/packet/coverage/journal formats.
It does not alter source files, start a search, or modify an existing engine.
"""
import scaling_core as core
import exact_host_opt
import packing_opt

def initialize(source, cpus=(), *, serializer=True):
    if core._ENGINE is not None or exact_host_opt._MODE is not None:
        raise RuntimeError('Speed options require a fresh worker process')
    exact_host_opt.initialize(source, cpus, 'combined')
    core.prepare_task = exact_host_opt.prepare_task
    core.certify_task = exact_host_opt.certify_task
    if serializer:
        core.task_digest = packing_opt.task_digest
