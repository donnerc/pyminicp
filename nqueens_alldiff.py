from toycsp import ToyCSP, Variable, GACAllDifferent3 as AllDifferent

def nqueens(n: int):
    # problème
    csp: ToyCSP = ToyCSP()
    # variables de décision
    q: list[Variable] = [csp.add_variable(range(n)) for _ in range(n)]

    # 1. Une dame par colonne (déjà géré par la structure du problème : queens[i] est la ligne en col i)
    # 2. Toutes les lignes doivent être différentes
    csp.post(AllDifferent(q, pigeonhole=False))

    # 3. Diagonales montantes : Xi + i doit être différent
    csp.post(AllDifferent(q, offsets=[i for i in range(n)], pigeonhole=False))

    # 4. Diagonales descendantes : Xi - i doit être différent
    csp.post(AllDifferent(q, offsets=[-i for i in range(n)], pigeonhole=False))
    
    @csp.on('solution')
    def handle_solution(csp, infos):
        solutions.append(csp.get_solution())
        #print(sol)

    solutions = []
    csp.dfs()
    
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
    print(f"{len(nqueens(n)) = }\n\nfor {n = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CUMULATIVE)
        .print_stats()
    )
