from collections.abc import Iterable

from solver import TuringCP
from state import CopyStateManager
from variable import IntVarImpl

from state_types import StateManager
from cp_types import CPSolver, IntVar, Constraint

sm: StateManager = CopyStateManager()
solver: CPSolver = TuringCP(sm)

def int_var(values: Iterable[int]) -> IntVar:
    return IntVarImpl(solver, values)

def post(c: Constraint) -> None:
    solver.post(c)