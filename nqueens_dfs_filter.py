from collections.abc import Iterable

def check_constraints(q: Iterable[int]) -> bool:
    '''
    Vérifie que toutes les contraintes du problème soient satisfaites dans la
    solution ``q`` représentant la ligne sur laquelle est placée chaque dames
    q[i]
    '''
    n = len(q)

    for i in range(n):
        for j in range(i + 1, n):
            if q[i] == q[j]: return False
            if q[i] - q[j] == i - j: return False
            if q[j] - q[i] == i - j: return False

    return True


def nqueens_solver(n: int) -> None:
    '''
    Retourne toutes les solutions pour le problème des n dames

    >>> nqueens_solver(n=1)
    [[0]]
    >>> nqueens_solver(n=2)
    []
    >>> nqueens_solver(n=3)
    []
    >>> nqueens_solver(n=4)
    [[1, 3, 0, 2], [2, 0, 3, 1]]
    >>> nqueens_solver(n=5)
    [[0, 2, 4, 1, 3], [0, 3, 1, 4, 2], [1, 3, 0, 2, 4], [1, 4, 2, 0, 3], [2, 0, 3, 1, 4], [2, 4, 1, 3, 0], [3, 0, 2, 4, 1], [3, 1, 4, 2, 0], [4, 1, 3, 0, 2], [4, 2, 0, 3, 1]]
    '''
    def on_solution(queens: list[int]) -> None:
        solutions.append(queens)
        
        
    def dfs(queens: Iterable[int], index: int = 0) -> None:
        n = len(queens)
        if index == n:
            if check_constraints(queens):
                # Attention à faire une copie de la liste `queens`
                on_solution(queens[:])
        else:
            for i in range(n):
                queens[index] = i
                dfs(queens, index=index + 1)


    # Préparation du tableau utilisé pour représenter la solution
    queens = [None] * n
    solutions = []

    # Générer tous les placements de dames imaginables
    # => feuilles de l'arbre de recherche

    dfs(queens)

    return solutions


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    solutions = nqueens_solver(n=4)
    print(solutions)