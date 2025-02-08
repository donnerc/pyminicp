from toycsp import ToyCSP, Variable, NotEqual

def nqueens_solver(n: int) -> list[list[int]]:
    csp: ToyCSP = ToyCSP()
    q: list[Variable] = [csp.add_variable(range(n)) for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            csp.post(NotEqual(q[i], q[j], 0))
            csp.post(NotEqual(q[i], q[j], i - j))
            csp.post(NotEqual(q[i], q[j], j - i))

    @csp.on('solution')
    def handle_solution(csp, infos):
        solutions.append(csp.get_solution())

    solutions = []
    csp.dfs()
    
    return solutions


if __name__ == '__main__':
    solutions = nqueens_solver(n=4)
    print(f"{solutions = }")
