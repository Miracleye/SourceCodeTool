from xml.etree import ElementTree as ET

from core.common import App


class LanguageParser:
    """ The languages is a list, each item is a dict that contains a type name, an extensions tuple,
        keywords tuple, comment line format, comment block start start and end format.
    """
    languages = list()

    def __init__(self):
        pass

    @classmethod
    def get(cls, ext):
        if not cls.languages:
            cls._parse(App.default_langs_file)
        for language in cls.languages:
            if ext in language.get(App.EXT):
                return language
        return None

    @classmethod
    def _parse(cls, file_path):
        tree = ET.ElementTree(file=file_path)
        root = tree.getroot()
        if root.tag != App.APP_NAME:
            raise Exception()
        if root[0].tag != 'Languages':
            raise Exception()
        for lang in root[0]:
            language = dict()
            language['name'] = lang.attrib.get('name')
            exts = lang.attrib.get(App.EXT).strip().split()
            language[App.EXT] = tuple(exts)
            language[App.COMMENT_LINE] = lang.attrib.get(App.COMMENT_LINE)
            language[App.COMMENT_START] = lang.attrib.get(App.COMMENT_START)
            language[App.COMMENT_END] = lang.attrib.get(App.COMMENT_END)
            keywords = list()
            for keywords_element in lang:
                keywords_text = keywords_element.text.strip()
                keywords.extend(keywords_text.split())
            language[App.KEYWORDS] = tuple(keywords)
            cls.languages.append(language)
