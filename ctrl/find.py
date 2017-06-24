import os
import threading

from core.common import App
from core.grep import Grep
from core.model.model import FindResultModel
from core.walk import DirWalker
from view.func.findwindow import FindWindow


class FindController:
    def __init__(self, parent=None):
        self.ui = FindWindow(self, parent)
        self.model = FindResultModel()
        self.ui.set_result_table(self.model)
        self.greper = Grep()
        self._t = None  # thread to update the model
        self._t_busy = False
        self.ui.show()

    def do_request(self):
        base_dir = self.ui.get_dir()
        target = self.ui.get_target_string()
        filters = self.ui.get_filters()
        using_regex = self.ui.is_regex_enable()
        if os.path.isdir(base_dir):
            self.delete_model()
        if not filters:
            filters = App.default_filters
        self._t_busy = True
        self._t = threading.Thread(target=self.update_model,
                                   args=(base_dir, target, filters, using_regex,))
        self._t.setDaemon(True)
        self._t.start()

    def stop_operation(self):
        self._t_busy = False

    def get_model(self):
        if not self.model:
            self.model = FindResultModel()
        return self.model

    def update_model(self, base_dir, target, filters, using_regex):
        walker = DirWalker(base_dir, filters)
        file_iter = iter(walker)
        result = list()
        if using_regex:
            for file, ext in file_iter:
                if self._t_busy:
                    result.append(file)
                    result.extend(self.greper.grep(file, target))
                    if result[1]:
                        self.model.append_result(result)
                    result.clear()
                else:
                    break
        else:
            for file, ext in file_iter:
                if self._t_busy:
                    result.append(file)
                    result.extend(self.greper.find(file, target))
                    if result[1]:
                        self.model.append_result(result)
                    result.clear()
                else:
                    break
        # the operation is done, update ui state
        self.ui.reset()

    def delete_model(self):
        self.model.clear()

    def quit(self):
        self.stop_operation()
        self.ui.close()
