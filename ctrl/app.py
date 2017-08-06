import os
import threading

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QSplitter

from core.common import App
from core.common.config import ConfigsHolder, FontHolder
from core.common.uilang import UILangHolder
from core.file import open_file
from core.model.model import DirModel
from ctrl.calc import CalcController
from ctrl.find import FindController
from view.appframe import AppFrame
from view.codebrowser import CodeBrowser
from view.dirbrowser import DirBrowser
from view.messagebox import MessageBox


class AppController:
    def __init__(self, parent=None):
        self._open_files = set()
        self._open_dirs = set()  # save all the open directories
        self._dir_model = DirModel()
        self.find_controller = None
        self.calc_controller = None
        self.ui = AppFrame(self, parent)
        # self._widget = QWidget(self._ui)
        # self._ui.setCentralWidget(self._widget)
        # self.dir_browser = DirBrowser(self, self._widget)
        # self.dir_browser.setModel(self._dir_model)
        # self.code_browser = CodeBrowser(self, self._widget)
        # self.layout = QHBoxLayout(self._widget)
        # self.layout.addWidget(self.dir_browser, 1)
        # self.layout.addWidget(self.code_browser, 4)
        # self._widget.setLayout(self.layout)
        # self._ui.resize(1000, 800)
        # self._ui.show()
        self.splitter = QSplitter(self.ui)
        self.ui.setCentralWidget(self.splitter)
        self.dir_browser = DirBrowser(self, self.splitter)
        self.dir_browser.setModel(self._dir_model)
        self.code_browser = CodeBrowser(self, self.splitter)
        self.splitter.setStretchFactor(1, 1)
        self.ui.resize(1000, 800)
        self.ui.show()

    def do_open_file(self, file):
        if not os.path.isfile(file):
            return
        if file in self._open_files:
            self.code_browser.set_current_tab(file)
            return
        text = open_file(file)
        if text:
            self.code_browser.add_new(file, text)
            self._open_files.add(file)
        else:
            # warning = QMessageBox(self.ui)
            # warning.warning(warning, "Error Occurred", "Cannot open {}".format(file), QMessageBox.Yes)
            MessageBox.warning(self.ui, "Error Occurred", "Cannot open {}".format(file)).show()
        pass

    def do_open_dir(self, path):
        if not path:
            return
        if not os.path.isdir(path):
            # QMessageBox.warning()
            return
        if path in self._open_dirs:
            return
        for p in self._open_dirs:
            if path.startswith(p):
                return
            elif p.startswith(path):
                return
        self._open_dirs.add(path)
        # start a new thread to update the model
        t = threading.Thread(target=self._dir_model.add_dir, args=(path, ))
        t.setDaemon(True)
        t.start()

    def do_close_file(self, file=None):
        if file:
            self._open_files.remove(file)
            return
        file = self.code_browser.close_current_tab()
        if file:
            self._open_files.remove(file)

    def do_close_all(self):
        self.code_browser.close_all_tabs()
        self._open_files.clear()

    def do_exit(self):
        if self.find_controller:
            self.find_controller.quit()
        if self.calc_controller:
            self.calc_controller.quit()
        ConfigsHolder.save()
        QCoreApplication.instance().quit()

    def do_find_file(self, file):
        pass

    def do_find_dir(self):
        self.find_controller = FindController(self.ui)

    def do_calculate(self):
        self.calc_controller = CalcController(self.ui)

    def do_change_tool_bar(self, show):
        ConfigsHolder.modify(App.TOOL_BAR, show)

    def do_change_font(self, font: QFont):
        FontHolder.set(font)
        self.ui.update_font()
        self.code_browser.update_font()

    def do_change_lang(self, lang_type):
        UILangHolder.get_ui_lang(lang_type)
        self.ui.update_lang()

    def do_change_theme(self, theme_name):
        pass

    def do_help(self):
        pass
