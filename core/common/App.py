""" This module defined most of Constants that application will use,
"""

APP_NAME = "SourceCodeTool"


""" Define key constants for core.common.lang module, other module use these to access language value.
    Register constant before use.
"""
WINDOW_TITLE = "WindowTitle"
MENU_BAR = "MenuBar"
MENU_FILE = "FileMenu"
MENU_VIEW = "ViewMenu"
MENU_FUNC = "FunctionMenu"
MENU_THEME = "ThemeMenu"
MENU_HELP = "HelpMenu"
OPEN = "Open"
OPEN_DIR = "OpenDir"
CLOSE = "Close"
CLOSE_ALL = "CloseAll"
CLEAR = "ClearCache"
EXIT = "Exit"
TOOL_BAR = "ToolBar"
THEME = "Theme"
FONT = "Font"
LANG = "Language"
FIND = "Find"
FIND_DIR = "FindDir"
CALC = "Calculate"
HELP = "Help"
EXPORT = "Export"
IMPORT = "Import"
CALC_WINDOW_TITLE = "CalcWindowTitle"
FIND_WINDOW_TITLE = "FindWindowTitle"
DIR_LABEL = "DirLabel"
TARGET_LABEL = "TargetLabel"
FILTER_LABEL = "FilterLabel"
DIR_HINT = "Hint"
LOCATION = "Location"
SIZE = "Size"
LINES = "Lines"
TOTAL_LINES = "TotalLines"
WORDS = "Words"
ERROR_INFO = "ErrorInfo"
FOUND = "Found"
FILTER = "Filter"
START = "Start"
PAUSE = "Pause"
STOP = "Stop"
REGEX = "Regex"

LANG_TYPE = "name"


""" belows are used by core.common.config module """
CONFIG_TOOL_BAR = TOOL_BAR
CONFIG_LANG = LANG
CONFIG_THEME = THEME
CONFIG_FONT = FONT
CONFIG_FONT_SIZE = "FontSize"
CONFIG_BOLD = "Bold"
CONFIG_ITALIC = "Italic"
CONFIG_UNDERLINE = "Underline"
config_set = {
    CONFIG_TOOL_BAR, CONFIG_LANG, CONFIG_THEME, CONFIG_FONT, CONFIG_FONT_SIZE, CONFIG_BOLD,
    CONFIG_ITALIC
}


""" belows are default settings for application """
default_config_file = "./res/config.ini"
default_ui_lang_file = "./res/UILanguage.xml"
default_langs_file = "./res/langs.xml"
default_theme_dir = "./res/themes/"
default_theme = "Default"
default_filters = {
    '.s', '.S',
    '.c',
    '.cpp', '.C', '.cc', '.cxx', '.c++',
    '.h', '.hpp', 'hxx',
    '.java', '.py', '.cs', '.sh'
}


""" used by core.highlight module """
EXT = "Ext"
NUMBER = "Number"
STRING = "String"
COMMENT = "Comment"
COMMENT_LINE = "CommentLine"
COMMENT_START = "CommentStart"
COMMENT_END = "CommentEnd"
KEYWORDS = "Keywords"
KEYWORD = "Keyword"

LEXER_TYPE = "LexerStyles"
GLOBAL_TYPE = "GlobalStyles"
FG_COLOR = "fgColor"
BG_COLOR = "bgColor"
