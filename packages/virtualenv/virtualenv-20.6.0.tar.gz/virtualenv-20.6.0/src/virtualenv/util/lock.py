"""holds locking functionality that works across processes"""
from __future__ import absolute_import, unicode_literals

import logging
import os
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from threading import Lock, RLock

from filelock import FileLock, Timeout
from six import add_metaclass

from virtualenv.util.path import Path


class _CountedFileLock(FileLock):
    def __init__(self, lock_file):
        parent = os.path.dirname(lock_file)
        if not os.path.isdir(parent):
            try:
                os.makedirs(parent)
            except OSError:
                pass
        super(_CountedFileLock, self).__init__(lock_file)
        self.count = 0
        self.thread_safe = RLock()

    def acquire(self, timeout=None, poll_intervall=0.05):
        with self.thread_safe:
            if self.count == 0:
                super(_CountedFileLock, self).acquire(timeout=timeout, poll_intervall=poll_intervall)
            self.count += 1

    def release(self, force=False):
        with self.thread_safe:
            if self.count == 1:
                super(_CountedFileLock, self).release(force=force)
            self.count = max(self.count - 1, 0)


_lock_store = {}
_store_lock = Lock()


@add_metaclass(ABCMeta)
class PathLockBase(object):
    def __init__(self, folder):
        path = Path(folder)
        self.path = path.resolve() if path.exists() else path

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.path)

    def __div__(self, other):
        return type(self)(self.path / other)

    def __truediv__(self, other):
        return self.__div__(other)

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def lock_for_key(self, name, no_block=False):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def non_reentrant_lock_for_key(name):
        raise NotImplementedError


class ReentrantFileLock(PathLockBase):
    def __init__(self, folder):
        super(ReentrantFileLock, self).__init__(folder)
        self._lock = None

    def _create_lock(self, name=""):
        lock_file = str(self.path / "{}.lock".format(name))
        with _store_lock:
            if lock_file not in _lock_store:
                _lock_store[lock_file] = _CountedFileLock(lock_file)
            return _lock_store[lock_file]

    @staticmethod
    def _del_lock(lock):
        with _store_lock:
            if lock is not None:
                with lock.thread_safe:
                    if lock.count == 0:
                        _lock_store.pop(lock.lock_file, None)

    def __del__(self):
        self._del_lock(self._lock)

    def __enter__(self):
        self._lock = self._create_lock()
        self._lock_file(self._lock)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release(self._lock)

    def _lock_file(self, lock, no_block=False):
        # multiple processes might be trying to get a first lock... so we cannot check if this directory exist without
        # a lock, but that lock might then become expensive, and it's not clear where that lock should live.
        # Instead here we just ignore if we fail to create the directory.
        try:
            os.makedirs(str(self.path))
        except OSError:
            pass
        try:
            lock.acquire(0.0001)
        except Timeout:
            if no_block:
                raise
            logging.debug("lock file %s present, will block until released", lock.lock_file)
            lock.release()  # release the acquire try from above
            lock.acquire()

    @staticmethod
    def _release(lock):
        lock.release()

    @contextmanager
    def lock_for_key(self, name, no_block=False):
        lock = self._create_lock(name)
        try:
            try:
                self._lock_file(lock, no_block)
                yield
            finally:
                self._release(lock)
        finally:
            self._del_lock(lock)

    @contextmanager
    def non_reentrant_lock_for_key(self, name):
        with _CountedFileLock(str(self.path / "{}.lock".format(name))):
            yield


class NoOpFileLock(PathLockBase):
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @contextmanager
    def lock_for_key(self, name, no_block=False):
        yield

    @contextmanager
    def non_reentrant_lock_for_key(self, name):
        yield


__all__ = (
    "NoOpFileLock",
    "ReentrantFileLock",
    "Timeout",
)
