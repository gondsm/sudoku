import copy
import unittest

# Local stuff:
from game_board import GameBoard
import solvers

class TestStringMethods(unittest.TestCase):
    # A constant valid board. I absolutely did not copy this by hand from an example online.
    valid_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    # The same board with a few elements removed, ripe for solving.
    partial_board = [
        [5, None, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, None, 1, 9, 5, None, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, None],
        [8, None, 9, 7, None, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, None, 6],
        [9, 6, 1, None, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    def test_valid_board(self):
        """ A simple, complete and valid board should be considered solved.
        """
        board = GameBoard()
        board._board = copy.deepcopy(self.valid_board)

        self.assertTrue(board.is_solved())

    def test_repeated_value(self):
        """ A board with a repeated value should not be valid.
        """
        board = GameBoard()
        board._board = copy.deepcopy(self.valid_board)
        board.value(0, 0, 2)

        self.assertFalse(board.is_valid())

    def test_out_of_range(self):
        """ A board with an out-of-range value should not be valid.
        """
        board = GameBoard()
        board._board = copy.deepcopy(self.valid_board)
        board.value(1, 1, 10)

        self.assertFalse(board.is_valid())

    def test_incomplete(self):
        """ A board that is missing an element should not be considered complete.
        """
        board = GameBoard()
        board._board = copy.deepcopy(self.valid_board)
        board.erase(0, 0)

        self.assertFalse(board.is_complete())

    def test_random_board(self):
        """ Test generating a random board.

        A random board should (extremely likely) not be solved, should (extremely likely) not be valid, and should be
        complete.
        """
        board = GameBoard()
        board.random_init()

        self.assertFalse(board.is_solved())
        self.assertFalse(board.is_valid())
        self.assertTrue(board.is_complete())

    def test_random_board_iterator(self):
        """ Test generating a random board iterator.
        """
        board = GameBoard()
        elements = list(board.random_board_iterator())

        self.assertTrue(len(elements) == len(set((tuple(elem) for elem in elements))))
        self.assertTrue(len(elements) == 81)

    def test_generate_from_empty(self):
        """ If we solve an empty board, it should generate a solved board.
        """
        generated_board = solvers.backtrack()
        self.assertTrue(generated_board.is_solved())

    def test_solve_from_partial(self):
        """ If we solve a partial board, it should generated a solved board.

        The solved board should be equal to the valid board, since I didn't remove enough elements to generate a
        multi-solution problem.

        The original board should remain unchanged, which is useful e.g. for benchmarking solvers.
        """
        board = GameBoard()
        board._board = copy.deepcopy(self.partial_board)
        solved_board = solvers.backtrack(board)

        self.assertTrue(solved_board.is_solved)
        self.assertEqual(board._board, self.partial_board)
        self.assertEqual(solved_board._board, self.valid_board)


if __name__ == "__main__":
    unittest.main()
