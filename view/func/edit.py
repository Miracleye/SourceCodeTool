from PyQt5.QtCore import QDir, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QAction, QFileDialog, QCompleter

from core.common import App
from core.common.uilang import UILangHolder
from core.model.model import PathCompleterModel
from res.resource import IconsHolder


class DirEdit(QLineEdit):
    def __init__(self, parent):
        super(DirEdit, self).__init__(parent)
        self.update_lang()
        self.dir_act = QAction(self)
        self.dir_act.setIcon(IconsHolder.get_by_ext("dir"))
        self.addAction(self.dir_act, QLineEdit.TrailingPosition)
        self._completer = QCompleter(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer_model = PathCompleterModel()
        self._completer.setModel(self._completer_model)
        self.setCompleter(self._completer)
        self.dir_act.triggered.connect(self.open_file_dialog)
        self.textChanged.connect(self.update_completer)
        self._completer.activated.connect(self.setText)

    def update_lang(self):
        self.setPlaceholderText(UILangHolder.get(App.DIR_HINT))

    def open_file_dialog(self):
        home_path = QDir.homePath()
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Directory", home_path, options)
        if selected_dir:
            self.setText(selected_dir)

    def update_completer(self, path):
        if not path:
            return
        self._completer_model.update(path)


class FilterEdit(QLineEdit):
    def __init__(self, parent=None):
        super(FilterEdit, self).__init__(parent)
        reg = QRegExp(r'(\*\.[a-zA-Z+]*;)*')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.setValidator(validator)
        self.setClearButtonEnabled(True)

