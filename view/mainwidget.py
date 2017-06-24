from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSplitter


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # self.resize(1000, 800)
        # self.splitter = QSplitter(Qt.Horizontal, self)
        # self.splitter.addWidget(QTextEdit(self.splitter))
        self._setup_ui()

    def _setup_ui(self):
        self.resize(1000, 800)
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.resize(1000, 800)
        self.splitter.addWidget(QWidget(self.splitter))
        # self.splitter.setHandleWidth(10)
        # self.dir_browser = DirBrowser(self.splitter)
        # self.dir_browser.resize(300, self.height())
        # self.code_browser = CodeBrowser(self.splitter)
        # self.dir_browser.setMouseTracking(True)
        # self.code_browser.setMouseTracking(True)
        # self.dir_browser.installEventFilter(self)
        # self.code_browser.installEventFilter(self)

    # def resizeEvent(self, event):
    #     self.splitter.setGeometry(0, 0, self.width(), self.height())
    #     QWidget.resizeEvent(event)

    # def eventFilter(self, obj: QObject, event: QEvent):
    #     if event.type() == QEvent.MouseMove:
    #         mouse_move =
