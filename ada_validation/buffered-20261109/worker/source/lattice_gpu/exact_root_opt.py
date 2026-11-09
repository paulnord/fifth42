"""Opt-in exact GMP integer roots on independently loaded lattice snapshots.

No shared snapshot is modified. Use ``initialize`` only as the initializer of a
fresh worker process; normal streaming/production initializers are unchanged.
"""
import importlib.util
import operator
from pathlib import Path
import sys
import uuid
import weakref

import gmpy2

if gmpy2.version() != '2.2.2':
    raise RuntimeError('Exact root experiment requires gmpy2 2.2.2')

_PRIVATE = weakref.WeakSet()


def exact_iroot(n, k=5):
    """Floor of the nonnegative integer kth root, with no floating arithmetic.

    Return a Python int even for mpz inputs. Very large degrees are handled
    before GMP's bounded C degree conversion, preserving arbitrary integer k.
    """
    n, k = operator.index(n), operator.index(k)
    if n < 0 or k < 1:
        raise ValueError('nonnegative radicand and positive degree required')
    if n < 2 or k == 1:
        return n
    if k >= n.bit_length():
        return 1
    return int(gmpy2.iroot(n, k)[0])


def install_on_private_lattice(lattice):
    """Install only into a private copy constructed by this module."""
    if lattice not in _PRIVATE or sys.modules.get(lattice.__name__) is not lattice:
        raise ValueError('Refusing to modify a shared or unowned lattice module')
    if lattice.root_bracket.__globals__ is not vars(lattice):
        raise ValueError('Root enclosure does not belong to the private module')
    lattice.iroot = exact_iroot
    return lattice


def load_private_lattice(source, optimized=True):
    """Load a fresh mpq snapshot; ``optimized=False`` supplies a clean control."""
    path = Path(source) / 'compiled_experiment' / 'lattice5_snapshot.py'
    name = '_exact_root_private_' + uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, path)
    lattice = importlib.util.module_from_spec(spec)
    sys.modules[name] = lattice  # dataclass introspection needs this registration
    try:
        spec.loader.exec_module(lattice)
        lattice.Q = gmpy2.mpq
        _PRIVATE.add(lattice)
        if optimized:
            install_on_private_lattice(lattice)
        return lattice
    except BaseException:
        sys.modules.pop(name, None)
        raise


def initialize(source, cpus=()):
    """Multiprocessing initializer. Reject reuse instead of contaminating trials.

    Existing initialization still enforces pinned dependencies, CPU affinity,
    worker parent-lifetime guard, and a warmed exact-certified LLL backend.
    """
    import scaling_core as core
    if core._ENGINE is not None:
        raise RuntimeError('Exact root initializer requires a fresh worker')
    core.initialize(source, cpus)
    lattice = load_private_lattice(source)
    core._ENGINE = (str(source), lattice)
