import re

from PyQt5.QtGui import QColor, QTextCharFormat

from core.common import App
from core.highlight.parser import LanguageParser
from core.highlight.theme import ThemesHolder


class HighlightRule:
    def __init__(self, pattern=None, text_format=None):
        self.pattern = pattern
        self.text_format = text_format

    def set_pattern(self, pattern):
        self.pattern = pattern

    def set_format(self, text_format):
        self.text_format = text_format

    def get_pattern(self):
        return self.pattern

    def get_format(self):
        return self.text_format


class HighlightRulesHolder:
    """ NOTE: These methods are not thread-safe, and I didn't do many checks!
        Some string constants are not registered in core.common.App
    """
    _existed_rules = dict()

    def __init__(self):
        pass

    @classmethod
    def default_rule(cls, ext):
        language = LanguageParser.get(ext)
        if not language:
            return None
        name = language.get('name')
        exist_type = cls._existed_rules.get(name)
        # if rules has already existed, return them immediately
        if exist_type:
            default_rule = exist_type.get("Default")
            if default_rule:
                return default_rule
        else:
            cls._existed_rules[name] = dict()
        rule = HighlightRule()
        color = ThemesHolder.get_lexer(name, 'Default')
        fg_color = to_rgb(color[0])
        bg_color = to_rgb(color[1])
        rule.text_format = QTextCharFormat()
        rule.text_format.setForeground(QColor(*fg_color))
        rule.text_format.setBackground(QColor(*bg_color))
        cls._existed_rules.get(name)["Default"] = rule
        return rule

    @classmethod
    def keywords_rules(cls, ext):
        language = LanguageParser.get(ext)
        if not language:
            return None
        name = language.get('name')
        exist_type = cls._existed_rules.get(name)
        if exist_type:
            keywords_rules = exist_type.get(App.KEYWORDS)
            if keywords_rules:
                return keywords_rules
        else:
            cls._existed_rules[name] = dict()
        keywords_rules = list()
        text_format = QTextCharFormat()
        color = ThemesHolder.get_lexer(name, App.KEYWORDS)
        fg_color = to_rgb(color[0])
        bg_color = to_rgb(color[1])
        text_format.setForeground(QColor(*fg_color))
        text_format.setBackground(QColor(*bg_color))
        keywords = language.get(App.KEYWORDS)
        if keywords:
            for keyword in keywords:
                rule = HighlightRule()
                rule.pattern = re.compile(r'\b' + keyword + r'\b')
                rule.text_format = text_format
                keywords_rules.append(rule)
            keywords_rules = tuple(keywords_rules)  # convert to unchangeable structure
            cls._existed_rules.get(name)[App.KEYWORDS] = keywords_rules
            return keywords_rules
        else:
            return None

    @classmethod
    def number_rule(cls, ext):
        language = LanguageParser.get(ext)
        if not language:
            return None
        name = language.get('name')
        exist_type = cls._existed_rules.get(name)
        if exist_type:
            default_rule = exist_type.get(App.NUMBER)
            if default_rule:
                return default_rule
        else:
            cls._existed_rules[name] = dict()
        rule = HighlightRule()
        # match number: with prefix 0b, 0d, 0x, with suffix b, d, F, L, and so on
        rule.pattern = re.compile(r'(\b0[bBdDxX][0-9a-fA-F]+[lL]?)|(\b\d+\.?\d*?[bBdDfFlL]?)')
        color = ThemesHolder.get_lexer(name, App.NUMBER)
        fg_color = to_rgb(color[0])
        bg_color = to_rgb(color[1])
        rule.text_format = QTextCharFormat()
        rule.text_format.setForeground(QColor(*fg_color))
        rule.text_format.setBackground(QColor(*bg_color))
        cls._existed_rules.get(name)[App.NUMBER] = rule
        return rule

    @classmethod
    def string_rule(cls, ext):
        language = LanguageParser.get(ext)
        if not language:
            return None
        name = language.get('name')
        exist_type = cls._existed_rules.get(name)
        if exist_type:
            default_rule = exist_type.get(App.STRING)
            if default_rule:
                return default_rule
        else:
            cls._existed_rules[name] = dict()
        rule = HighlightRule()
        # common string pattern, words in ""
        rule.pattern = re.compile(r'\".*?\"')
        color = ThemesHolder.get_lexer(name, App.STRING)
        fg_color = to_rgb(color[0])
        bg_color = to_rgb(color[1])
        rule.text_format = QTextCharFormat()
        rule.text_format.setForeground(QColor(*fg_color))
        rule.text_format.setBackground(QColor(*bg_color))
        cls._existed_rules.get(name)[App.STRING] = rule
        return rule

    @classmethod
    def comment_line_rule(cls, ext):
        language = LanguageParser.get(ext)
        if not language:
            return None
        name = language.get('name')
        exist_type = cls._existed_rules.get(name)
        if exist_type:
            comment_line_rule = exist_type.get(App.COMMENT_LINE)
            if comment_line_rule:
                return comment_line_rule
        else:
            cls._existed_rules[name] = dict()
        comment_line = language.get(App.COMMENT_LINE)
        if comment_line:
            rule = HighlightRule()
            rule.pattern = re.compile(comment_line + r'[^\n]*')
            rule.text_format = QTextCharFormat()
            color = ThemesHolder.get_lexer(name, App.COMMENT_LINE)
            fg_color = to_rgb(color[0])
            bg_color = to_rgb(color[1])
            rule.text_format.setForeground(QColor(*fg_color))
            rule.text_format.setBackground(QColor(*bg_color))
            cls._existed_rules.get(name)[App.COMMENT_LINE] = rule
            return rule
        return None


def to_rgb(rgb):
    """ Convert the RGB color defined in the theme file to color tuple (r, g, b),
        the RGB format likes this (F0F0F0).
    """
    r = int(rgb[0:2], 16)
    g = int(rgb[2:4], 16)
    b = int(rgb[4:6], 16)
    return r, g, b
