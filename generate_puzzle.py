from random import seed
from game_board import GameBoard
import solvers

def generate_puzzle(seed_size=10, max_solver_iterations=5000, max_attempts=100):
    """ Generate a puzzle by randomly creating boards and checking whether they're solvable.

    For now, the scripts brute-forces its way into a valid puzzle, so who knows how long it might take.
    """
    attempts = 0

    while attempts < max_attempts:
        board = GameBoard()
        board.random_init(seed_size)

        solved_board = solvers.backtrack(board, max_solver_iterations)

        if solved_board.is_solved():
            print("Here's your puzzle:")
            print(board.printable())
            print()
            print("And here's the solution:")
            print(solved_board.printable())
            return

        max_attempts += 1

    print(f"Could not generate puzzle within {attempts} attempts!")


if __name__ == "__main__":
    generate_puzzle()