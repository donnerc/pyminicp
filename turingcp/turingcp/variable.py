from collections.abc import Iterable 

from cp_types import CPSolver, IntVar, Constraint
from utils import Procedure
from domain import IntDomain, SparseSetDomain
from state_stack import StateStack
from state import StateManager


class IntVarImpl(IntVar):
    '''
    >>> v = IntVar([2, 3, 4])
    >>> v
    '''
    
    var_counter: int = 0
    
    def __init__(self, solver: CPSolver, values: Iterable[int], name: str | None = None) -> None:
        self.solver: CPSolver = solver
        self.domain: IntDomain = SparseSetDomain(values)
        self.name = name or f"Var_{IntVar.var_counter}"
        
        IntVar.var_counter += 1
        
        sm: StateManager = solver.get_state_manager()
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

    def is_fixed(self) -> bool:
        return self.domain.is_fixed()

    def contains(self, v: int) -> bool: ...

    def remove(self, v: int) -> None: ...

    def fix(self, v: int) -> None: ...

    def remove_below(self, v: int) -> None: ...

    def remove_above(self, v: int) -> None: ...
    
    def __repr__(self) -> str:
        return f"IntVar(domain={repr(self.domain)}, name='{self.name}')"


class BoolVar(IntVar):

    def is_true(self) -> bool: ...

    def is_false(self) -> bool: ...

    def fix(b: bool) -> None: ...


if __name__ == '__main__':
    import doctest
    doctest.testmod()