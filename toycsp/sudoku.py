from toycsp import ToyCSP, Variable, NotEqual
from itertools import product

def all_different(csp: ToyCSP, vars: list[Variable]) -> None:
    n = len(vars)
    for i in range(n):
        for j in range(i + 1, n):
            csp.post(NotEqual(vars[i], vars[j]))

csp: ToyCSP = ToyCSP()


############### Parameters #######################################
grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]


############### Decision variables ###############################
X: list[list[Variable | None]] = [[None] * 9 for _ in range(9)]
for i in range(9):
    for j in range(9):
        Vij = grid[i][j]
        domain = [Vij] if Vij != 0 else range(1, 10)
        X[i][j] = csp.add_variable(domain)
        
############### Constraints ######################################
# Row constraints
for i in range(9):
    all_different(csp, [X[i][j] for j in range(9)])
    
# Column constraints
for j in range(9):
    all_different(csp, [X[i][j] for i in range(9)])
    
# squares
for r1, r2 in product([range(0, 3), range(3, 6), range(6, 9)], repeat=2):
    all_different(csp, [X[i][j] for i in r1 for j in r2])

'''
This is equivalent to the following constraints
-----------------------------------------------
all_different(csp, [X[i][j] for i in range(0, 3) for j in range(0, 3)])
all_different(csp, [X[i][j] for i in range(3, 6) for j in range(0, 3)])
all_different(csp, [X[i][j] for i in range(6, 9) for j in range(0, 3)])

all_different(csp, [X[i][j] for i in range(0, 3) for j in range(3, 6)])
all_different(csp, [X[i][j] for i in range(3, 6) for j in range(3, 6)])
all_different(csp, [X[i][j] for i in range(6, 9) for j in range(3, 6)])

all_different(csp, [X[i][j] for i in range(0, 3) for j in range(6, 9)])
all_different(csp, [X[i][j] for i in range(3, 6) for j in range(6, 9)])
all_different(csp, [X[i][j] for i in range(6, 9) for j in range(6, 9)])
'''

def show_solution():
    for i in range(9):
        print(" ".join(str(X[i][j].value()) for j in range(9)))
        
@csp.on('solution')
def handle_solution(csp, infos):
    show_solution()

csp.dfs()
