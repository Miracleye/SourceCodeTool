import os

from PyQt5.QtWidgets import QTabWidget

from core.common.config import FontHolder
from view.texteditor import TextEditor


class CodeBrowser(QTabWidget):
    def __init__(self, controller=None, parent=None):
        super(CodeBrowser, self).__init__(parent)
        self.controller = controller
        self.usesScrollButtons()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def set_controller(self, controller):
        self.controller = controller

    def update_font(self):
        self.setFont(FontHolder.get())
        for index in range(self.count()):
            tab = self.widget(index)
            tab.update_font()

    def add_new(self, file, text):
        tab = TextEditor(file, text, self)
        self.addTab(tab, os.path.split(file)[1])
        self.setCurrentIndex(self.count() - 1)

    def set_current_tab(self, file):
        for index in range(self.count()):
            tab = self.widget(index)
            if file == tab.get_file():
                self.setCurrentIndex(index)

    def get_current_text(self):
        if not self.count():
            return None
        tab = self.currentWidget()
        return tab.get_text()

    def close_tab(self, index):
        tab = self.widget(index)
        file = tab.get_file()
        self.removeTab(index)
        self.controller.do_close_file(file)

    def close_current_tab(self):
        if not self.count():
            return None
        file = self.currentWidget().get_file()
        self.removeTab(self.currentIndex())
        return file

    def close_all_tabs(self):
        self.clear()
