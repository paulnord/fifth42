"""Explicit native backend selection and canonical packet record accounting."""
from engine_session import EngineSession

def open_session(binary, backend, deadline, threads=1):
    if backend not in ('emulated','gpu'):
        raise ValueError('Unknown native backend')
    command=[str(binary)]
    if backend=='emulated':command+=['--threads',str(threads)]
    return EngineSession(command,backend,deadline)

def verify_workers(identities,cpus):
    if len(identities)!=len(cpus) or set(identities.values())!={(c,) for c in cpus}:
        raise RuntimeError('Worker affinity is missing or duplicated')

def normalized_counts(batch,response,locals_=None):
    indices=range(len(batch.tasks)) if locals_ is None else locals_
    return sorted((batch.tasks[i].id,response['counts'][i]['expected'],response['counts'][i]['visited']) for i in indices)

def normalized_hits(batch,response,locals_=None):
    indices=set(range(len(batch.tasks)) if locals_ is None else locals_)
    return sorted((batch.tasks[h['task']].id,h['linear'],h['a'],h['b'],h['c']) for h in response['hits'] if h['task'] in indices)
