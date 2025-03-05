from collections.abc import Iterable 

from solver import CPSolver
from constraint import Constraint
from utils import Procedure
from domain import IntDomain
from domain import SparseSetDomain
from state_stack import StateStack
from state import StateManager


class IntVar:
    
    def __init__(self, cp: CPSolver, values: Iterable[int]):
        self.cp: CPSolver = cp
        self.domain: IntDomain = SparseSetDomain(values)
        
        sm: StateManager = cp.get_state_manager()
        self.on_domain: StateStack[Constraint] = StateStack(sm)
        self.on_fix: StateStack[Constraint] = StateStack(sm)
        self.on_bound: StateStack[Constraint] = StateStack(sm)

    def on_fixed(self, f: Procedure) -> None: ...

    def on_bound_change(self, f: Procedure) -> None: ...

    def on_domain_change(self, f: Procedure) -> None: ...

    def propagate_on_domain_change(self, c: Constraint) -> None: ...

    def propagate_on_fix(self, c: Constraint) -> None: ...

    def propagate_on_bound_change(self, c: Constraint) -> None: ...

    def min(self) -> int: ...

    def max(self) -> int: ...

    def size(self) -> int: ...

    def is_fixed(self) -> bool: ...

    def contains(self, v: int) -> bool: ...

    def remove(self, v: int) -> None: ...

    def fix(self, v: int) -> None: ...

    def remove_below(self, v: int) -> None: ...

    def remove_above(self, v: int) -> None: ...


class BoolVar(IntVar):

    def is_true(self) -> bool: ...

    def is_false(self) -> bool: ...

    def fix(b: bool) -> None: ...
