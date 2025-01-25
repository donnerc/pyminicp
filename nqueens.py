from toycsp import ToyCSP, Variable

def nqueens(n: int):
    # problème
    csp: ToyCSP = ToyCSP()
    # variables de décision
    q: list[Variable] = [csp.make_variable(n) for _ in range(n)]

    ## Déclaration des contraintes du problème
    for i in range(n):
        for j in range(i + 1, n):
            # Pas deux reines sur la même ligne,
            csp.not_equal(q[i], q[j], 0)
            # Pas deux reines sur une diagonale montante
            csp.not_equal(q[i], q[j], i - j)
            # Pas deux reines sur une diagonale descendante
            csp.not_equal(q[i], q[j], j - i)
            
    def handle_solution(sol):
        solutions.append(sol)
        #print(sol)

    solutions = []
    csp.dfs(on_solution=handle_solution)
    
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
