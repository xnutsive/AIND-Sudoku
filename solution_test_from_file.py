# This script was originaly authored by Peter Norvig.
# I'm using it here to load sudokus from file, track my solution's performance
# and experiment with different techniques
#
# Also updated the script to run on Python 3
#

import time, random, solution


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        values = solution.solve(grid)
        t = time.clock() - start

        # Display puzzles that take long enough
        if showif is not None and t > showif:
            solution.display(solution.grid_values(grid))
            if values: solution.display(values)
            print('(%.2f seconds)\n' % t)

        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])

    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."

    def unitsolved(unit): return set(values[s] for s in unit) == set(solution.digits)

    return values is not False and all(unitsolved(unit) for unit in solution.unitlist)


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    grids = [grid.replace('\n', '') for grid in open(filename, 'r').read().strip().split(sep)]

    for grid in grids:
        assert(len(grid) == 81)

    return grids


# TODO
# This doesn't work as planned. Assign in Peter's code did elimination automatically, which is not the
# case with this solution, so I'll need to look into it later.
#
# def random_puzzle(N=17):
#     """Make a random puzzle with N or more assignments. Restart on contradictions.
#     Note the resulting puzzle is not guaranteed to be solvable, but empirically
#     about 99.8% of them are solvable. Some have multiple solutions."""
#     values = dict((box, solution.digits) for box in solution.boxes)
#     for b in shuffled(solution.boxes):
#         if not solution.assign_value(values, b, random.choice(values[b])):
#             break
#         ds = [values[b] for b in solution.boxes if len(values[b]) == 1]
#         if len(ds) >= N and len(set(ds)) >= 8:
#             return ''.join(values[b] if len(values[b])==1 else '.' for b in solution.boxes)
#     return random_puzzle(N) ## Give up and make a new puzzle
#
# def shuffled(seq):
#     "Return a randomly shuffled copy of the input sequence."
#     seq = list(seq)
#     random.shuffle(seq)
#     return seq

if __name__ == '__main__':
    solve_all(from_file("easy50.txt", '========'), "easy", None)
    solve_all(from_file("top95.txt"), "hard", None)
    solve_all(from_file("hardest.txt"), "hardest", None)
    # solve_all([random_puzzle() for _ in range(99)], "random", 100.0)