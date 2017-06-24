""" A switch-case class for internal use
"""


class Switch:
    def __int__(self):
        self.case = {}

    def add_case(self, name, value):
        self.case[name] = value
