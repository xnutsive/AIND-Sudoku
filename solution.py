# This file provides an API to solve any sudoku (9x9 grid) using
# constrant propagation techniques and search.
#
# TODO
# 1. [ ] Add Naked Twins implementation that passes the provided `sudoku_test`.
# 2. [ ] Add a separate script loader that will solve more sudokus and track time
# 3. [ ] Add more complex sudokus to the test
# 4. [ ] Add only available box constraint to propagation
# 5. [ ] Try implementing naked_twins for 3 or more digits?
# 6. [ ] Write question answers in readme.md
# 7. [ ] Describe my testing suite and additional algs implemented
# 8. [ ] Upload for review
#

# FIXME
# How do I move those down below the variables initialization?


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]

# Log of all the assignments made
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Create two additional diagonal units. That way `eliminate()` will also do the diagonal rule automatically.
diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))], [rows[i]+cols[::-1][i] for i in range(len(rows))]]

# Add diagonal_units to the unitlist.
unitlist = row_units + column_units + square_units + diagonal_units

# Units and peers will use diagonal units automatically.
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find each pair, and then find their common units, and then update values
    twin_pairs = [[b1, b2] for b1 in boxes for b2 in peers[b1]
                   if (len(values[b1]) == 2) and (values[b1] == values[b2])]

    for twin_pair in twin_pairs:
        # Shortcuts for twin boxes for easier access
        b1 = twin_pair[0]

        for unit in [unit for unit in units[twin_pair[0]] if unit in units[twin_pair[1]]]:

            # For each box that is not in the twin pair (triple, etc) and that is unsolved,
            # delete all the digits which are in the pair (triple).
            for box in [box for box in unit if (box not in twin_pair) and len(values[box]) > 1]:
                for digit in values[b1]:
                    assign_value(values, box, values[box].replace(digit, ''))

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]) > 0:
            return False
    return values


def search(values):
    values = reduce_puzzle(values)

    if not values:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    number, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    for val in values[box]:
        option = values.copy()
        assign_value(option, box, val)
        result = search(option)
        if result:
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid in a string representation. 
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Just default to search, it'll apply constraint prop when possible.
    return search(grid_values(grid))


if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
