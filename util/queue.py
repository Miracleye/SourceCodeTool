""" defined queue operations
"""
from collections import deque


class QueueError(Exception):
    def __init__(self, info):
        super(QueueError, self).__init__(info)


# class Queue:
#     def __init__(self, max_size=10):
#         self.size = 0
#         self.max_size = max_size
#         self.head.next = self.tail
#         self.tail.next = self.head
#
#     def enqueue(self, item):
#         if not self.is_full():
#             self.tail.next.data = item
#             self.tail = self.tail.next
#             self.size += 1
#         else:
#             raise QueueError("Enqueue Error")
#
#     def dequeue(self):
#         if not self.is_empty():
#             item = self.head.data
#             self.head = self.head.next
#             self.size -= 1
#             return item
#         else:
#             raise QueueError("Dequeue Error")
#
#     def is_empty(self):
#         return self.size == 0
#
#     def is_full(self):
#         return self.size == self.max_size


class Queue:
    def __init__(self):
        self.size = 0
        self.queue = deque()

    def enqueue(self, data):
        self.queue.append(data)
        self.size += 1

    def dequeue(self):
        if not self.is_empty():
            self.size -= 1
            return self.queue.popleft()
        return None

    def is_empty(self):
        return self.size == 0


class PriorityQueue(Queue):
    def __init__(self, max_size):
        super(PriorityQueue, self).__init__(max_size)

    def enqueue(self):
        pass

    def dequeue(self):
        pass
