"""Ordered, bounded preparation on one background thread (standard library only).

Estimates must bound every prepared item's resident bytes and points. Reservations
include in-flight preparation, queued results, and the result held by the consumer
until its next next() call. Bytes mean caller-defined serialized canonical
payload/packet bytes, not Python object RSS. Source storage is not counted. No
external coverage state is changed here: callers commit only after consuming and
successfully processing a result.
"""
from collections import deque
from threading import Condition, Event, Thread, current_thread


class PrefetchLimitError(ValueError):
    """An item exceeds its declared reservation or a configured limit."""


class BoundedPrefetch:
    """Prepare items in order, reserving capacity before calling ``prepare``.

    ``estimate_size(item)`` and optional ``actual_size(result)`` return integer
    ``(bytes, points)`` pairs. Actual size must not exceed the estimate, even if
    other capacity is available. Without actual_size, estimates are trusted.
    A result's reservation is released on the following next() call or close().

    close() is idempotent, discards unconsumed results, and joins the worker.
    Python cannot interrupt arbitrary callbacks: source iteration, size callbacks,
    and prepare must terminate; long-running callbacks should observe cancel_event.
    Blocking pool.map or I/O callbacks need their own task deadlines: close()
    intentionally waits for preparation to exit rather than abandoning its work.
    Consumers must use a context manager or explicitly close on early exit.
    Only one consumer is supported.
    """

    def __init__(self, items, prepare, *, estimate_size, max_outstanding,
                 max_item_bytes, max_item_points, max_queued_bytes,
                 max_queued_points, actual_size=None):
        limits = (max_outstanding, max_item_bytes, max_item_points,
                  max_queued_bytes, max_queued_points)
        if any(type(v) is not int or v <= 0 for v in limits):
            raise ValueError("all limits must be positive integers")
        self._items = items
        self._prepare = prepare
        self._estimate_size = estimate_size
        self._actual_size = actual_size
        self._max_outstanding = max_outstanding
        self._item_limits = (max_item_bytes, max_item_points)
        self._queued_limits = (max_queued_bytes, max_queued_points)
        self.cancel_event = Event()
        self._condition = Condition()
        self._queue = deque()
        self._thread = None
        self._done = False
        self._active_size = None
        self._outstanding = self._bytes = self._points = 0
        self._peak_outstanding = self._peak_bytes = self._peak_points = 0

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def __iter__(self):
        self._start()
        return self

    def _start(self):
        with self._condition:
            if self._thread is None and not self.cancel_event.is_set():
                self._thread = Thread(target=self._run, name="bounded-prefetch",
                                      daemon=True)
                self._thread.start()

    @staticmethod
    def _size(value):
        try:
            byte_count, points = value
        except (TypeError, ValueError) as exc:
            raise PrefetchLimitError("size must be a (bytes, points) pair") from exc
        if any(type(v) is not int or v < 0 for v in (byte_count, points)):
            raise PrefetchLimitError("bytes and points must be nonnegative integers")
        return byte_count, points

    def _reserve(self, size):
        self._outstanding += 1
        self._bytes += size[0]
        self._points += size[1]
        self._peak_outstanding = max(self._peak_outstanding, self._outstanding)
        self._peak_bytes = max(self._peak_bytes, self._bytes)
        self._peak_points = max(self._peak_points, self._points)

    def _release(self, size):
        self._outstanding -= 1
        self._bytes -= size[0]
        self._points -= size[1]

    def _run(self):
        reserved = None
        try:
            source = iter(self._items)
            while True:
                # Do not even advance the source while the item window is full.
                with self._condition:
                    self._condition.wait_for(lambda: self.cancel_event.is_set() or
                        self._outstanding < self._max_outstanding)
                    if self.cancel_event.is_set():
                        return
                try:
                    item = next(source)
                except StopIteration:
                    return
                size = self._size(self._estimate_size(item))
                if any(n > cap for n, cap in zip(size, self._item_limits)):
                    raise PrefetchLimitError("item exceeds per-item limit")
                if any(n > cap for n, cap in zip(size, self._queued_limits)):
                    raise PrefetchLimitError("item exceeds aggregate capacity")
                with self._condition:
                    self._condition.wait_for(lambda: self.cancel_event.is_set() or (
                        self._bytes + size[0] <= self._queued_limits[0] and
                        self._points + size[1] <= self._queued_limits[1]))
                    if self.cancel_event.is_set():
                        return
                    self._reserve(size)
                    reserved = size
                result = self._prepare(item)
                if self._actual_size is not None:
                    actual = self._size(self._actual_size(result))
                    if any(n > cap for n, cap in zip(actual, size)):
                        raise PrefetchLimitError("actual item size exceeds reservation")
                with self._condition:
                    if self.cancel_event.is_set():
                        return
                    self._queue.append((result, None, reserved))
                    reserved = None
                    self._condition.notify_all()
                # Do not retain an extra result after the consumer releases it.
                del result, item
        except BaseException as exc:
            with self._condition:
                if not self.cancel_event.is_set():
                    if reserved is None:
                        reserved = (0, 0)
                        self._reserve(reserved)
                    self._queue.append((None, exc, reserved))
                    reserved = None
                    self._condition.notify_all()
        finally:
            with self._condition:
                if reserved is not None:
                    self._release(reserved)
                self._done = True
                self._condition.notify_all()

    def __next__(self):
        self._start()
        with self._condition:
            if self._active_size is not None:
                self._release(self._active_size)
                self._active_size = None
                self._condition.notify_all()
            self._condition.wait_for(lambda: self._queue or self._done or
                                     self.cancel_event.is_set())
            if self.cancel_event.is_set() or not self._queue:
                raise StopIteration
            result, error, size = self._queue.popleft()
            if error is None:
                self._active_size = size
            else:
                self._release(size)
            self._condition.notify_all()
        if error is not None:
            raise error
        return result

    def snapshot(self):
        """Return counters, including reserved in-flight preparation resources."""
        with self._condition:
            return dict(outstanding=self._outstanding, reserved_bytes=self._bytes,
                        reserved_points=self._points,
                        peak_outstanding=self._peak_outstanding,
                        peak_reserved_bytes=self._peak_bytes,
                        peak_reserved_points=self._peak_points)

    def close(self):
        with self._condition:
            self.cancel_event.set()
            if self._active_size is not None:
                self._release(self._active_size)
                self._active_size = None
            while self._queue:
                _, _, size = self._queue.popleft()
                self._release(size)
            self._condition.notify_all()
            thread = self._thread
        if thread is not None and thread is not current_thread():
            thread.join()
