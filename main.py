import sys

from PyQt5.QtWidgets import QApplication

from core.common import App
from core.common.config import ConfigsHolder
from core.common.uilang import UILangHolder
from ctrl.app import AppController

if __name__ == '__main__':
    config = ConfigsHolder.get_configs()
    UILangHolder.get_ui_lang(config[App.CONFIG_LANG])
    app = QApplication(sys.argv)
    instance = AppController()
    sys.exit(app.exec_())
