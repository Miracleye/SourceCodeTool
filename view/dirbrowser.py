from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTreeView, QAbstractItemView

from core.common.config import FontHolder

"""
"""


class DirBrowser(QTreeView):
    def __init__(self, controller=None, parent=None):
        super(DirBrowser, self).__init__(parent)
        self.controller = controller
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.clicked.connect(self.column_resize)
        self.collapsed.connect(self.column_resize)
        self.expanded.connect(self.column_resize)
        self.doubleClicked.connect(self._open_file)

    def update_ui(self):
        font = FontHolder.get()
        self.setFont(font)

    def column_resize(self, index):
        self.resizeColumnToContents(0)

    def _open_file(self, index: QModelIndex):
        if index.isValid():
            file = self.model().get_file_path(index)
            self.controller.do_open_file(file)
