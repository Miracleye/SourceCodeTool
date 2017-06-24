import codecs
import re


class Calculator:
    def __init__(self):
        self._ext_func_map = {
            ".S": self.do_cnt_asm,
            ".c": self.do_cnt_common,
            ".h": self.do_cnt_common, ".hpp": self.do_cnt_common, ".hxx": self.do_cnt_common,
            ".cpp": self.do_cnt_common, ".C": self.do_cnt_common, ".cxx": self.do_cnt_common,
            ".c++": self.do_cnt_common,
            ".java": self.do_cnt_common,
            ".cs": self.do_cnt_common,
            ".py": self.do_cnt_py,
            ".sh": self.do_cnt_py
        }
        self._ext_keys = self._ext_func_map.keys()
        self.blank = re.compile("^\s*$")
        self.cmt_line = re.compile(r'^\s*//')
        self.cmt_blk_start = re.compile(r'/\*')
        self.cmt_blk_end = re.compile(r'\*/')
        self.asm_cmt_line = re.compile(r'^\s*#')
        self.py_cmt_line = re.compile(r'^\s*#')
        self.total_files = 0
        self.total_lines = 0
        self.code_lines = 0

    def clear(self):
        self.total_files = 0
        self.total_lines = 0
        self.code_lines = 0

    def do_cnt_common(self, file):
        code_lines = 0
        lines = 0
        words = 0
        error = None
        f = codecs.open(file, encoding='utf-8')  # open file with utf-8 encoding
        try:
            cmt_blk_flag = False  # when block comment appears, set this flag
            for line in f:
                lines += 1
                words += len(line)
                if cmt_blk_flag and self.cmt_blk_end.search(line):
                    cmt_blk_flag = False
                    continue
                elif self.blank.match(line):  # blank line
                    continue
                elif self.cmt_line.match(line):  # line comment
                    continue
                elif self.cmt_blk_start.match(line):  # block comment starts at beginning
                    if self.cmt_blk_end.search(line):
                        cmt_blk_flag = True
                else:
                    code_lines += 1
        except UnicodeError as encoding_err:
            error = str(encoding_err.args)
        except Exception:
            error = "Error Occurred"
        finally:
            f.close()
            return code_lines, lines, words, error

    def do_cnt_py(self, file):
        code_lines = 0
        lines = 0
        words = 0
        error = None
        f = codecs.open(file, encoding='utf-8')
        try:
            for line in f:
                lines += 1
                words += len(line)
                if self.blank.match(line):
                    continue
                elif self.py_cmt_line.match(line):
                    continue
                else:
                    code_lines += 1
        except UnicodeError as encoding_err:
            error = str(encoding_err.args)
        except Exception:
            error = "Error Occurred"
        finally:
            f.close()
            return code_lines, lines, words, error

    def do_cnt_asm(self, file):
        code_lines = 0
        lines = 0
        words = 0
        error = None
        f = codecs.open(file, encoding='utf-8')
        try:
            cmt_blk_flag = False
            for line in f:
                lines += 1
                words += len(line)
                if cmt_blk_flag and self.cmt_blk_end.search(line):
                    cmt_blk_flag = False
                    continue
                elif self.blank.match(line):
                    continue
                elif self.cmt_line.match(line) or self.asm_cmt_line.match(line):
                    continue
                elif self.cmt_blk_start.match(line):
                    if self.cmt_blk_end.search(line):
                        cmt_blk_flag = True
                else:
                    code_lines += 1
        except UnicodeError as encoding_err:
            error = encoding_err.args[0]
        except Exception:
            error = "Error Occurred"
        finally:
            f.close()
            return code_lines, lines, words, error

    def do_cnt_sh(self, file):
        pass

    def count(self, file, ext):
        """ The method calculates each source code file and return code lines, total lines, words, and words.
            If error occurred while calculating, the error info also in the returns, else None.
            The method doesn't do these itself, instead, it dispatches each task by mapping @ext to @do_xxx(file).
        :param file: file path
        :param ext: file extension
        :return: the return is a tuple with format (code lines, lines, words, size, error info)
        """
        if ext in self._ext_keys:
            ret = self._ext_func_map[ext](file)
            self.total_files += 1
            self.code_lines += ret[0]
            self.total_lines += ret[1]
            return ret
        else:
            return 0, 0, 0, None
