import os

from PyQt5.QtCore import QVariant, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from core.common import App
from core.common.uilang import UILangHolder
from res.resource import IconsHolder
from util.queue import Queue

""" This module defined all the Qt Models that Qt Views will use, each model is customized, means that 
    you don't need to modify it.
"""


class DirModel(QStandardItemModel):
    """
    """

    def __init__(self, header: str="Name"):
        super(DirModel, self).__init__()
        # get these objects for faster access
        self.setHorizontalHeaderLabels([header])
        self.icons = IconsHolder.get_icons()
        self.emap = IconsHolder.get_ext_id_map()
        self.emap_keys = self.emap.keys()
        self.base_dirs = list()

    def add_dir(self, path: str):
        self.base_dirs.append(path)
        # self.dfs_add_dir(self, *os.path.split(path))
        self.bfs_add_dir(path)

    def dfs_add_dir(self, item, dir_path, path):
        """ Recursive DFS to fill model
        """
        new = QStandardItem(self.icons[self.emap["dir"]], path)
        item.appendRow(new)
        real = os.path.join(dir_path, path)
        for f in os.listdir(real):
            if os.path.isdir(os.path.join(real, f)):
                self.dfs_add_dir(new, real, f)
            else:
                (name, ext) = os.path.splitext(f)
                if ext in self.emap_keys:
                    new.appendRow(QStandardItem(self.icons[self.emap[ext]], f))
                else:
                    new.appendRow(QStandardItem(self.icons[self.emap["unknown"]], f))

    def bfs_add_dir(self, dir_path):
        """ Non-Recursive BFS to fill model
        """
        item = QStandardItem(self.icons[self.emap["dir"]], dir_path)
        self.appendRow(item)
        queue = Queue()
        queue.enqueue((dir_path, item))
        while not queue.is_empty():
            """ Only directories will be added to the queue, in each loop, a dir will be popped out
            """
            (path, item) = queue.dequeue()
            for f in os.listdir(path):
                file = os.path.join(path, f)
                if os.path.isdir(file):
                    new = QStandardItem(self.icons[self.emap["dir"]], f)
                    item.appendRow(new)
                    queue.enqueue((file, new))
                else:
                    (name, ext) = os.path.splitext(file)
                    if ext in self.emap_keys:
                        item.appendRow(QStandardItem(self.icons[self.emap[ext]], f))
                    else:
                        item.appendRow(QStandardItem(self.icons[self.emap["unknown"]], f))

    def get_file_path(self, index: QModelIndex):
        """ From index to get real file path
        """
        if not index.isValid():
            return None
        path = list()
        path.append(index.data())
        while index.parent().isValid():
            index = index.parent()
            path.append(index.data())
        row = index.row()
        path[-1] = self.base_dirs[row]
        path.reverse()
        return '/'.join(path)


class FindResultModel(QStandardItemModel):
    """ The model holds the 'find' operation's results. Set the result table view with this model.
    """

    def __init__(self):
        super(FindResultModel, self).__init__()
        self.header = [
            UILangHolder.get(App.LOCATION),
            UILangHolder.get(App.FOUND),
            UILangHolder.get(App.ERROR_INFO)
        ]
        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)

    def append_result(self, result):
        row = self.rowCount()
        item = QStandardItem(result[0])
        self.setItem(row, 0, item)
        if result[1]:
            found = ''.join(result[1])
            item = QStandardItem(found)
            self.setItem(row, 1, item)
        item = QStandardItem(result[2])
        self.setItem(row, 2, item)

    def clear(self):
        super(FindResultModel, self).clear()
        self.setHorizontalHeaderLabels(self.header)


class CalcResultModel(QStandardItemModel):
    """ The model holds the 'calculate' operation's results. Set the result table view with this model.
    """

    def __init__(self):
        super(CalcResultModel, self).__init__()
        self.header = [
            UILangHolder.get(App.LOCATION),
            UILangHolder.get(App.SIZE),
            UILangHolder.get(App.LINES),
            UILangHolder.get(App.TOTAL_LINES),
            UILangHolder.get(App.WORDS),
            UILangHolder.get(App.ERROR_INFO)
        ]
        self.column = len(self.header)
        self.setColumnCount(self.column)
        self.setHorizontalHeaderLabels(self.header)

    def append_result(self, result):
        """
        :param result: The @result format should be like this: [file, size, code lines, total lines, words, error]
        :return:
        """
        row = self.rowCount()
        item = QStandardItem(result[0])
        self.setItem(row, 0, item)
        for i in range(1, self.column - 1):
            item = QStandardItem()
            item.setData(QVariant(result[i]), Qt.EditRole)
            self.setItem(row, i, item)
        item = QStandardItem(result[self.column - 1])
        self.setItem(row, self.column-1, item)

    def clear(self):
        super(CalcResultModel, self).clear()
        self.setHorizontalHeaderLabels(self.header)

    def get_data(self):
        for i in range(self.rowCount()):
            data = list()
            # data.append(self.)
            yield data


class PathCompleterModel(QStandardItemModel):
    def __init__(self):
        super(PathCompleterModel, self).__init__()
        self.setColumnCount(1)
        self.prev_path = ''

    def update(self, path):
        if not path:
            return
        self.clear()
        d = os.path.dirname(path)
        if os.path.isdir(d):
            for file in os.listdir(d):
                path = os.path.join(d, file)
                if os.path.isdir(path):
                    self.appendRow(QStandardItem(path))
