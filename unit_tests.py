import copy

# Local stuff:
from game_board import GameBoard
import solvers

# TODO: re-write using unittest

def test():
    """ A few test cases to make sure things are working
    """
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

    print("Unit tests:")

    # Sneak initialise with a valid board
    board = GameBoard()
    board._board = copy.deepcopy(valid_board)
    print("Solved board working:")
    print(board.is_solved() == True)

    # Repeated value
    board.value(0, 0, 2)
    print("Repeated value working:")
    print(board.is_valid() == False)

    # Out-of-range value
    board._board = copy.deepcopy(valid_board)
    board.value(1, 1, 10)
    print("Out-of-range value working:")
    print(board.is_valid() == False)

    # Incomplete board
    board._board = copy.deepcopy(valid_board)
    board.erase(0, 0)
    print("Incomplete board working:")
    print(board.is_complete() == False)

    # Generate a random board and print it
    print()
    print("Random board:")
    board.random_init()
    print(board.printable())

    print("Is this random board solved?")
    print(board.is_solved())

    print("Is this random board valid?")
    print(board.is_valid())

    print("Is this random board complete?")
    print(board.is_complete())

    # Modify the random board and print it
    print()
    board.erase(0, 0)
    board.erase(0, 3)
    board.erase(4, 2)
    board.erase(8, 6)
    print("Modified random board:")
    print(board.printable())

    print("Is this random board solved?")
    print(board.is_solved())

    print("Is this random board valid?")
    print(board.is_valid())

    print("Is this random board complete?")
    print(board.is_complete())

    # Random board iterator:
    print()
    elements = list(board.random_board_iterator())
    print("Here's a random set of coordinates to access the board:")
    print(elements)

    print("Is this list duplicate-free?")
    print(len(elements) == len(set((tuple(elem) for elem in elements))))

    print("Does this list contain the expected number of elements (9x9 = 81)?")
    print(len(elements) == 81)

    # Test generating a board by solving an empty board
    print("Generating a board...")
    generated_board = solvers.backtrack()
    print("Here's a generated board:")
    print(generated_board.printable())

    print("Is this board solved? It should be.")
    print(generated_board.is_solved())
    
    # Solving a partial board
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

    # Sneak in the board and solve it
    board._board = copy.deepcopy(partial_board)

    print("Here's an incomplete board:")
    print(board.printable())

    solved_board = solvers.backtrack(board)
    
    print("Here's the solved board:")
    print(solved_board.printable())

    print("Is this board solved? It should be.")
    print(solved_board.is_solved())

if __name__ == "__main__":
    test()
