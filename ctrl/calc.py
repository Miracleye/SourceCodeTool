import os
import threading

from core.calc import Calculator
from core.common import App
from core.model.model import CalcResultModel
from core.walk import DirWalker
from view.func.calcwindow import CalcWindow


class CalcController:
    def __init__(self, parent=None):
        self.ui = CalcWindow(self, parent)
        self._model = CalcResultModel()
        self.ui.set_result_table(self._model)
        self.calculator = Calculator()
        self._t = None  # thread to update the model
        self._t_busy = False
        self.ui.show()

    def do_request(self):
        base_dir = self.ui.get_dir()
        filters = self.ui.get_filters()
        if os.path.isdir(base_dir):
            self.delete_model()
        if not filters:
            filters = App.default_filters
        self._t_busy = True
        self._t = threading.Thread(target=self.update_model,
                                   args=(base_dir, filters,))
        self._t.setDaemon(True)
        self._t.start()

    def stop_operation(self):
        self._t_busy = False

    def get_model(self):
        if not self._model:
            self._model = CalcResultModel()
        return self._model

    def update_model(self, base_dir, filters):
        self.calculator.clear()
        walker = DirWalker(base_dir, filters)
        file_iter = iter(walker)
        result = list()
        for file, ext in file_iter:
            if self._t_busy:
                result.append(file)
                size_kb = os.path.getsize(file) / 1024
                result.append(round(size_kb, 2))
                result.extend(self.calculator.count(file, ext))
                self._model.append_result(result)
                result.clear()
            else:
                break
        self._model.append_result(["Total", 0, self.calculator.code_lines, self.calculator.total_lines, 0, None])
        # the operation is done, update ui state
        self.ui.reset_ui()

    def delete_model(self):
        self._model.clear()

    def quit(self):
        self.stop_operation()
        self.ui.close()
