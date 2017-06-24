from xml.etree import ElementTree as ET

from core.common import App

default_langs = ["English"]
default_ui_lang = {
    App.WINDOW_TITLE: "SourceCodeTool",
    App.MENU_FILE: "File",
    App.MENU_VIEW: "View",
    App.MENU_FUNC: "Function",
    App.MENU_THEME: "Theme",
    App.MENU_HELP: "Help",
    App.TOOL_BAR: "ToolBar",
    App.OPEN: "Open",
    App.OPEN_DIR: "Open Folder",
    App.CLOSE: "Close",
    App.CLOSE_ALL: "Close All",
    App.EXIT: "Exit",
    App.FIND: "Find",
    App.FIND_DIR: "Find",
    App.CALC: "Calculate",
    App.CALC_WINDOW_TITLE: "Calculate",
    App.FIND_WINDOW_TITLE: "Find",
    App.DIR_LABEL: "Select Directory",
    App.DIR_HINT: "Please select a directory",
    App.START: "Start",
    App.STOP: "Stop",
    App.FILTER_LABEL: "Add Filters",
    App.FILTER: "Filter",
    App.TARGET_LABEL: "Target String",
    App.REGEX: "Enable Regex",
    App.LOCATION: "Location",
    App.SIZE: "Size",
    App.LINES: "Code Lines",
    App.TOTAL_LINES: "Total Lines",
    App.ERROR_INFO: "Error Information",
    App.WORDS: "Words",
    App.EXPORT: "Export",
    App.IMPORT: "Import"
}


def load_langs(lang_file):
    """ Load all lang types supported in @lang_file or @App.default_ui_lang_file.
    :param lang_file:
    :return:
    """
    try:
        lang_tree = ET.ElementTree(file=lang_file)
        lang_root = lang_tree.getroot()
        if lang_root.tag == App.APP_NAME:
            langs = []
            for child in lang_root:
                langs.append(child.attrib.get('name'))
            if langs:
                return langs
            else:
                return default_langs
        else:
            return default_langs
    except Exception:
        return default_langs


def load_lang(lang_file, lang_type: str):
    try:
        lang_tree = ET.ElementTree(file=lang_file)
        lang_root = lang_tree.getroot()
        if lang_root.tag == App.APP_NAME:
            lang = {}
            for child in lang_root:
                if child.attrib[App.LANG_TYPE] == lang_type:
                    lang[App.LANG_TYPE] = child.attrib[App.LANG_TYPE]
                    for e in child:
                        lang[e.tag] = e.text
                    break
            if lang:
                return lang
            else:
                return default_ui_lang
        else:
            return default_ui_lang
    except Exception:
        return default_ui_lang


# a little chaotic
class UILangHolder:
    """ The UILangHolder holds all supported UI language types, and only one language
        exists at any time while the application is running.
    """
    _langs = None  # UI language types
    _ui_lang = None

    def __init__(self):
        pass

    @classmethod
    def get_langs(cls):
        """ Get all lang types that defined in @AppConfig.default_ui_lang_file
        :return: @cls._langs
        """
        if cls._langs:
            return cls._langs
        cls._langs = load_langs(App.default_ui_lang_file)
        return cls._langs

    @classmethod
    def get(cls, key: str):
        if cls._ui_lang:
            return cls._ui_lang.get(key)
        return cls.get_ui_lang().get(key)

    @classmethod
    def get_ui_lang(cls, lang_type: str=None):
        if not cls._ui_lang:
            cls._ui_lang = load_lang(App.default_ui_lang_file, lang_type)
        if not lang_type:
            pass
        elif cls._ui_lang.get(App.LANG_TYPE) != lang_type:
            cls._ui_lang = load_lang(App.default_ui_lang_file, lang_type)
        return cls._ui_lang
