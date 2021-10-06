import random
import copy

class GameBoard:
    """ Represents a 9x9 Sudoku board.

    Implements the logistics of the board, and none of the algorithms, e.g.
    * Access (setting/getting values)
    * Determining validity, completion, etc...
    * Producing a printable board.
    """

    _board_size = 9
    _sub_board_size = 3
    _valid_values = list(range(1, 10))

    # Initialise the board as empty
    _board = [
            [None, None, None, None, None, None, None, None, None] for i in range(9)
        ]

    def board_iterator(self):
        """ Returns an iterator that goes over the whole board.

        Goes through each line, column by column, starting at line 0.
        Actually a generator. Fancy.
        """
        for i in range(self._board_size):
            for j in range(self._board_size):
                yield [i, j]

    def random_board_iterator(self):
        """ Returns an iterator that goes over the whole board randomly.
        """
        elements = list(self.board_iterator())
        random.shuffle(elements)
        for element in elements:
            yield element

    def random_valid_value(self):
        """ Returns a random value from the valid values.
        """
        return random.choice(self._valid_values)

    def size_iterator(self):
        for i in range(self._board_size):
            yield(i)

    def sub_board_iterator(self):
        """ Returns an iterator that goes over all sub-boards.

        Again, column by column.
        """
        for i in range(self._sub_board_size):
            for j in range(self._sub_board_size):
                yield [i, j]

    def line(self, i):
        """ Returns the values for the given line
        """
        for val in self._board[i]:
            yield val

    def column(self, j):
        """ Returns the values for the given column
        """
        for i in range(self._board_size):
            yield self._board[i][j]

    def sub_board(self, i_sub_board, j_sub_board):
        """ Returns the values for the given sub-board.

        Bear in mind that the sub-boards are the 9 3x3 grids that a typical Sudoku board contains.
        Therefore, i_sub_board and j_sub_board should be in [0, 1, 2].

        Also a generator. Neat.
        """
        i_corner = i_sub_board * 3
        j_corner = j_sub_board * 3
        for i in range(i_corner, i_corner + 3):
            for j in range(j_corner, j_corner + 3):
                yield self.value(i, j)

    def random_init(self):
        """ Initialises the board with random values.

        Not guaranteed to be a valid solution.
        """
        # TODO: actually make it a valid solution?
        for val, (i, j) in enumerate(self.board_iterator()):
            self.value(i, j, random.randint(1, 9))

    def value(self, i, j, value=None):
        """ Accesses or sets a value.

        If value is not None, then it is set at the given coordinates.
        Always returns a copy of the referenced value. If the value is changed, returns a copy of the new value.

        None means that the referenced cell is empty.
        """
        if value != None :
            self._board[i][j] = value

        return copy.copy(self._board[i][j])

    def increment(self, i, j):
        """ Increments the given cell.

        Will not do anything if the cell is empty. Does not check whether the new value is valid.
        """
        if self._board[i][j] != None:
            self._board[i][j] = self._board[i][j] + 1

    def erase(self, i, j):
        """ Erases a certain value
        """
        self._board[i][j] = None

    def is_solved(self):
        """ Returns whether the current board is solved.

        A solved board is both complete (is all filled in) and valid (not invalid).
        """
        return self.is_complete() and self.is_valid()

    def is_complete(self):
        """ Returns whether the current board is complete
        """
        for i, j in self.board_iterator():
            if self.value(i, j) == None:
                return False

        return True

    def is_valid(self):
        """ Returns whether the current board is valid.
        """
        for i, j in self.board_iterator():
            val = self.value(i, j)

            if val == None:
                continue

            if not val in self._valid_values:
                return False

            if list(self.line(i)).count(val) > 1:
                return False

            if list(self.column(j)).count(val) > 1:
                return False

            for i_sub_board, j_sub_board in self.sub_board_iterator():
                if list(self.sub_board(i_sub_board, j_sub_board)).count(val) > 1:
                    return False

        return True

    def printable(self):
        """ Generates a neat string that represents the board
        """
        output = ""
        for i in self.size_iterator():
            printable_values = [val if val != None else " " for val in self._board[i]]
            output += "{} {} {} | {} {} {} | {} {} {}".format(*(printable_values))
            output += "\n"

            if i in [2, 5]:
                output += "---------------------"
                output += "\n"

        return output