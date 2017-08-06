import os
from collections import Iterator, Iterable, deque


class DirWalker(Iterable):
    def __init__(self, base_dir: str, filters: set = None):
        self._base_dir = base_dir
        self._filters = filters

    def __iter__(self):
        if self._filters:
            return bfs_filtered_file_generator(self._base_dir, self._filters)
        else:
            return bfs_file_generator(self._base_dir)


def bfs_file_generator(base_dir):
    unvisited = deque()
    unvisited.append(base_dir)
    while len(unvisited):
        d = unvisited.popleft()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                unvisited.append(f)
            else:
                yield f
    raise StopIteration()


def bfs_filtered_file_generator(base_dir, filters):
    unvisited = deque()
    unvisited.append(base_dir)
    while len(unvisited):
        d = unvisited.popleft()
        for f in os.listdir(d):
            f = os.path.join(d, f)
            if os.path.isdir(f):
                unvisited.append(f)
            elif os.path.isfile(f):
                # get file if file's extension in @self._filters
                ext = os.path.splitext(f)[-1]
                if ext in filters:
                    yield (f, ext)
    raise StopIteration()
