class InvalidColumnError(Exception):
    def __init__(self, column):
        Exception.__init__(self, column)

class InvalidRowError(Exception):
    def __init__(self, row):
        Exception.__init__(self, row)

class VisitError(Exception):
    pass

class EmptyStackError(Exception):
    pass

class ModuleError(Exception):
    def __init__(self):
        Exception.__init__(self, "This module is not meant to be run")

if __name__ == '__main__':
    raise ModuleError()
