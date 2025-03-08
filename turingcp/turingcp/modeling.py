from collections.abc import Iterable

from solver import TuringCP
from state import CopyStateManager

from state_types import StateManager
from cp_types import CPSolver, IntVar, Constraint
from util_types import Supplier, Procedure

from variable import IntVarImpl
from search import DFSearch

sm: StateManager = CopyStateManager()
solver: CPSolver = TuringCP(sm)


def int_var(values: Iterable[int]) -> IntVar:
    return IntVarImpl(solver, values)


def int_const(v: int) -> IntVar:
    return IntVarImpl(solver, {v})


def post(c: Constraint) -> None:
    solver.post(c)


def make_search(branching: Supplier[list[Procedure]] | None = None) -> DFSearch:
    return DFSearch(solver, branching)


def get_values(vars: list[IntVar]) -> list[int]:
    return [v.min() for v in vars]