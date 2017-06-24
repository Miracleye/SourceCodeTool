import codecs
import re

from PyQt5.QtGui import QFont

from core.common import App
from util.error import ConfigError

""" default configurations for application """
default_configs = {
    App.CONFIG_TOOL_BAR: "True",
    App.CONFIG_LANG: "English",
    App.CONFIG_THEME: "Default",
    App.CONFIG_FONT: "微软雅黑",
    App.CONFIG_FONT_SIZE: "11",
    App.CONFIG_BOLD: "False",
    App.CONFIG_ITALIC: "False",
    App.CONFIG_UNDERLINE: "False"
}
comment = re.compile(r'\s*#')
valid_item = re.compile(r'[\w\d\s]+')


# load config file
def load_configs(config_file):
    file = codecs.open(config_file, encoding='utf-8')
    try:
        config = {}
        for line in file:
            if re.match(comment, line):  # line comment is ignored
                continue
            item = line.split('=')
            config[item[0].strip()] = item[1].strip()
        # do validation, make sure all the configurations exist
        for key in default_configs.keys():
            if key not in config.keys():
                return default_configs
        return config
    except Exception as error:
        return default_configs
    finally:
        file.close()


def save_configs(config_file, configs: dict):
    file = codecs.open(config_file, mode='w', encoding='utf-8')
    try:
        for key, value in configs.items():
            file.write(key + ' = ' + value + '\n')
    except Exception as error:
        pass
    finally:
        file.close()


class ConfigsHolder:
    _configs = {}

    def __init__(self):
        pass

    @classmethod
    def get_configs(cls):
        """ Get all configs, return a dict """
        if not cls._configs:
            cls._configs = load_configs(App.default_config_file)
        return cls._configs

    @classmethod
    def get(cls, key: str):
        """ Get a config by passing a key, if no such config, return None.
        :param key:
        :return: @cls._configs[key]
        """
        if cls._configs:
            return cls._configs.get(key)
        return cls.get_configs().get(key)

    @classmethod
    def modify(cls, key, value):
        """ Modify config by passing a key and a new value, if the key doesn't exist, error occurs.
        :param key:
        :param value:
        :exception: @ConfigError
        """
        if key in cls._configs.keys():
            cls._configs[key] = str(value)
        else:
            raise ConfigError("Not such configuration")

    @classmethod
    def save(cls):
        """ Save all configurations to config file. """
        save_configs(App.default_config_file, cls._configs)


class FontHolder:
    _font = None

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        if cls._font:
            return cls._font
        cls._font = QFont()
        cls._font.setFamily(ConfigsHolder.get(App.CONFIG_FONT))
        cls._font.setPointSize(int(ConfigsHolder.get(App.CONFIG_FONT_SIZE)))
        if ConfigsHolder.get(App.CONFIG_BOLD) == "True":
            cls._font.setBold(True)
        if ConfigsHolder.get(App.CONFIG_ITALIC) == "True":
            cls._font.setItalic(True)
        if ConfigsHolder.get(App.CONFIG_UNDERLINE) == "True":
            cls._font.setUnderline(True)
        return cls._font

    @classmethod
    def set(cls, font: QFont):
        if cls._font == font:
            return
        cls._font = font
        ConfigsHolder.modify(App.CONFIG_FONT, cls._font.family())
        ConfigsHolder.modify(App.CONFIG_FONT_SIZE, cls._font.pointSize())
        ConfigsHolder.modify(App.CONFIG_BOLD, cls._font.bold())
        ConfigsHolder.modify(App.CONFIG_ITALIC, cls._font.italic())
        ConfigsHolder.modify(App.CONFIG_UNDERLINE, cls._font.underline())
