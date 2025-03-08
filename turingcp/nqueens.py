from modeling import *

from search import DFSearch
from constraint import NotEqual, Equal

NQueensSolution = list[int]


def nqueens(n: int = 8) -> list[NQueensSolution]:
    solutions: NQueensSolution = []

    # variables
    q = [int_var(range(0, n)) for _ in range(n)]

    # constraints
    for i in range(0, n):
        for j in range(i + 1, n):
            post(NotEqual(q[i], q[j], 0))
            post(NotEqual(q[i], q[j], i - j))
            post(NotEqual(q[i], q[j], j - i))

    # solving
    dfs: DFSearch = make_search()

    @dfs.on("solution")
    def handle_solution(dfs, infos):
        solutions.append(get_values(q))

    '''
    @dfs.branching_strategy
    def branching():
        def left():
            post(Equal(var, int_const(v)))

        def right():
            post(NotEqual(var, int_const(v)))

        # next variable choice
        for var in q:
            if not var.is_fixed():
                break
        else:
            return []

        # next value choice
        v: int = var.min()

        return [left, right]
    '''

    dfs.solve()

    return solutions


# profiling : https://realpython.com/python-profiling/
from cProfile import Profile
from pstats import SortKey, Stats

import sys

try:
    n = int(sys.argv[1])
except:
    n = 4

with Profile() as profile:
    print(f"{nqueens(n) = }\n\nfor {n = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CUMULATIVE)
        .print_stats()
    )
