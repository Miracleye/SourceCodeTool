class DirectoryExistsError(Exception):
    pass


class DirectoryError(Exception):
    pass


class ConfigError(Exception):
    pass


class QueueError(IndexError):
    pass


class StackError(IndexError):
    pass
