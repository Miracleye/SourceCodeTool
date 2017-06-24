from PyQt5.QtWidgets import QAction, QMainWindow

from core.common import App
from core.common.config import FontHolder
from core.common.uilang import UILangHolder
from res.resource import IconsHolder


class WindowFrame(QMainWindow):
    """ This is a window frame that only has a simple menu bar and three custom signals,
        and it can hold other widget by calling the method @setCentralWidget()
    """

    def __init__(self, parent=None):
        super(WindowFrame, self).__init__(parent)
        self.resize(800, 600)
        self._init_menu_bar()
        self.update_ui()
        self._init_signals()

    def _init_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu(UILangHolder.get(App.MENU_FILE))
        self.export_act = QAction(self)
        self.export_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_OPEN))
        self.import_act = QAction(self)
        self.import_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_CLOSE))
        self.exit_act = QAction(self)
        self.exit_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_EXIT))
        self.file_menu.addAction(self.export_act)
        self.file_menu.addAction(self.import_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)

    def _init_signals(self):
        pass
        # self.export_act.triggered.connect(self.sig_export_request)
        # self.import_act.triggered.connect(self.sig_import_request)
        # self.exit_act.triggered.connect(self._exit)

    def update_ui(self):
        font = FontHolder.get()
        self.export_act.setFont(font)
        self.export_act.setText(UILangHolder.get(App.EXPORT))
        self.import_act.setFont(font)
        self.import_act.setText(UILangHolder.get(App.IMPORT))
        self.exit_act.setFont(font)
        self.exit_act.setText(UILangHolder.get(App.EXIT))
