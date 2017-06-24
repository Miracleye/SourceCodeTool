""" define the Const class which can be use for define
    const variable """


class ConstError(TypeError):
    pass


class Const:

    def __setattr__(self, key, value):
        if self.__dict__[key] is not None:
            raise ConstError("Constant Assignment Error")
        self.__dict__[key] = value


Const.CPP = 1
Const.H = 2
Const.JAVA = 3
Const.PY = 4
Const.SH = 5
