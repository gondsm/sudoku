from game_board import GameBoard

def backtrack(board=GameBoard(), max_iterations=100000):
    """ Use the backtrack method to solve a board.

    The backtrack method is usually described/implemented as a recursive call, but I'm allergic to recursive programs.

    Reference: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
    """
    cells = list(board.board_iterator())

    # State
    current_cell_idx = 0
    iterations = 0

    while not board.is_solved() and iterations < max_iterations:
        # Increment state
        iterations += 1
        i, j = cells[current_cell_idx]
        val = board.value(i, j)

        # Report progress
        if iterations % 100 == 0:
            print(f"Solving. {(iterations/max_iterations)*100:.2f}% of max_iterations.", end="\r")

        # If the cell is empty, we set it to 1 and move on
        if val == None:
            board.value(i, j, 1)
            continue

        # If the cell or board is not a valid value anymore, we erase it and move back
        if val not in board._valid_values:
            # Clear cell
            board.erase(i, j)

            # Backtrack and increment
            current_cell_idx -= 1
            i, j = cells[current_cell_idx]
            board.increment(i, j)
            continue

        # If the current value is a valid number, we increment it
        if not board.is_valid():
            board.value(i, j, val+1)
            continue

        # And if the board remains valid, we move on
        current_cell_idx += 1

    print(f"Solved in {iterations} iterations. Max iterations reached?", iterations == max_iterations)

    return board