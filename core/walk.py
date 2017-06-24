import os
from collections import Iterator, Iterable

from util.queue import Queue
from util.stack import Stack


class DirWalker(Iterable):
    DFS = 1
    BFS = 2

    def __init__(self, base_dir: str, filters: set=None):
        self._base_dir = base_dir
        self._filters = filters

    def __iter__(self):
        if self._filters:
            # return BFSFilteredFileIterator(self._base_dir, self._filters)
            return bfs_filtered_file_generator(self._base_dir, self._filters)
        else:
            # return BFSFileIterator(self._base_dir)
            return bfs_file_generator(self._base_dir)


def bfs_file_generator(base_dir):
    unvisited = Queue()
    unvisited.enqueue(base_dir)
    while not unvisited.is_empty():
        d = unvisited.dequeue()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                unvisited.enqueue(f)
            else:
                yield f
    raise StopIteration()


def bfs_filtered_file_generator(base_dir, filters):
    unvisited = Queue()
    unvisited.enqueue(base_dir)
    while not unvisited.is_empty():
        d = unvisited.dequeue()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                unvisited.enqueue(f)
            elif os.path.isfile(f):
                # get file if file's extension in @self._filters
                ext = os.path.splitext(f)[-1]
                if ext in filters:
                    yield (f, ext)
    raise StopIteration()


def dfs_file_generator(base_dir):
    visited = Stack()
    visited.push(base_dir)
    while not visited.is_empty():
        d = visited.pop()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                visited.push(f)
            else:
                yield f
    raise StopIteration()


def dfs_filtered_file_generator(base_dir, filters):
    visited = Stack()
    visited.push(base_dir)
    while not visited.is_empty():
        d = visited.pop()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                visited.push(f)
            elif os.path.isfile(f):
                ext = os.path.splitext(f)[-1]
                if ext in filters:
                    yield (f, ext)
    raise StopIteration()


# The following classes are use for module's internal use
class BFSFileIterator(Iterator):
    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._unvisited = Queue()
        self._unvisited.enqueue(self._base_dir)

    def __next__(self):
        """ BFS to get each file under a base directory.
        :return:
        """
        while not self._unvisited.is_empty():
            d = self._unvisited.dequeue()
            for f in os.listdir(d):
                f = os.path.join(d, f)
                if os.path.isdir(f):
                    self._unvisited.enqueue(f)
                else:
                    yield f
        raise StopIteration()


class DFSFileIterator(Iterator):
    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._visited = Stack()
        self._visited.push(self._base_dir)

    def __next__(self):
        """ DFS to get each file under a base directory.
        """
        while not self._visited.is_empty():
            d = self._visited.pop()
            for f in os.listdir(d):
                f = os.path.join(d, f)
                if os.path.isdir(f):
                    self._visited.push(f)
                else:
                    yield f
        raise StopIteration()


class BFSFilteredFileIterator(Iterator):
    def __init__(self, base_dir, filters):
        self._base_dir = base_dir
        self._filters = filters
        self._unvisited = Queue()
        self._unvisited.enqueue(self._base_dir)

    def __next__(self):
        """ BFS to get each file under a base directory.
        :return:
        """
        while not self._unvisited.is_empty():
            d = self._unvisited.dequeue()
            for f in os.listdir(d):
                f = os.path.join(d, f)
                if os.path.isdir(f):
                    self._unvisited.enqueue(f)
                elif os.path.isfile(f):
                    # get file if file's extension in @self._filters
                    ext = os.path.splitext(f)[-1]
                    if ext in self._filters:
                        yield (f, ext)
        raise StopIteration()


class DFSFilteredFileIterator(Iterator):
    def __init__(self, base_dir, filters):
        self._base_dir = base_dir
        self._filters = filters
        self._visited = Stack()
        self._visited.push(self._base_dir)

    def __next__(self):
        """ DFS to get each file under a base directory.
        """
        while not self._visited.is_empty():
            d = self._visited.pop()
            for f in os.listdir(d):
                f = os.path.join(d, f)
                if os.path.isdir(f):
                    self._visited.push(f)
                elif os.path.isfile(f):
                    ext = os.path.splitext(f)[-1]
                    if ext in self._filters:
                        yield (f, ext)
        raise StopIteration()
