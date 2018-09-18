from Stack import Stack
import constants, operator, exceptions

class Board:
    def __init__(self):
        self.board = []

        # create the board and references
        for col in constants.COLUMNS:
            n = []

            for row in constants.ROWS:
                n += [self.Node(col, row)]

            self.board += [n]

        # establish all knight moves
        vertDif = [2, 1, -1, -2, -2, -1, 1, 2]
        horzDif = [1, 2, 2, 1, -1, -2, -2, -1]

        for row in range(0, 8):
            for col in range(0, 8):
                for i in range(0, 8):
                    tempRow = row + vertDif[i]
                    tempCol = col + horzDif[i]

                    if tempRow in range(0, 8) and tempCol in range(0, 8):
                        self.board[row][col].add_connection(self.board[tempRow][tempCol])

        # sort all connections from each square based on possible moves from those connections
        for row in range(0, 8):
            for col in range(0, 8):
                self.board[row][col].connections = sorted(self.board[row][col].connections, key=operator.methodcaller('get_possible_moves'))

    def __get_node(self, column, row):
        """Returns the specified board square"""

        if column not in constants.COLUMNS:
            raise exceptions.InvalidColumnError(column)
        if row not in constants.ROWS:
            raise exceptions.InvalidRowError(row)

        return self.board[constants.COLUMNS.index(column)][constants.ROWS.index(row)]

    def knights_tour(self, column, row):
        """performs a knight's tour of a 8x8 chess board from the given starting location
           returns a list containing the 64 moves required"""

        currNode = self.__get_node(column, row)
        currNode.visit()

        # update all connections' degrees and sort their connections by degree in ascending order
        for node in currNode.connections:
            node.connections = sorted(node.connections, key=operator.methodcaller('get_possible_moves'))

        stack = Stack()
        stack.push([currNode, 0]) # first element represents current square, second element which connection number it took

        while True:
            # knight's tour is complete
            if stack.size() == 64:
                moveList = []

                for i in range(0, stack.size()):
                    moveList += [str(stack.items[i][0])]

                return moveList

            stackElement = stack.peek()
            stackNode = stackElement[0]
            stackNum = stackElement[1]

            # there is a valid move from this square
            if stackNode.get_possible_moves() != 0 and stackNum < len(stackNode.connections):
                while stackNode.connections[stackNum].visited:
                    stackNum += 1

                # update stack if the stackNum was changed
                if stackNum != stackElement[1]:
                    stack.pop()
                    stack.push([stackNode, stackNum])

                nextNode = stackNode.connections[stackNum]
                nextNode.visit()

                for node in nextNode.connections:
                    node.connections = sorted(node.connections, key=operator.methodcaller('get_possible_moves'))

                # add this square to the path and assume the first connection from this square is valid
                stack.push([nextNode, 0])

            # there is no valid move from this square
            else:
                # this path isn't valid, so "undo" it
                stackNode = stack.pop()[0]
                stackNode.unvisit()

                # update all connections' degrees and sort their connections by degree in ascending order
                for node in stackNode.connections:
                    node.connections = sorted(node.connections, key=operator.methodcaller('get_possible_moves'))

    class Node:
        """Represents a square on the chess board"""

        def __init__(self, column, row):
            # columns are letters A-H, rows are numbers 1-8

            if column not in constants.COLUMNS:
                raise exceptions.InvalidColumnError(column)
            if row not in constants.ROWS:
                raise exceptions.InvalidRowError(row)

            self.col = column
            self.row = row
            self.visited = False
            self.connections = []

        def visit(self):
            """visits the current square, throws an error if already visited"""

            if not self.visited:
                self.visited = True
            else:
                raise exceptions.VisitError("Already visited")

        def un_visit(self):
            """unvisits the current square, throws an error if not been visited"""

            if self.visited:
                self.visited = False
            else:
                raise exceptions.VisitError("Has not been visited")

        def get_possible_moves(self):
            """Returns the number of possible knight moves from this square"""
            count = 0

            for node in self.connections:
                if not node.visited:
                    count += 1

            return count

        def add_connection(self, node):
            self.connections += [node]

        def __str__(self):
            return self.col + self.row

if __name__ == '__main__':
    raise exceptions.ModuleError()