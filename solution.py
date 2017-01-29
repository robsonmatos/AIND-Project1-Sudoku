assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    """Cross product of elements in A and elements in B.

    Args:
        A(string): An string indicating ideally row names.
        B(string): An string indicating ideally column names.

    Returns:
        Cross combination between every element of A and B.
    """
    return [a + b for a in A for b in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [[row + col for row, col in zip(rows, cols)], [row + col for row, col in zip(rows[::-1], cols)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """Please use this function to update your values dictionary!

    Assigns a value to a given box. If it updates the board record it.

    Args:
        values(dict): A Sudoku in dictionary form.
        box(string): An string containing the box which will be updated.
        value(string): A string containing the value that should be savec.

    Returns:
        The updated Sudoku in dictionary form.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminates values using the naked twins strategy.

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """
    two_element_boxes = [box for box in boxes if len(values[box]) == 2]
    # Find all instances of naked twins
    elimin_candidates = [(values[box], [u for u in unit if u != box and u != peer]) for box in two_element_boxes
                         for unit in units[box] for peer in unit
                         if values[box] == values[peer] and box != peer]

    # Eliminate possible candidates
    [assign_value(values, box, values[box].replace(digit, '')) for digits, candidates in elimin_candidates
     for box in candidates for digit in digits]

    return values


def grid_values(grid):
    """Converts grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid(string): A grid in string form.

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_vals = {}

    for box, value in zip(boxes, grid):
        if value == '.':
            grid_vals[box] = '123456789'
        else:
            grid_vals[box] = value

    return grid_vals


def display(values):
    """Displays the values as a 2-D grid.

    Args:
        values(dict): A Sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()


def eliminate(values):
    """Eliminates values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values(dict): A Sudoku in dictionary form.

    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, value in values.items():
        if len(value) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(value, ''))

    return values


def only_choice(values):
    """Finalizes all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        values(dict): A Sudoku in dictionary form.

    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()  # note: do not modify original values
    for unit in unitlist:
        for digit in cols:
            dboxes = [box for box in unit if digit in values[box]]
            if len(dboxes) == 1:
                assign_value(new_values, dboxes[0], digit)

    return new_values


def reduce_puzzle(values):
    """Iterates eliminate() and only_choice().

    Args:
        values(dict): A Sudoku in dictionary form.

    Returns:
        If the Sudoku is solved, return the Sudoku.
        If after an iteration of both functions, the Sudoku remains the same, return the Sudoku.
        If at some point, there is a box with no available values, return False.
    """
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use naked twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Creates a search tree using depth-first search and constraint propagation, and solve the Sudoku.

    Use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return the
    answer

    Args:
        values(dict): A Sudoku in dictionary form.

    Returns:
        Resulting Sudoku in dictionary form after search is successful. Otherwise, return None.
    """
    # First, reduce the puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(value) == 1 for value in values.values()):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n_min, box_key = min((len(value), box) for box, value in values.items() if len(value) > 1)
    # Iterate recursively through
    for value in values[box_key]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, box_key, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Finds the solution to a Sudoku grid.

    Args:
        grid(string): a string representing a Sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns:
        The dictionary representation of the final Sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solution = solve(diag_sudoku_grid)
    display(solution)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
