from toycsp import ToyCSP
from gturtle import *

def draw_chess_board(csp: ToyCSP, x: int = -200, y: int = -100, size: int = 50, color="black") -> tuple[int, int]:
    def square(cx, cy) -> None:
        setPos(cx - size / 2, cy - size / 2)
        for _ in range(4):
            fd(size)
            rt(90)

    def queen(cx, cy):
        setPos(cx, cy)
        dot(size * 0.7)

    def crossout(cx, cy):
        setPos(cx, cy)
        lt(45)
        setPenWidth(5)
        setPenColor("red")
        for _ in range(4):
            fd(size * 0.5)
            bk(size * 0.5)
            rt(90)
        rt(45)
        setPenWidth(1)
        setPenColor("black")

    hideTurtle()
    setPenColor(color)
    setFontSize(size * 0.95)

    solution = csp.get_solution()
    n = len(solution)

    for i in range(n):
        for j in range(n):
            cx = x + i * size - size / 2
            cy = y + j * size - size / 2
            setPenColor("black")
            square(cx, cy)
            if solution[i] == j:
                queen(cx, cy)
            elif j not in csp.variables[i].dom.values:
                crossout(cx, cy)

    setPos(x - size, y - 2 * size)
    setHeading(0)
    label("  ".join(str(q) if q is not None else '?' for q in solution))

    return n, size