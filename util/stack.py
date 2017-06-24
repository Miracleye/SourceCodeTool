from collections import deque

from util.error import StackError


# Just for fun, it's awful
class Stack:
    def __init__(self):
        self._stack = deque()

    def push(self, data):
        self._stack.append(data)

    def pop(self):
        return self._stack.pop()

    def is_empty(self):
        return len(self._stack) == 0


class FixedStack(Stack):
    def __init__(self, size):
        super(FixedStack, self).__init__()
        self.max_size = size
        self.size = 0

    def push(self, data):
        if self.size < self.max_size:
            super(FixedStack, self).push(data)
            self.size += 1
        else:
            raise StackError("Stack is full")

    def pop(self):
        super(FixedStack, self).pop()
        self.size -= 1
