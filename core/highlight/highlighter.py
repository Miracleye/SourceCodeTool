import re

from PyQt5.QtGui import QSyntaxHighlighter, QTextDocument, QColor, QTextCharFormat

from core.common import App
from core.highlight.parser import LanguageParser
from core.highlight.rule import to_rgb, HighlightRulesHolder, HighlightRule
from core.highlight.theme import ThemesHolder


class BaseHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument, ext):
        super(BaseHighlighter, self).__init__(parent)
        self.default_rule = HighlightRulesHolder.default_rule(ext)
        self.keywords_rules = HighlightRulesHolder.keywords_rules(ext)
        self.number_rule = HighlightRulesHolder.number_rule(ext)
        self.string_rule = HighlightRulesHolder.string_rule(ext)
        self.comment_line_rule = HighlightRulesHolder.comment_line_rule(ext)

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.default_rule.text_format)
        if self.keywords_rules:
            for rule in self.keywords_rules:
                matched = rule.pattern.search(text)
                while matched:
                    self.setFormat(matched.start(), matched.end() - matched.start(), rule.text_format)
                    matched = rule.pattern.search(text, matched.end())
        if self.number_rule:
            matched = self.number_rule.pattern.search(text)
            while matched:
                self.setFormat(matched.start(), matched.end() - matched.start(), self.number_rule.text_format)
                matched = self.number_rule.pattern.search(text, matched.end())
        if self.string_rule:
            matched = self.string_rule.pattern.search(text)
            while matched:
                self.setFormat(matched.start(), matched.end() - matched.start(), self.string_rule.text_format)
                matched = self.string_rule.pattern.search(text, matched.end())

    @classmethod
    def create(cls, document, ext):
        language = LanguageParser.get(ext)
        if not language:
            return
        if language.get('name') == 'c' or language.get('name') == 'cpp':
            return CHighlighter(document, ext)
        elif language.get('name') == 'java':
            return JavaHighlighter(document, ext)
        elif language.get('name') == 'python':
            return PyHighlighter(document, ext)
        else:
            return None


class CHighlighter(BaseHighlighter):
    def __init__(self, parent: QTextDocument, ext):
        super(CHighlighter, self).__init__(parent, ext)
        self.preprocessor_rule = HighlightRule()
        self.preprocessor_rule.pattern = re.compile(r'^\s*#[^\n]*')
        color = ThemesHolder.get_lexer('c', "Preprocessor")
        fg_color = to_rgb(color[0])
        bg_color = to_rgb(color[1])
        self.preprocessor_rule.text_format = QTextCharFormat()
        self.preprocessor_rule.text_format.setForeground(QColor(*fg_color))
        self.preprocessor_rule.text_format.setBackground(QColor(*bg_color))
        language = LanguageParser.get(ext)
        self.comment_start = language.get(App.COMMENT_START)
        self.comment_end = language.get(App.COMMENT_END)

    def highlightBlock(self, text):
        super(CHighlighter, self).highlightBlock(text)
        matched = self.preprocessor_rule.pattern.match(text)
        if matched:
            self.setFormat(matched.start(), matched.end() - matched.start(), self.preprocessor_rule.text_format)
        if self.comment_line_rule:
            matched = self.comment_line_rule.pattern.search(text)
            if matched:
                self.setFormat(matched.start(), matched.end() - matched.start(), self.comment_line_rule.text_format)
        if self.comment_start and self.comment_end:
            self.setCurrentBlockState(0)
            start_index = 0
            if self.previousBlockState() != 1:
                start_index = text.find(self.comment_start, 0)
            while start_index >= 0:
                end_index = text.find(self.comment_end, start_index)
                if end_index == -1:
                    self.setCurrentBlockState(1)
                    comment_length = len(text) - start_index
                else:
                    comment_length = end_index - start_index + len(self.comment_end)
                self.setFormat(start_index, comment_length, self.comment_line_rule.text_format)
                start_index = text.find(self.comment_start, start_index + comment_length)


class JavaHighlighter(BaseHighlighter):
    def __init__(self, parent: QTextDocument, ext):
        super(JavaHighlighter, self).__init__(parent, ext)
        language = LanguageParser.get(ext)
        self.comment_start = language.get(App.COMMENT_START)
        self.comment_end = language.get(App.COMMENT_END)

    def highlightBlock(self, text):
        super(JavaHighlighter, self).highlightBlock(text)
        if self.comment_line_rule:
            matched = self.comment_line_rule.pattern.search(text)
            if matched:
                self.setFormat(matched.start(), matched.end() - matched.start(), self.comment_line_rule.text_format)
        if self.comment_start and self.comment_end:
            self.setCurrentBlockState(0)
            start_index = 0
            if self.previousBlockState() != 1:
                start_index = text.find(self.comment_start, 0)
            while start_index >= 0:
                end_index = text.find(self.comment_end, start_index)
                if end_index == -1:
                    self.setCurrentBlockState(1)
                    comment_length = len(text) - start_index
                else:
                    comment_length = end_index - start_index + len(self.comment_end)
                self.setFormat(start_index, comment_length, self.comment_line_rule.text_format)
                start_index = text.find(self.comment_start, start_index + comment_length)


class PyHighlighter(BaseHighlighter):
    def __init__(self, parent: QTextDocument, ext):
        super(PyHighlighter, self).__init__(parent, ext)
        self.doc_string_start = '"""'
        self.doc_string_end = '"""'

    def highlightBlock(self, text):
        super(PyHighlighter, self).highlightBlock(text)
        if self.comment_line_rule:
            matched = self.comment_line_rule.pattern.search(text)
            if matched:
                self.setFormat(matched.start(), matched.end() - matched.start(), self.comment_line_rule.text_format)
        if self.doc_string_start and self.doc_string_end:
            self.setCurrentBlockState(0)
            start_index = 0
            if self.previousBlockState() != 1:
                start_index = text.find(self.doc_string_start, 0)
            while start_index >= 0:
                end_index = text.find(self.doc_string_end, start_index + 3)
                if end_index == -1:
                    self.setCurrentBlockState(1)
                    length = len(text) - start_index
                else:
                    length = end_index - start_index + len(self.doc_string_end)
                self.setFormat(start_index, length, self.string_rule.text_format)
                start_index = text.find(self.doc_string_start, start_index + length)
