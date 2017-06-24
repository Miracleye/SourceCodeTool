def get_next(t, next_list):
    j, k = 0, -1
    next_list[0] = -1
    while j < len(next_list) - 1:
        if k == -1 or t[j] == t[k]:
            j += 1
            k += 1
            next_list[j] = k
        else:
            k = next_list[k]
    return next_list


def KMP_search(text, pattern, start=0):
    t_len = len(text) - start
    p_len = len(pattern)
    if t_len >= p_len:
        i, j = 0, 0
        next_list = [-2 for i in range(p_len)]
        get_next(pattern, next_list)
        while i < t_len and j < p_len:
            if j == -1 or text[start + i] == pattern[j]:
                i += 1
                j += 1
            else:
                j = next_list[j]
            if j == p_len:
                return i - p_len
    return -1


class KMPSearch:
    def __init__(self):
        self.pattern = None
        self.next_list = None

    def set_pattern(self, pattern):
        self.pattern = pattern
        next_list = [-2 for i in range(len(pattern))]
        self.next_list = get_next(pattern, next_list)

    def search(self, text, start):
        t_len = len(text) - start
        p_len = len(self.pattern)
        if t_len >= p_len:
            i, j = 0, 0
            while i < t_len and j < p_len:
                if j == -1 or text[start + i] == self.pattern[j]:
                    i += 1
                    j += 1
                else:
                    j = self.next_list[j]
                if j == p_len:
                    return i - p_len
        return -1
