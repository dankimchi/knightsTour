import exceptions

class Stack:
    """represents the stack data structure (first in, last out)"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.size() == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise exceptions.EmptyStackError()

        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise exceptions.EmptyStackError()

        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

if __name__ == '__main__':
    raise exceptions.ModuleError()