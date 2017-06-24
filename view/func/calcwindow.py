from core.common import App
from core.common.uilang import UILangHolder
from core.file import open_file
from view.func.calcwidget import CalcWidget
from view.func.frame import WindowFrame


class CalcWindow(WindowFrame):
    def __init__(self, controller, parent=None):
        super(CalcWindow, self).__init__(parent)
        self.controller = controller
        self.setWindowTitle(UILangHolder.get(App.CALC_WINDOW_TITLE))
        self.widget = CalcWidget(controller, self)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(open_file("./res/css/func.css"))
        self.exit_act.triggered.connect(self._exit)

    def get_dir(self):
        return self.widget.dir_edit.text()

    def get_filters(self):
        return self.widget.get_filters()

    def set_result_table(self, model):
        self.widget.set_result_table(model)

    def reset_ui(self):
        self.export_act.setEnabled(True)
        self.import_act.setEnabled(True)
        self.widget.reset_ui()

    def set_ui(self):
        self.export_act.setEnabled(False)
        self.import_act.setEnabled(False)
        self.widget.set_ui()

    def _exit(self):
        self.controller.quit()

    def closeEvent(self, *args, **kwargs):
        self.controller.quit()
