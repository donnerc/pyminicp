from collections.abc import Iterable

def nqueens_solver(n: int) -> None:

    def on_solution(queens: Iterable[int]) -> None:
        solutions.append(queens)
        
    def check_constraints(q: Iterable[int], i: int) -> bool:
        n = len(q)

        for j in range(0, i):
            if q[i] == q[j]: return False
            if q[i] - q[j] == i - j: return False
            if q[j] - q[i] == i - j: return False

        return True


    def dfs(queens: Iterable[int], index: int = 0) -> None:
        n = len(queens)
        if index == n:
                # Attention à faire une copie de la liste `queens`
                on_solution(queens[:])
        else:
            for i in range(n):
                queens[index] = i
                if check_constraints(queens, i=index):
                    dfs(queens, index=index + 1)
                queens[index] = None

    solutions = []

    # Préparation du tableau utilisé pour représenter la solution
    queens = [None] * n

    # Générer tous les placements de dames imaginables
    # => feuilles de l'arbre de recherche
    dfs(queens)
    
    return solutions


if __name__ == '__main__':
    # solutions = nqueens_solver(n=4)
    solutions = nqueens_solver(n=4)
    print(solutions)

    # Dessiner une solution particulière
    # draw_chess_board([0, 3, 3, None], x=0, y=0, size=20, color="red")

    import doctest
    doctest.testmod()
