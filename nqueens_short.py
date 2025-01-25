from toycsp import ToyCSP, Variable

n = int(input("Taille du problème"))

csp: ToyCSP = ToyCSP()
q: list[Variable] = [csp.make_variable(n) for _ in range(n)]

for i in range(n):
    for j in range(i + 1, n):
        csp.not_equal(q[i], q[j], 0)
        csp.not_equal(q[i], q[j], i - j)
        csp.not_equal(q[i], q[j], j - i)
        
def handle_solution(sol):
    solutions.append(sol)

solutions = []
csp.dfs(on_solution=handle_solution)

print(solutions)

