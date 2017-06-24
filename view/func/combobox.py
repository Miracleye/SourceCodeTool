import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox

from core.common import App
from core.common.uilang import UILangHolder


class FilterComboBox(QComboBox):
    def __init__(self, parent=None):
        super(FilterComboBox, self).__init__(parent)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setAutoFillBackground(True)
        self.setInsertPolicy(QComboBox.InsertAtBottom)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setDuplicatesEnabled(True)
        # The font is set by self
        font = QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.setFont(font)
        self.setCurrentText(UILangHolder.get(App.FILTER))
        self.addItem("All types")
        self.addItem("Assembly (*.s;*.S)")
        self.addItem("C (*.c)")
        self.addItem("C++ (*.cpp;*.C;*.cc;*.cxx;*.c++)")
        self.addItem("Header (*.h;*.hpp;*.hxx)")
        self.addItem("Java (*.java)")
        self.addItem("Python (*.py)")
        self.addItem("C# (*.cs)")
        self.addItem("Shell (*.sh)")
        self.pattern = re.compile("[^(]*?(?=\))")  # match the content in ()

    def get_filter_text(self, index):
        if index and index < self.count():
            text = self.itemText(index)
            content = re.search(self.pattern, text)
            filter_text = content.group(0)
            return filter_text
