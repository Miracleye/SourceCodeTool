import codecs
import re

from util.kmp import KMPSearch


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
        found = []
        KMP = KMPSearch()
        KMP.set_pattern(target)
        f = codecs.open(file, encoding='utf-8')
        try:
            for line in f:
                # if line.find(target) != -1:
                # if KMP_search(line, target) != -1:
                if KMP.search(line, 0) != -1:
                    found.append(line.lstrip())
            return found, None
        except Exception as err:
            return found, str(err.args)
        finally:
            f.close()
