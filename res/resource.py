from PyQt5.QtGui import QIcon

from res import apprcc


class IconsHolder:
    """ The class holds all the icons that the application will use,
        by calling the class method to get icon(s).
    """

    _icons = None
    _ext_id_map = {"unknown": 0, "": 0,
                   "dir": 1,
                   ".S": 2, ".s": 2,
                   ".c": 3, ".cpp": 3, ".cc": 3, ".C": 3, ".cxx": 3, ".c++": 3,
                   ".h": 4, ".hpp": 4, ".hxx": 4,
                   ".java": 5,
                   ".py": 6,
                   ".cs": 7,
                   ".sh": 8,
                   ".html": 9, ".htm": 9,
                   ".xml": 10,
                   ".json": 11,
                   ".txt": 12
                   }

    _EMAP_SIZE = 13  # max id of EXT_ID_MAP can map plus 1
    ID_OPEN = _EMAP_SIZE
    ID_OPEN_DIR = _EMAP_SIZE + 1
    ID_CLOSE = _EMAP_SIZE + 2
    ID_CLOSE_ALL = _EMAP_SIZE + 3
    ID_EXIT = _EMAP_SIZE + 4
    ID_FIND = _EMAP_SIZE + 5
    ID_FIND_DIR = _EMAP_SIZE + 6
    ID_CALC = _EMAP_SIZE + 7
    ID_LOGO = _EMAP_SIZE + 8

    def __init__(self):
        pass

    @classmethod
    def get_icons(cls):
        """ Get the icons tuple, if @self._icons is None, do initialization """
        if cls._icons:
            return cls._icons
        cls._icons = (
            QIcon(":image/unknown.png"),
            QIcon(":image/dir.png"),
            QIcon(":image/asm.png"),
            QIcon(":image/cpp.png"),
            QIcon(":image/h.png"),
            QIcon(":image/java.png"),
            QIcon(":image/py.png"),
            QIcon(":image/cs.png"),
            QIcon(":image/sh.png"),
            QIcon(":image/html.png"),
            QIcon(":image/xml.png"),
            QIcon(":image/json.png"),
            QIcon(":image/txt.png"),
            QIcon(":image/open.png"),
            QIcon(":image/open_dir.png"),
            QIcon(":image/close.png"),
            QIcon(":image/close_all.png"),
            QIcon(":image/exit.png"),
            QIcon(":image/find.png"),
            QIcon(":image/find_dir.png"),
            QIcon(":image/calculate.png"),
            QIcon(":image/logo.png")
        )
        return cls._icons

    @classmethod
    def get_ext_id_map(cls):
        return cls._ext_id_map

    @classmethod
    def get_by_ext(cls, ext: str= "unknown"):
        """ By passing the file extension to get corresponding icon, return the 'unknown' icon as default
        :param ext:
        :return:
        """
        if not cls._icons:  # icons are not initialized
            cls.get_icons()
        if ext in cls._ext_id_map.keys():
            return cls._icons[cls._ext_id_map[ext]]
        else:
            return cls._icons[0]

    @classmethod
    def get_by_id(cls, idx: int=0):
        """ By passing the index to get icon in @self._icons, return the 'unknown' icon as default
         :exception: @idx beyonds the length
         """
        if not cls._icons:
            cls.get_icons()
        return cls._icons[idx]
