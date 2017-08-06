import codecs
import re


class Grep:
    def __init__(self):
        self.pattern = None

    def clear(self):
        self.pattern = None

    def grep(self, file, regex):
        pattern = re.compile(regex)
        found = []
        f = codecs.open(file, encoding='utf-8')
        try:
            text = f.read()
            matched = pattern.search(text)
            while matched:
                found.append(text[matched.start(): matched.end()] + '\n')
                matched = pattern.search(text, matched.end())
            return found, None
        except Exception as err:
            return found, str(err.args)
        finally:
            f.close()

    def find(self, file, target):
        found = list()
        f = codecs.open(file, encoding='utf-8')
        try:
            for line in f:
                if line.find(target) != -1:
                    found.append(line)
            return found, None
        except Exception as err:
            return found, str(err.args)
        finally:
            f.close()
