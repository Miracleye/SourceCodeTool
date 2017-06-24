from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

from core.common.config import FontHolder


class MessageBox:

    @classmethod
    def warning(cls, parent, title, content):
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(content)
        box.setStandardButtons(QMessageBox.Apply)
        box.setFont(FontHolder.get())
        fg = box.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        return box

    @classmethod
    def message(cls, parent, title, content):
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(content)
        box.setStandardButtons(QMessageBox.Yes)
        box.setFont(FontHolder.get())
        fg = box.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        return box
