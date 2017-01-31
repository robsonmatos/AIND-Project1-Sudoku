assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    """Cross product of elements in A and elements in B.

    Args:
        A(string): A string indicating row names.
        B(string): A string indicating column names.

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