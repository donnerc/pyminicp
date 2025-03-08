from collections.abc import Iterable

from util_types import Procedure
from cp_types import IntDomain, DomainListener, CPSolver, IntVar, BoolVar, Constraint
from state_types import StateManager

from domain import SparseSetDomain
from state_stack import StateStack
from state import CopyStateManager

from solver import TuringCP
from utils import InconsistencyException
from constraint import FuncConstraint


class IntVarImpl(IntVar):
    """
    >>> sm = CopyStateManager()
    >>> cp = TuringCP(sm)
    >>> x = IntVarImpl(cp, {2, 3, 4, 6, 8})
    >>> x
    IntVar(domain=SparseSetDomain([2, 3, 4, 6, 8]), name='Var_0')
    >>> len(x)
    5
    >>> 3 in x
    True
    >>> 18 in x
    False
    >>> sm.save_state()
    >>> x.remove(3)
    >>> x
    IntVar(domain=SparseSetDomain([2, 4, 6, 8]), name='Var_0')
    >>> x.remove(3)
    >>> x.fix(4)
    >>> x
    IntVar(domain=SparseSetDomain([4]), name='Var_0')
    >>> sm.restore_state()
    >>> x
    IntVar(domain=SparseSetDomain([2, 3, 4, 6, 8]), name='Var_0')
    >>> x.remove_below(1)
    >>> x
    IntVar(domain=SparseSetDomain([2, 3, 4, 6, 8]), name='Var_0')
    >>> x.remove_below(6)
    >>> x
    IntVar(domain=SparseSetDomain([6, 8]), name='Var_0')
    >>> x.remove_below(10)
    Traceback (most recent call last):
      ...
    utils.InconsistencyException
    >>> x
    IntVar(domain=SparseSetDomain([]), name='Var_0')
    """

    var_counter: int = 0

    def __init__(
        self, solver: CPSolver, values: Iterable[int], name: str | None = None
    ) -> None:
        sm: StateManager = solver.get_state_manager()

        self.solver: CPSolver = solver
        self.domain: IntDomain = SparseSetDomain(sm, values)
        self.name = name or f"Var_{IntVarImpl.var_counter}"
        
        # add the variable to the solver variable stack
        self.solver.add_variable(self)

        IntVarImpl.var_counter += 1

        # the variable maintains stacks of constraints that have
        # to be propagated when different type of changes happen
        # on the domain
        self._on_domain: StateStack[Constraint] = StateStack(sm)
        self._on_fix: StateStack[Constraint] = StateStack(sm)
        self._on_bound: StateStack[Constraint] = StateStack(sm)

        self._domain_listener: DomainListener = DomainListener(
            empty=self.handle_empty,
            change=self.handle_change,
            change_max=self.handle_change_max,
            change_min=self.handle_change_min,
            fix=self.handle_fix,
        )

    def get_solver(self) -> CPSolver:
        return self.solver

    def handle_empty(self):
        raise InconsistencyException

    def handle_change(self):
        self._schedule_all(self._on_domain)

    def handle_change_min(self):
        self._schedule_all(self._on_bound)

    def handle_change_max(self):
        self._schedule_all(self._on_bound)

    def handle_fix(self):
        self._schedule_all(self._on_fix)

    def _schedule_all(self, constraints: StateStack[Constraint]) -> None:
        for c in constraints:
            self.solver.schedule(c)

    def when_fixed(self, f: Procedure) -> None:
        self._on_fix.push(self._func_constraint(f))

    def when_bound_change(self, f: Procedure) -> None:
        self._on_bound.push(self._func_constraint(f))

    def when_domain_change(self, f: Procedure) -> None:
        self._on_domain.push(self._func_constraint(f))

    def _func_constraint(self, f: Procedure) -> Constraint:
        c: Constraint = FuncConstraint(self.solver, f)
        self.solver.post(c)
        return c

    def propagate_on_domain_change(self, c: Constraint) -> None:
        self._on_domain.push(c)

    def propagate_on_fix(self, c: Constraint) -> None:
        self._on_fix.push(c)

    def propagate_on_bound_change(self, c: Constraint) -> None:
        self._on_bound.push(c)

    def min(self) -> int:
        return self.domain.min()

    def max(self) -> int:
        return self.domain.max()

    def __len__(self) -> int:
        return len(self.domain)

    def is_fixed(self) -> bool:
        return self.domain.is_fixed()

    def remove(self, v: int) -> None:
        self.domain.remove(v, self._domain_listener)

    def fix(self, v: int) -> None:
        self.domain.remove_all_but(v, self._domain_listener)

    def remove_below(self, v: int) -> None:
        self.domain.remove_below(v, self._domain_listener)

    def remove_above(self, v: int) -> None:
        self.domain.remove_above(v, self._domain_listener)
        
    def fill_list(self, dest: list[int]) -> int:
        for i in range(len(self.domain)):
            dest[i] = self.domain[i]
        return len(self.domain)
    
    def __contains__(self, v: int) -> bool:
        return v in self.domain

    def __repr__(self) -> str:
        return f"IntVar(domain={repr(self.domain)}, name='{self.name}')"


class BoolVarImpl(BoolVar):
    """
    TODO: implement the remaining methods + add docstring
    """

    def __init__(
        self,
        solver: CPSolver | None = None,
        var: IntVar | None = None,
        name: str | None = None,
    ) -> None:
        if solver is None and var is None:
            raise TypeError("Bool var must be instantiated with solver=... or var=...")
        if (solver and var) is not None:
            raise TypeError(
                "Bool var must be instantiated either with solver=... or var=... but not both"
            )

        if var is not None:
            if var.max() > 1 or var.min < 0:
                raise ValueError("Int var must have {0, 1} domain")
            self._bin_var: IntVar = var
        else:
            self._bin_var: IntVar = IntVarImpl(solver, {0, 1})

    def is_true(self) -> bool:
        return self._bin_var.min() == 1

    def is_false(self) -> bool:
        return self._bin_var.max() == 0

    def fix(self, b: bool) -> None:
        self._bin_var.fix(1 if b else 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
