from cp_types import Constraint, Variable
from state_types import State
from turingcp.cp_types import CPSolver
from turingcp.cp_types import IntVar
from turingcp.util_types import Procedure


class AbstractConstraint(Constraint):
    """

    Represents an abstract constraint with some common methods from the
    Constraint ABC already implemented. Each concrete constraint has to inherit
    from this class and implement the `post` and `propagate` methods.

    """

    def __init__(self, solver: CPSolver):
        self._solver: CPSolver = solver
        self._scheduled = False
        self._active: State[bool] = self._solver.get_state_manager().make_state_obj(
            True
        )

    def get_solver(self) -> CPSolver:
        "Returns the underlying solver"
        return self._solver

    def set_scheduled(self, scheduled) -> None:
        """
        Sets the scheduled status of a constraint to avoid rescheduling
        propagation for a constraint already present in the propagation queue
        """
        self._scheduled = scheduled

    def is_scheduled(self) -> bool:
        """
        Returns `True` if the constraint is already scheduled in the propagation
        queue and `False` otherwise.
        """
        return self._scheduled

    def set_active(self, active: bool) -> None:
        """
        Sets the activation status of the constraint. An inactive constraint
        won't be scheduled into the propagation queue.
        """
        self._active.set_value(active)

    def is_active(self) -> bool:
        """
        Returns `True` if the constraint is active and `False` otherwise.
        """
        return self._active.value()

    def post(self) -> None:
        """
        Posts the constraint
        """
        ...

    def propagate(self) -> None:
        """
        Propagates the constraint
        """
        ...


class FuncConstraint(AbstractConstraint):

    def __init__(self, solver: CPSolver, filtering: Procedure) -> None:
        super().__init__(solver)
        self.filtering = filtering

    def post(self) -> None: ...

    def propagate(self) -> None:
        self.filtering()


class NotEqual(AbstractConstraint):
    """

    Represents the constraint x != y + offset, where x and y are two constraints
    and offset is an integer constant.

    """

    def __init__(self, x: IntVar, y: IntVar, offset: int = 0) -> None:
        super().__init__(x.get_solver())
        self._x: IntVar = x
        self._y: IntVar = y
        self._offset: int = offset

    def post(self) -> None:
        x, y = self._x, self._y
        if y.is_fixed():
            x.remove(y.min() + self._offset)
        elif x.is_fixed():
            y.remove(x.min() - self._offset)
        else:
            # This constraint can only propagate on domain fix
            x.propagate_on_fix()
            y.propagate_on_fix()

    def propagate(self) -> None:
        x, y = self._x, self._y
        if y.is_fixed():
            x.remove(y.min() + self._offset)
        else:
            y.remove(x.min() - self._offset)
        self.set_active(False)


class Equal(AbstractConstraint):

    def __init__(self, x: IntVar, y: IntVar) -> None:
        super().__init__(x.get_solver())
        self._x: IntVar = x
        self._y: IntVar = y

    def _handle_domain_change(self, v1: IntVar, v2: IntVar, values: list[int]) -> None:
        self._bounds_intersect()
        self._prune_equals(v1, v2, values)

    def _prune_equals(
        self, from_var: IntVar, to_var: IntVar, values: list[int]
    ) -> None: 
        ...

    def _bounds_intersect(self) -> None:
        """
        Ensures both variables have the same bounds
        """
        x, y = self._x, self._y
        new_min: int = max(x.min(), y.min())
        new_max: int = min(x.max(), y.max())
        x.remove_below(new_min)
        x.remove_above(new_max)
        y.remove_below(new_min)
        y.remove_above(new_max)

    def post(self) -> None:
        x, y = self._x, self._y
        if y.is_fixed():
            x.fix(y.min())
        elif x.is_fixed():
            y.fix(x.min())
        else:
            self._bounds_intersect()
            values: list[int] = [0] * max(len(x), len(y))
            self._prune_equals(y, x, values)
            self._prune_equals(x, y, values)
            x.when_domain_change(
                lambda: (lambda _values: self._handle_domain_change(x, y, _values))(
                    values
                )
            )
            y.when_domain_change(
                lambda: (lambda _values: self._handle_domain_change(y, x, _values))(
                    values
                )
            )

    def propagate(self) -> None: ...
