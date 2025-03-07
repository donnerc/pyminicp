from turingcp.modeling import int_var, post
from turingcp.constraint import NotEqual
from turingcp.search import dfs_branching


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
    @on_solution
    def handle_solution(solution):
        solutions.append(solution)

    @strategy
    def solve():
        for var in q:
            if not var.is_fixed():
                break
        else:
            return []

        v: int = var.min()
        left = post(Equal(var, v))
        right = post(NotEqual(var, v))
        return [left, right]

    solve()

    return solutions


if __name__ == "__main__":
    solutions = nqueens(n=8)
    print(solutions)
