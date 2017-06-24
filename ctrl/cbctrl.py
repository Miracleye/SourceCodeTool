import os


class CodeBrowserController:
    def __init__(self, parent=None):
        self.open_files = set()
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def get_ui(self):
        return self.ui

    def do_open_file(self, file):
        if os.path.isfile(file):
            if file in self.open_files:
                return
            self.ui.add_new(file)
            self.open_files.add(file)

    def do_close_file(self, file):
        self.open_files.remove(file)
        pass
