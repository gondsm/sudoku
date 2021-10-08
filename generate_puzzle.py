import copy
import argparse

from game_board import GameBoard
import solvers

def generate_puzzle(seed_size, max_solver_iterations, max_attempts, final_size):
    """ Generate a puzzle by randomly creating boards and checking whether they're solvable.

    For now, the scripts brute-forces its way into a valid puzzle, so who knows how long it might take.
    """
    attempts = 0

    seed_board = None
    solved_board = None
    puzzle_board = None

    # Look for a valid board from a random seed
    while attempts < max_attempts:
        seed_board = GameBoard()
        seed_board.random_init(seed_size)

        solved_board = solvers.solve(seed_board, max_solver_iterations)

        if solved_board.is_solved():
            break

        max_attempts += 1

    # Whittle down the puzzle board from the solution
    if seed_board != None and solved_board != None:
        puzzle_board = copy.deepcopy(solved_board)

        while puzzle_board.occupancy() > final_size:
            puzzle_board.erase_random()

    return [seed_board, puzzle_board, solved_board]


def parse_args():
    parser = argparse.ArgumentParser(description='Generate a Sudoku puzzle.')
    parser.add_argument("--seed_size", type=int, default=10,
                        help="number of random values to seed into the board")
    parser.add_argument("--max_solver_iterations", type=int, default=10000,
                        help="maximum number of iterations we'll allow the underlying solver")
    parser.add_argument("--max_attempts", type= int, default=100,
                        help="maximmum number of seed->solve loops we'll run until we find a viable puzzle")
    parser.add_argument("--final_size", type=float, default=0.6,
                        help="fraction of the board we want filled in at the end")

    return parser.parse_args()


def print_results(seed_board, puzzle_board, solved_board):
    if puzzle_board != None:
        print("Seed board:")
        print(seed_board)

        print("Puzzle board:")
        print(puzzle_board)

        print("Solution board:")
        print(solved_board)
    else:
        print(f"Could not generate puzzle!")


if __name__ == "__main__":
    args = parse_args()
    boards = generate_puzzle(args.seed_size, args.max_solver_iterations, args.max_attempts, args.final_size)
    print_results(*boards)