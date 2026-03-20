from collections.abc import Iterable
from typing import cast

type PartialSolution = list[int | None]
type Solution = list[int]

def mid_first(values: list[int]) -> list[int]:
    '''
    Return the values in a "mid-first" order.
    >>> mid_first([0, 1, 2, 3])
    [2, 1, 3, 0]
    >>> mid_first([0, 1, 2, 3, 4])
    [2, 3, 1, 4, 0]
    >>> mid_first([0, 1, 2, 3, 4, 5])
    [3, 2, 4, 1, 5, 0]
    '''
    n = len(values)
    mid = n // 2
    result = []
    for i in range(n):
        if n % 2 == 1:
            if i % 2 == 0:
                result.append(values[mid - i // 2])
            else:
                result.append(values[mid + (i + 1) // 2])
        else:
            if i % 2 == 0:
                result.append(values[mid + i // 2])
            else:
                result.append(values[mid - (i + 2) // 2])
    return result
    
    
def nqueens_solver(n: int) -> None:

    def on_solution(queens: Solution) -> None:
        solutions.append(queens)
        
    def check_constraints(q: PartialSolution, i: int) -> bool:
        n = len(q)

        for j in range(0, i):
            if cast(int, q[i]) == cast(int, q[j]): return False
            if cast(int, q[i]) - cast(int, q[j]) == i - j: return False
            if cast(int, q[j]) - cast(int, q[i]) == i - j: return False

        return True


    def dfs(queens: PartialSolution, index: int = 0) -> None:
        n = len(queens)
        if index == n:
                # Attention à faire une copie de la liste `queens`
                on_solution(cast(Solution, queens[:]))
        else:
            for i in mid_first(list(range(n))):
                queens[index] = i
                if check_constraints(queens, i=index):
                    dfs(queens, index=index + 1)
                queens[index] = None

    solutions = []

    # Préparation du tableau utilisé pour représenter la solution
    queens: PartialSolution = [None] * n

    # Générer tous les placements de dames imaginables
    # => feuilles de l'arbre de recherche
    dfs(queens)


if __name__ == '__main__':
    # solutions = nqueens_solver(n=4)
    solutions = nqueens_solver(n=4)
    print(solutions)

    # Dessiner une solution particulière
    # draw_chess_board([0, 3, 3, None], x=0, y=0, size=20, color="red")

    import doctest
    doctest.testmod()
