import copy

from game_board import GameBoard

def backtrack(input_board=GameBoard(), max_iterations=100000):
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

    # State
    cells = list(board.board_iterator())
    current_cell_idx = 0
    iterations = 0

    # Basic functions on state
    def get_current_value():
        i, j = cells[current_cell_idx]
        val = board.value(i, j)

        return val

    def report_progress():
        nonlocal iterations
        iterations += 1

        if iterations % 100 == 0:
            print(f"Solving. {(iterations/max_iterations)*100:.2f}% of max_iterations.", end="\r")

    def initialise():
        i, j = cells[current_cell_idx]
        board.value(i, j, 1)

    def increment():
        i, j = cells[current_cell_idx]
        board.increment(i, j)

    def backtrack():
        nonlocal current_cell_idx
        # Clear cell
        i, j = cells[current_cell_idx]
        board.erase(i, j)

        # Backtrack and increment
        current_cell_idx -= 1
        i, j = cells[current_cell_idx]
        board.increment(i, j)

    def advance():
        nonlocal current_cell_idx
        current_cell_idx += 1

    # The main loop is split into three essential clauses:
    # * If the value is empty, it's initialised as 1.
    # * If the value is out of bounds, we backtrack to the previous element we were looking at.
    # * If the board is not valid, we increment the current value.
    # If none of these clauses get triggered, we simply move on to the next cell.
    while not board.is_solved() and iterations < max_iterations:
        curr_value = get_current_value()
        report_progress()

        # If the cell is empty, we set it to 1 and move on
        if curr_value == None:
            initialise()
            continue

        # If the cell or board is not a valid value anymore, we erase it and move back
        if curr_value not in board._valid_values:
            backtrack()
            continue

        # If the current value is a valid number, we increment it
        if not board.is_valid():
            increment()
            continue

        # And if the board remains valid, we move on
        advance()

    print(f"Solved in {iterations} iterations. Max iterations reached?", iterations == max_iterations)

    return board