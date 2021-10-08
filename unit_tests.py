import copy
import unittest

# Local stuff:
from game_board import GameBoard
import solvers

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
partial_board_1 = [
    [5, None,    4,    6,    7,    8,    9,    1,    2],
    [6,    7, None,    1,    9,    5, None,    4,    8],
    [1,    9,    8,    3,    4,    2,    5,    6, None],
    [8, None,    9,    7, None,    1,    4,    2,    3],
    [4,    2,    6,    8,    5,    3,    7,    9,    1],
    [7,    1,    3,    9,    2,    4,    8, None,    6],
    [9,    6,    1, None,    3,    7,    2,    8,    4],
    [2,    8,    7,    4,    1,    9,    6,    3,    5],
    [3,    4,    5,    2,    8,    6,    1,    7,    9],
]

# The same board with a few more elements removed.
partial_board_2 = [
    [5, None,    4,    6,    7,    8,    9,    1,    2],
    [6,    7, None,    1,    9,    5, None,    4,    8],
    [1,    9,    8,    3,    4, None,    5,    6, None],
    [8, None,    9,    7, None,    1,    4,    2,    3],
    [4,    2,    6,    8,    5,    3,    7,    9,    1],
    [7,    1,    3,    9,    2,    4,    8, None,    6],
    [None, 6,    1, None,    3,    7,    2,    8,    4],
    [None, None, 7,    4,    1,    9,    6,    3,    5],
    [None, None, 5,    2,    8,    6,    1,    7,    9],
]

# A harder problem
partial_board_3 = [
    [5, None,    4,    6,    7,    8,    9,    1,    2],
    [6,    7, None,    1,    9,    5, None,    4,    8],
    [1,    9,    8,    3,    4, None,    5,    6, None],
    [8, None,    9,    7, None,    1,    4,    2,    3],
    [4,    2,    6,    8,    5,    3,    7,    9,    1],
    [7,    1,    3, None,    2, None,    8, None,    6],
    [None, 6,    1, None,    3,    7,    2,    8,    4],
    [None, None, 7,    4,    1, None,    6,    3,    5],
    [None, None, 5,    2,    8,    6, None,    7,    9],
]

class TestGameBoard(unittest.TestCase):
    def test_valid_board(self):
        """ A simple, complete and valid board should be considered solved.
        """
        board = GameBoard()
        board.initialise_board(valid_board)

        self.assertTrue(board.is_solved())

    def test_repeated_value(self):
        """ A board with a repeated value should not be valid.
        """
        board = GameBoard()
        board.initialise_board(valid_board)
        board.value(0, 0, 2)

        self.assertFalse(board.is_valid())

    def test_out_of_range(self):
        """ A board with an out-of-range value should not be valid.
        """
        board = GameBoard()
        board.initialise_board(valid_board)
        board.value(1, 1, 10)

        self.assertFalse(board.is_valid())

    def test_incomplete(self):
        """ A board that is missing an element should not be considered complete.
        """
        board = GameBoard()
        board.initialise_board(valid_board)
        board.erase(0, 0)

        self.assertFalse(board.is_complete())

    def test_empty_board(self):
        """ An empty board cannot be completed or solved.
        """
        board = GameBoard()

        self.assertFalse(board.is_solved())
        self.assertTrue(board.is_valid())
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

    def test_random_partial_board(self):
        """ We can specify not wanting to initialise the whole board.
        """
        board = GameBoard()
        board.random_init(50)

        self.assertFalse(board.is_solved())
        self.assertFalse(board.is_valid())
        self.assertFalse(board.is_complete())

    def test_random_board_iterator(self):
        """ Test generating a random board iterator.
        """
        board = GameBoard()
        elements = list(board.random_board_iterator())

        self.assertTrue(len(elements) == len(set((tuple(elem) for elem in elements))))
        self.assertTrue(len(elements) == 81)

    def test_occupancy(self):
        """ The occupancy function returns how much of the grid is occupied.
        """
        board = GameBoard()

        self.assertEqual(board.occupancy(), 0)

        board = GameBoard()
        board.random_init(9)
        self.assertAlmostEqual(board.occupancy(), 0.1, 1)

        board = GameBoard()
        board.random_init(18)
        self.assertAlmostEqual(board.occupancy(), 0.2, 1)

    def test_erase_random(self):
        """ Random erasure function should do what we want it to.

        E.g. if we add only one element, it should remove it.
        """
        board = GameBoard()

        board.random_init(1)
        self.assertGreater(board.occupancy(), 0)

        board.erase_random()
        self.assertEqual(board.occupancy(), 0)

        board = GameBoard()
        board.random_init(5)

        for _ in range(5):
            board.erase_random()

        self.assertEqual(board.occupancy(), 0)

    def test_fixed_positions(self):
        """ Elements added as fixed should be reported as such.
        """
        board = GameBoard()
        board.random_init(1, True)

        count = 0
        for i, j in board.board_iterator():
            if board.value(i, j) != None:
                count += 1
                self.assertTrue(board.is_fixed(i, j))

        self.assertEqual(count, 1)

    def test_non_fixed_positions(self):
        """ Elements added as non-fixed should be reported as such.
        """
        board = GameBoard()
        board.random_init(1, False)

        count = 0
        for i, j in board.board_iterator():
            if board.value(i, j) != None:
                count += 1
                self.assertFalse(board.is_fixed(i, j))

        self.assertEqual(count, 1)

    def test_sub_board_coordinates(self):
        board = GameBoard()

        coordinates = [
            (0, 0),
            (3, 3),
            (5, 6)
        ]
        sub_board_indices = [
            (0, 0),
            (1, 1),
            (1, 2)
        ]

        for elem, expected in zip(coordinates, sub_board_indices):
            self.assertEqual(board.sub_board_from_indices(*elem), expected)


class TestBacktrackSolver(unittest.TestCase):
    def test_generate_from_empty(self):
        """ If we solve an empty board, it should generate a solved board.
        """
        generated_board = solvers._backtrack(GameBoard(), 1000000)
        self.assertTrue(generated_board.is_solved())

    def test_solve_from_partial(self):
        """ If we solve a partial board, it should generated a solved board.

        The solved board should be equal to the valid board, since I didn't remove enough elements to generate a
        multi-solution problem.

        The original board should remain unchanged, which is useful e.g. for benchmarking solvers.
        """
        board = GameBoard()
        board.initialise_board(partial_board_1)
        solved_board = solvers._backtrack(board, 1000)

        self.assertTrue(solved_board.is_solved())
        self.assertEqual(board._board, partial_board_1)
        self.assertEqual(solved_board._board, valid_board)


class TestDeductiveSolver(unittest.TestCase):
    def test_solve_from_partial(self):
        """ If we solve a partial board, it should generated a solved board.
        """
        board = GameBoard()
        board.initialise_board(partial_board_1)
        solved_board = solvers._deductive(board, 1000)

        self.assertTrue(solved_board.is_solved())
        self.assertEqual(board._board, partial_board_1)
        self.assertEqual(solved_board._board, valid_board)

    def test_solve_from_partial(self):
        """ Should be able to solve a slightly harder problem.
        """
        board = GameBoard()
        board.initialise_board(partial_board_2)
        solved_board = solvers._deductive(board, 1000)

        self.assertTrue(solved_board.is_solved())
        self.assertEqual(board._board, partial_board_2)
        self.assertEqual(solved_board._board, valid_board)


class TestCombinedSolvers(unittest.TestCase):
    def test_solve_from_partial(self):
        """ The deductive solver might not be able to tackle a certain harder problem

        ... but a combination of deductive and backtrack should.
        """
        board = GameBoard()
        board.initialise_board(partial_board_3)
        intermediate_board = solvers._deductive(board, 1000)

        self.assertFalse(intermediate_board.is_solved())

        solved_board = solvers._backtrack(intermediate_board, 10000)
        self.assertTrue(solved_board.is_solved())

    def test_top_level_solve(self):
        """ The top-level solve function should be able to solve any valid problem.
        """
        board = GameBoard()
        board.initialise_board(partial_board_3)
        solved_board = solvers.solve(board, 10000)
        self.assertTrue(solved_board.is_solved())


if __name__ == "__main__":
    unittest.main()
