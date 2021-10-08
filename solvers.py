import copy
from collections import defaultdict

from game_board import GameBoard

########################################################################################################################
# PUBLIC INTERFACE
########################################################################################################################
def solve(input_board, max_iterations):
    """ Entry point to the solvers. Just calling this function, by default, should yield "good" results.

    The idea is that it'll call whatever solver happens to be the best at some point, depending on what's implemented.
    """
    # Define a pipeline of solvers to use. Since the intermediate solutions of each solver should be valid, the
    # intermediate results can be fed into one another.
    solvers = [
        _deductive,
        _backtrack
    ]

    intermediate_board = input_board
    for solver in solvers:
        intermediate_board = solver(intermediate_board, max_iterations)
        if intermediate_board.is_solved():
            break

    return intermediate_board


########################################################################################################################
# INTERNALS (here be dragons)
########################################################################################################################
def report_start(solver_name, occupancy):
    print(f"[{solver_name}] starting. Starting board occupancy at {occupancy:.2f}.")

def report_progress(solver_name, iterations, max_iterations):
    if iterations % 100 == 0:
        print(f"[{solver_name}]: {(iterations/max_iterations)*100:.2f}% of max_iterations.", end="\r")


def report_result(solver_name, solved, occupancy, reached_max_iterations):
    print(f"[{solver_name}] finished. Solved? {solved}. Final occupancy: {occupancy:.2f}. Reached maximum iterations? {reached_max_iterations}")


def _backtrack(input_board, max_iterations):
    """ Use the backtrack method to solve a board.

    The backtrack method is usually described/implemented as a recursive call, but I'm allergic to recursive programs.

    Since this was always going to be a lengthy function, I decided to break up the main loop into sub-functions that
    operate on the function's shared state and describe the atomic functions of the algorithm. This allowed me to define
    the main loop in almost 1-to-1 correspondence with the algorithm. This allows me to both understand the algorithm as
    a composition of operations, and perhaps move out functionality in the future.

    I'm not sure about this structure, but I'll leave it as an example. Perhaps a class would've been a better
    representation.

    Reference: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
    """
    # Duplicate the input board so we don't change it in place:
    board = copy.deepcopy(input_board)

    # Initilise state
    report_start("Backtrack", board.occupancy())
    cells = list(board.board_iterator())
    current_cell_idx = 0
    iterations = 0

    # Basic functions on state
    def get_current_value():
        i, j = cells[current_cell_idx]
        val = board.value(i, j)

        return val

    def initialise():
        i, j = cells[current_cell_idx]
        board.value(i, j, 1)

    def increment():
        i, j = cells[current_cell_idx]
        board.increment(i, j)

    def backtrack():
        nonlocal current_cell_idx
        # Clear cell and backtrack
        i, j = cells[current_cell_idx]
        board.erase(i, j)
        current_cell_idx -= 1

        # Skip over fixed cells
        while current_cell_idx > 0 and board.is_fixed(*cells[current_cell_idx]):
            current_cell_idx -= 1

    def advance():
        nonlocal current_cell_idx
        current_cell_idx += 1

        # Skip over fixed cells
        while current_cell_idx < len(cells) and board.is_fixed(*cells[current_cell_idx]):
            current_cell_idx += 1

    # The main loop is split into three essential clauses:
    # * If the value is empty, it's initialised as 1.
    # * If the value is out of bounds, we backtrack to the previous element we were looking at.
    # * If the board is not valid, we increment the current value.
    # If none of these clauses get triggered, we simply move on to the next cell.
    while not board.is_solved() and iterations < max_iterations and current_cell_idx < 81:
        iterations += 1
        curr_value = get_current_value()
        report_progress("Backtrack", iterations, max_iterations)

        # If the cell is empty, we set it to 1 and move on
        if curr_value == None:
            initialise()
            continue

        # If the cell or board is not a valid value anymore, we erase it and move back
        if curr_value not in board._valid_values:
            backtrack()
            increment()
            continue

        # If the current value is a valid number, we increment it
        if not board.is_valid():
            increment()
            continue

        # And if the board remains valid, we move on
        advance()

    report_result("Backtrack", board.is_solved(), board.occupancy(), iterations == max_iterations)

    return board


def _deductive(input_board, max_iterations):
    """ Implements a deductive method for solving the given board.

    This is based on the common heuristic everyone uses (I assume) where we pencil in the possible values for each cell
    and then unravel the puzzle from there.
    """
    # Duplicate the input board so we don't change it in place:
    board = copy.deepcopy(input_board)
    report_start("Deductive", board.occupancy())

    # We'll keep the pencilled-in numbers here
    pencil_board = defaultdict(set)
    valid_values = board._valid_values

    # Sub-functions
    def generate_pencil_board():
        print("[Deductive] solver generating pencil board.")
        for i, j in board.board_iterator():
            # Only work on empty cells
            if board.value(i, j) == None:
                # Iterate over all valid values
                for val in valid_values:
                    # Try adding, if it works it's a possible value
                    if try_adding_value(i, j, val):
                        key = (i, j)
                        pencil_board[key].add(val)
                        board.erase(i, j)

    def try_adding_value(i, j, value):
        """ Adds a value to the board only if the resulting board is valid.

        Returns whether the value stuck.
        """
        board.value(i, j, value)
        if not board.is_valid():
            board.erase(i, j)
            return False

        return True

    # Start by pencilling in all possibilities
    generate_pencil_board()

    iterations = 0
    while iterations < max_iterations and not board.is_solved() and len(pencil_board) > 0:
        iterations += 1
        report_progress("Deductive", iterations, max_iterations)

        # Iterate over the pencilled board
        for (i, j), values in pencil_board.items():
            # If there's only one possible value for a given cell, we write it in
            if len(values) == 1:
                # TODO: why would this not be valid?
                # TODO: surely we can get stuff from the set without making it into a list
                try_adding_value(i, j, list(values)[0])
                pencil_board[(i, j)] = []
                continue

            # If the current value is the only possible position for this value in this sub-board, we write it in
            sub_board_positions = board.sub_board_positions(*board.sub_board_from_indices(i, j))
            for value in values:
                # Evaluate whether the value is the only possibility for this value in this sub-board
                only_possibility_in_sub_board = True
                for sub_i, sub_j in sub_board_positions:
                    # Only check the pencil board if the key exists, since accessing the defaultdict on a non-existing
                    # key will add it to the dict and, thus, crash us as we're changing the dict mid-iteration.
                    if (sub_i, sub_j) in pencil_board.keys():
                        only_possibility_in_sub_board = not (value in pencil_board[(sub_i, sub_j)])

                # Write the value in and break early since we won't have another value for the current cell
                if only_possibility_in_sub_board:
                    board.value(i, j, value)
                    pencil_board[(i, j)].remove(value)
                    break

    report_result("Deductive", board.is_solved(), board.occupancy(), iterations == max_iterations)

    return board