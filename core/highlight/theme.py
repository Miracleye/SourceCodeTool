import os
import xml.etree.ElementTree as ET

from core.common import App


def _do_with_style(attrib: dict):
    """ Do with each style attribute, the XML format is defined like this:
        <Style name='' fgColor='' bgColor='' />. See also in the theme file.
    :return: a dict {name: (fgColor, bgColor)}
    """
    style = list()
    # all the string value is converted to lower case
    style.append(attrib.get(App.FG_COLOR).lower())
    style.append(attrib.get(App.BG_COLOR).lower())
    # return tuple(style)
    return {attrib.get('name'): tuple(style)}


def _do_with_lexer_styles(lexer_styles):
    styles = dict()
    for lexer_type in lexer_styles:
        style = dict()
        for words_style in lexer_type:
            style.update(_do_with_style(words_style.attrib))
        styles[lexer_type.attrib.get('name')] = style
    return styles


def _do_with_global_styles(global_styles):
    styles = dict()
    for widget_style in global_styles:
        styles.update(_do_with_style(widget_style.attrib))
    return styles


def _load_theme(theme_file: str):
    try:
        theme = {}
        tree = ET.ElementTree(file=theme_file)
        root = tree.getroot()
        if root.tag != App.APP_NAME:
            return None
        for child in root:
            if child.tag == App.LEXER_TYPE:
                theme[App.LEXER_TYPE] = _do_with_lexer_styles(child)
            elif child.tag == App.GLOBAL_TYPE:
                theme[App.GLOBAL_TYPE] = _do_with_global_styles(child)
        return theme
    except Exception as err:
        print(err)
        return None


class ThemesHolder:
    _themes = set()  # themes names are empty at first
    _theme = None

    def __init__(self):
        pass

    @classmethod
    def get_themes(cls):
        """ Get all theme types, all the theme files are under @App.default_theme_dir,
            and are stored as xml-format file.
        :return: @cls._themes
        """
        if os.path.isdir(App.default_theme_dir):
            for f in os.listdir(App.default_theme_dir):
                # if os.path.isfile(f):
                (name, ext) = os.path.splitext(f)
                cls._themes.add(name)
        else:
            cls._themes.add(App.default_theme)
        return cls._themes

    @classmethod
    def get_theme(cls, theme_name: str= App.default_theme):
        """ By passing the theme name to get theme. The return is a nested dict.
            This method will search the 'theme' directory, and load the matched
            theme file(a xml-format file). If nothing was matched, then return the
            default theme that defined in application.
        :param theme_name:
        :return: @cls._ui_theme
        """
        cls.get_themes()
        if theme_name in cls._themes:
            theme_file = theme_name + ".xml"
            theme_file = os.path.join(App.default_theme_dir, theme_file)
            if os.path.isfile(theme_file):
                cls._theme = _load_theme(theme_file)
                if cls._theme:
                    return cls._theme
                else:
                    return None

    @classmethod
    def get_lexer(cls, code_type, flag):
        if not cls._theme:
            cls.get_theme(App.default_theme)
        styles = cls._theme.get(App.LEXER_TYPE)
        for name, style in styles.items():
            if code_type == name:
                return style.get(flag)

    @classmethod
    def get_global(cls, flag):
        styles = cls._theme.get(App.GLOBAL_TYPE)
        for name, style in styles:
            pass
