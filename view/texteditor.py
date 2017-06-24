import os

from PyQt5.QtCore import QRect, QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QResizeEvent
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit

from core.common.config import FontHolder
from core.highlight.highlighter import BaseHighlighter


class LineNumberWidget(QWidget):
    """ Used by the TextWidget
    """

    def __init__(self, parent=None):
        super(LineNumberWidget, self).__init__(parent)
        self.parent = parent
        self.setFont(FontHolder.get())

    def sizeHint(self):
        return QSize(self.parent.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.parent.repaint_line_number_area(event)


class TextEditor(QPlainTextEdit):
    EDITABLE = 1
    BROWSE = 2

    def __init__(self, file, text, parent=None):
        super(TextEditor, self).__init__(parent)
        self._file = file
        self.setTabStopWidth(40)
        self.setLineWrapMode(self.NoWrap)
        self.set_mode(self.EDITABLE)
        self.setPlainText(text)
        self._set_highlighter()
        self.line_number_area = LineNumberWidget(self)
        self.update_line_number_area_width(0)
        self.update_font()
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def update_line_number_area_width(self, unused: int):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect: QRect, dy: int):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def line_number_area_width(self):
        space = self.fontMetrics().width(str(self.blockCount())) + 10
        return space

    def resizeEvent(self, event: QResizeEvent):
        super(TextEditor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = list()
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def repaint_line_number_area(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingGeometry(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(-2, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingGeometry(block).height())
            block_number += 1

    def update_font(self):
        font = FontHolder.get()
        self.setFont(font)
        self.line_number_area.setFont(font)

    def set_mode(self, mode):
        if mode == self.BROWSE:
            self.setReadOnly(True)
            self.highlight_current_line()
        elif mode == self.EDITABLE:
            self.setReadOnly(False)
            self.highlight_current_line()

    def get_file(self):
        return self._file

    def get_text(self):
        return self.toPlainText()

    def _set_highlighter(self):
        if not self._file:
            return
        (name, ext) = os.path.splitext(self._file)
        self.highlighter = BaseHighlighter.create(self.document(), ext)


class TextEdit(QPlainTextEdit):
    """ Without Line number
    """
    EDITABLE = 1
    BROWSE = 2

    def __init__(self, file, text, parent=None):
        super(TextEdit, self).__init__(parent)
        self._file = file
        self.setFont(FontHolder.get())
        self.setTabStopWidth(40)
        self.setBackgroundVisible(True)
        self.setLineWrapMode(self.NoWrap)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.set_mode(self.BROWSE)
        self.setPlainText(text)
        self._set_highlighter()

    # def update_line_number_area_width(self, unused: int):
    #     self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    #
    # def update_line_number_area(self, rect: QRect, dy: int):
    #     if dy:
    #         self.line_number_area.scroll(0, dy)
    #     else:
    #         self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
    #     if rect.contains(self.viewport().rect()):
    #         self.update_line_number_area_width(0)
    #
    # def line_number_area_width(self):
    #     space = self.fontMetrics().width(str(self.blockCount())) + 10
    #     return space

    # def resizeEvent(self, event=None):
    #     # QPlainTextEdit.resizeEvent(event)
    #     cr = self.contentsRect()
    #     self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = list()
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    # def repaint_line_number_area(self, event):
    #     painter = QPainter(self.line_number_area)
    #     painter.fillRect(event.rect(), Qt.lightGray)
    #     block = self.firstVisibleBlock()
    #     block_number = block.blockNumber()
    #     top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
    #     bottom = top + int(self.blockBoundingGeometry(block).height())
    #     while block.isValid() and top <= event.rect().bottom():
    #         if block.isVisible() and bottom >= event.rect().top():
    #             number = str(block_number + 1)
    #             painter.setPen(Qt.black)
    #             painter.drawText(-2, top, self.line_number_area.width(), self.fontMetrics().heigth(),
    #                              Qt.AlignRight, number)
    #         block = block.next()
    #         top = bottom
    #         bottom = top + int(self.blockBoundingGeometry(block).height)
    #         block_number += 1

    def update_ui(self):
        font = FontHolder.get()
        self.setFont(font)

    def set_mode(self, mode):
        if mode == self.BROWSE:
            self.setReadOnly(True)
            self.highlight_current_line()
        elif mode == self.EDITABLE:
            self.setReadOnly(False)
            self.highlight_current_line()

    def get_file(self):
        return self._file

    def _set_highlighter(self):
        if not self._file:
            return
        (name, ext) = os.path.splitext(self._file)
        self.highlighter = BaseHighlighter.create(self.document(), ext)
