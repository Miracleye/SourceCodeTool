from PyQt5.QtCore import QDir, QSize
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QActionGroup, QFontDialog, QMenu

from core.common import App
from core.common.config import ConfigsHolder, FontHolder
from core.common.uilang import UILangHolder
from core.highlight.theme import ThemesHolder
from res.resource import IconsHolder


class AppFrame(QMainWindow):

    def __init__(self, controller=None, parent=None):
        super(AppFrame, self).__init__(parent)
        self.controller = controller
        # self.setStyleSheet('background-color: rgb(0, 44, 56)')
        self.setWindowTitle(UILangHolder.get(App.WINDOW_TITLE))
        self.setWindowIcon(IconsHolder.get_by_id(IconsHolder.ID_OPEN))
        self._init_actions()
        self._init_menu_bar()
        self._init_tool_bar()
        self.update_lang()
        self.update_font()
        self._init_signals()

    def closeEvent(self, *args, **kwargs):
        """ Override the window close event, let the controller save and exit
        """
        self.controller.do_exit()

    def update_lang(self):
        self.setWindowTitle(UILangHolder.get(App.WINDOW_TITLE))
        self.file_menu.setTitle(UILangHolder.get(App.MENU_FILE))
        self.view_menu.setTitle(UILangHolder.get(App.MENU_VIEW))
        self.func_menu.setTitle(UILangHolder.get(App.MENU_FUNC))
        self.help_menu.setTitle(UILangHolder.get(App.MENU_HELP))
        self.open_act.setText(UILangHolder.get(App.OPEN))
        self.open_act.setToolTip(UILangHolder.get(App.OPEN) + '(O)')
        self.open_dir_act.setText(UILangHolder.get(App.OPEN_DIR))
        self.open_dir_act.setToolTip(UILangHolder.get(App.OPEN_DIR) + '(O)')
        self.close_act.setText(UILangHolder.get(App.CLOSE))
        self.close_act.setToolTip(UILangHolder.get(App.CLOSE) + '(W)')
        self.close_all_act.setText(UILangHolder.get(App.CLOSE_ALL))
        self.close_all_act.setToolTip(UILangHolder.get(App.CLOSE_ALL) + '(W)')
        self.exit_act.setText(UILangHolder.get(App.EXIT))
        self.exit_act.setToolTip(UILangHolder.get(App.EXIT) + '(Q)')
        self.tool_bar_act.setText(UILangHolder.get(App.TOOL_BAR))
        self.tool_bar_act.setToolTip(UILangHolder.get(App.TOOL_BAR))
        self.font_act.setText(UILangHolder.get(App.FONT))
        self.font_act.setToolTip(UILangHolder.get(App.FONT))
        self.lang_menu.setTitle(UILangHolder.get(App.LANG))
        self.find_act.setText(UILangHolder.get(App.FIND))
        self.find_act.setToolTip(UILangHolder.get(App.FIND) + '(F)')
        self.find_dir_act.setText(UILangHolder.get(App.FIND_DIR))
        self.find_dir_act.setToolTip(UILangHolder.get(App.FIND_DIR) + '(F)')
        self.calc_act.setText(UILangHolder.get(App.CALC))
        self.help_act.setText(UILangHolder.get(App.HELP))

    def update_font(self):
        font = FontHolder.get()
        self.setFont(font)
        self.file_menu.setFont(font)
        self.view_menu.setFont(font)
        self.func_menu.setFont(font)
        self.help_menu.setFont(font)
        self.lang_menu.setFont(font)
        for action in self.lang_act_grp.actions():
            action.setFont(font)

    def _init_file_actions(self):
        # open file action
        self.open_act = QAction(self)
        self.open_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_OPEN))
        self.open_act.setShortcut("Ctrl+O")
        # open directory action
        self.open_dir_act = QAction(self)
        self.open_dir_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_OPEN_DIR))
        self.open_dir_act.setShortcut("Ctrl+Shift+O")
        # close file action
        self.close_act = QAction(self)
        self.close_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_CLOSE))
        self.close_act.setShortcut("Ctrl+W")
        # close all files action
        self.close_all_act = QAction(self)
        self.close_all_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_CLOSE_ALL))
        self.close_all_act.setShortcut("Ctrl+Shift+W")
        # exit application action
        self.exit_act = QAction(self)
        self.exit_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_EXIT))
        self.exit_act.setShortcut("Ctrl+Q")

    def _init_view_actions(self):
        self.tool_bar_act = QAction(self)
        self.tool_bar_act.setCheckable(True)
        if ConfigsHolder.get(App.TOOL_BAR) == "True":
            self.tool_bar_act.setChecked(True)
        self.font_act = QAction(self)
        self.lang_menu = QMenu(self)
        self.lang_act_grp = QActionGroup(self)
        for lang in UILangHolder.get_langs():
            action = QAction(lang, self)
            action.setFont(FontHolder.get())
            action.setCheckable(True)
            self.lang_menu.addAction(action)
            self.lang_act_grp.addAction(action)
            if UILangHolder.get(App.LANG_TYPE) == lang:
                action.setChecked(True)

    def _init_func_actions(self):
        # find all matches in current file action
        self.find_act = QAction(self)
        self.find_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_FIND))
        self.find_act.setShortcut("Ctrl+F")
        # find all matches in the whole dir action
        self.find_dir_act = QAction(self)
        self.find_dir_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_FIND_DIR))
        self.find_dir_act.setShortcut("Ctrl+Shift+F")
        self.find_act.setEnabled(False)
        # account function action
        self.calc_act = QAction(self)
        self.calc_act.setIcon(IconsHolder.get_by_id(IconsHolder.ID_CALC))
        self.calc_act.setShortcut("Ctrl+Alt+L")
        self.calc_act.setToolTip(UILangHolder.get(App.CALC))

    def _init_theme_actions(self):
        self.theme_act_group = QActionGroup(self)
        self.theme_acts = {}
        for theme in ThemesHolder.get_themes():
            self.theme_acts[theme] = QAction(theme, self)
            self.theme_acts[theme].setActionGroup(self.theme_act_group)
            self.theme_menu.addAction(self.theme_acts[theme])

    def _init_help_actions(self):
        self.help_act = QAction(self)
        # self.setIcon(IconsHolder.get_icon_by_id())

    def _init_actions(self):
        self._init_file_actions()
        self._init_view_actions()
        self._init_func_actions()
        self._init_help_actions()

    def _init_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu(UILangHolder.get(App.MENU_FILE))
        self.file_menu.setFont(FontHolder.get())
        self.open_act.setCheckable(False)
        self.file_menu.addAction(self.open_act)
        self.file_menu.addAction(self.open_dir_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_act)
        self.file_menu.addAction(self.close_all_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)
        self.view_menu = self.menu_bar.addMenu(UILangHolder.get(App.MENU_VIEW))
        self.view_menu.setFont(FontHolder.get())
        self.view_menu.addAction(self.tool_bar_act)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.font_act)
        self.view_menu.addMenu(self.lang_menu)
        self.func_menu = self.menu_bar.addMenu(UILangHolder.get(App.MENU_FUNC))
        self.func_menu.setFont(FontHolder.get())
        # self.func_menu.addAction(self.find_act)
        self.func_menu.addAction(self.find_dir_act)
        self.func_menu.addSeparator()
        self.func_menu.addAction(self.calc_act)
        self.help_menu = self.menu_bar.addMenu(UILangHolder.get(App.MENU_HELP))
        self.help_menu.setFont(FontHolder.get())

    def _init_tool_bar(self):
        # tool bar for base functions
        self.file_tool_bar = self.addToolBar("base")
        self.file_tool_bar.setIconSize(QSize(25, 25))
        self.file_tool_bar.setMovable(False)
        self.file_tool_bar.addAction(self.open_act)
        self.file_tool_bar.addAction(self.open_dir_act)
        self.file_tool_bar.addAction(self.close_act)
        self.file_tool_bar.addAction(self.close_all_act)
        self.file_tool_bar.addAction(self.exit_act)
        self.func_tool_bar = self.addToolBar("func")
        self.func_tool_bar.setIconSize(QSize(25, 25))
        self.func_tool_bar.setMovable(False)
        # self.func_tool_bar.addAction(self.find_act)
        self.func_tool_bar.addAction(self.find_dir_act)
        self.func_tool_bar.addAction(self.calc_act)
        self._change_tool_bar()

    def _open_file(self):
        home_path = QDir.homePath()
        file = QFileDialog.getOpenFileName(self, "Select File", home_path, "All Files (*.*)")
        self.controller.do_open_file(file[0])

    def _open_dir(self):
        home_path = QDir.homePath()
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "选择目录", home_path, options)
        if selected_dir:
            self.controller.do_open_dir(selected_dir)

    def _close_file(self):
        self.controller.do_close_file()

    def _close_all(self):
        self.controller.do_close_all()

    def _exit(self):
        self.controller.do_exit()

    def _change_tool_bar(self):
        hidden = not self.tool_bar_act.isChecked()
        self.file_tool_bar.setHidden(hidden)
        self.func_tool_bar.setHidden(hidden)
        self.controller.do_change_tool_bar(not hidden)

    def _change_font(self):
        font, ok = QFontDialog.getFont(FontHolder.get())
        if ok:
            self.controller.do_change_font(font)

    def _change_lang(self, action):
        lang_type = action.text()
        if lang_type:
            self.controller.do_change_lang(lang_type)

    def _find_file(self):
        # self.controller.do_find_file()
        self.controller.do_find_dir()

    def _find_dir(self):
        self.controller.do_find_dir()

    def _calculate(self):
        self.controller.do_calculate()

    def _change_theme(self, action):
        pass

    def _help(self):
        pass

    def _init_signals(self):
        self.open_act.triggered.connect(self._open_file)
        self.open_dir_act.triggered.connect(self._open_dir)
        self.close_act.triggered.connect(self._close_file)
        self.close_all_act.triggered.connect(self._close_all)
        self.exit_act.triggered.connect(self._exit)
        self.tool_bar_act.triggered.connect(self._change_tool_bar)
        self.font_act.triggered.connect(self._change_font)
        self.lang_act_grp.triggered.connect(self._change_lang)
        self.find_act.triggered.connect(self._find_file)
        self.find_dir_act.triggered.connect(self._find_dir)
        self.calc_act.triggered.connect(self._calculate)
        # self.theme_act_group.triggered.connect(self._change_theme)
        self.help_act.triggered.connect(self._help)
