#####################################################
# Single file bundle of toycsp generated on 2026-03-21 01:55:59.928009
# Do not modify file
# Regenerate with 
#   python bundler.py > csp_bundle.py
#####################################################


from collections.abc import Iterable
from abc import ABC, abstractmethod
from typing import override
from typing import Optional, Any, Callable, cast

type PartialSolution = list[int | None]
type Solution = list[int]


class Inconsistency(Exception):
    """Exception raised when a constraint propagation leads to an empty domain."""
    pass





class Domain:
    """
    Implementation of a very basic domain
    using a set to store the values
    """

    def __init__(self, *args) -> None:
        """
        Initializes a domain with {0, ... ,n-1}

        Args:
            n: The number of values in the domain.
        """
        if len(args) != 1:
            raise TypeError("Domain takes only one parameter")
        elif isinstance(args[0], int):
            n = args[0]
            self.values = set(range(n))
        elif isinstance(args[0], set):
            dom = args[0]
            self.values = dom.copy()
        else:
            raise TypeError("Argument must be int or set[int]")

    def is_fixed(self) -> bool:
        """
        Verifies if only one value left

        Returns:
            True if only one value left, False otherwise.
        """
        return len(self.values) == 1

    def size(self) -> int:
        """
        Gets the domain size

        Returns:
            The number of values in the domain.
        """
        return len(self.values)
    
    def __len__(self) -> int:
        """
        Same as .size()
        """
        return self.size()

    def min(self) -> int:
        """
        Gets the minimum of the domain

        Returns:
            The minimum value in the domain.
        """
        return min(self.values)
    
    def max(self) -> int:
        """
        Gets the maximum of the domain

        Returns:
            The maximum value in the domain.
        """
        return max(self.values)

    def remove(self, v: int) -> bool:
        """
        Removes value v from the domain

        Args:
            v: The value to remove.

        Returns:
            True if the value was present in the domain, False otherwise.
        """
        if v in self.values:
            self.values.remove(v)
            if not self.values:
                raise Inconsistency
            return True
        return False

    def fix(self, v: int):
        """
        Fixes the domain to value v

        Args:
            v: The value to fix the domain to.

        Raises:
            Inconsistency: If the value is not in the domain.
        """
        if v not in self.values:
            raise Inconsistency
        self.values = {v}

    def clone(self) -> "Domain":
        """
        Creates a copy of the domain.

        Returns:
            A new Domain object with the same values.
        """
        return Domain(self.values)

    def __repr__(self) -> str:
        return f"Domain({self.values})"




class Variable:

    var_counter = 0
    
    def __init__(self, dom: Iterable[int], name: str | None = None) -> None:
        self.dom = Domain(set(dom))
        self.name = name or 'Var' + str(Variable.var_counter)
        Variable.var_counter += 1
        
    def value(self) -> int | None:
        if self.dom.is_fixed():
            return self.dom.min()
        else:
            return None
        
    
    def __repr__(self) -> str:
        return f"Variable(dom={self.dom.values}, name='{self.name}')"



class Constraint(ABC):
    """
    Abstract base class for constraints.
    """

    @abstractmethod
    def propagate(self) -> bool:
        """
        Propagate the constraint and return True if any value could be removed.

        Returns:
            True if at least one value of one variable could be removed, False otherwise.
        """
        pass




class NotEqual(Constraint):
    """
    Constraint representing x != y + offset.
    """

    def __init__(self, x: Variable, y: Variable, offset: int = 0) -> None:
        """
        Initializes the NotEqual constraint (x != y + offset).

        Args:
            x: The first variable.
            y: The second variable.
            offset: The offset value. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.offset = offset

    @override
    def propagate(self) -> bool:
        """
        Propagates the NotEqual constraint.

        Returns:
            True if any value was removed from a domain, False otherwise.
        """
        if self.x.dom.is_fixed():
            return self.y.dom.remove(self.x.dom.min() - self.offset)
        elif self.y.dom.is_fixed():
            return self.x.dom.remove(self.y.dom.min() + self.offset)
        return False

    def __repr__(self) -> str:
        return f'NotEqual(x={self.x}, y={self.y}, offset={self.offset})'





class ToyCSP:
    """
    Class representing a Tiny Constraint Satisfaction Problem (TCSP).
    """

    def __init__(self, *args, **kwargs):

        self.constraints: list[Constraint] = []
        self.variables: list[Variable] = []
        self.n_recur: int = 0  # Number of recursive calls

        # collects all handlers (args beginning with `on_`)
        self.handlers = {
            arg.split('on_')[1]: [value] for arg, value in kwargs.items() if arg.startswith("on_")
        }

    def __repr__(self) -> str:
        # return f"ToyCSP(constraints={self.constraints}, variables={self.variables})"
        return f"ToyCSP : #vars = {len(self.variables)} / #constraints = {len(self.constraints)}"

    def add_variable(self, domain: Iterable[int], name: str | None = None) -> Variable:
        """
        Creates a variable with the given domain.

        Args:
            domain: An iterable of integers representing the domain values.
            name: An optional name for the variable.

        Returns:
            A new Variable object.
        """
        var = Variable(domain, name)
        self.variables.append(var)
        return var

    def post(self, constraint: Constraint, schedule_fixpoint=True) -> Constraint:
        """
        Posts (adds) a constraint to the CSP and optionally schedules a fix point.

        Args:
            constraint: The constraint to add.
            schedule_fixpoint: If True, schedules a fix point after adding the constraint.

        Returns:
            The added constraint.
        """
        self.constraints.append(constraint)
        if schedule_fixpoint:
            self.fix_point()
        return constraint

    def backup_domains(self) -> list[Domain]:
        """
        Creates a backup copy of all variable domains.

        Returns:
            A list of Domain objects representing the backed-up domains.
        """
        backup = [var.dom.clone() for var in self.variables]
        return backup

    def restore_domains(self, backup: list[Domain]) -> None:
        """
        Restores the domains of all variables from the backup.

        Args:
            backup: A list of Domain objects representing the backed-up domains.
        """
        for i, var in enumerate(self.variables):
            var.dom = backup[i]

    def get_partial_solution(self) -> PartialSolution:
        """
        Returns the current partial solution as a list of variable values or None for unfixed variables.

        Returns:
            A list of integers or None representing the current partial solution.
        """
        return [cast(Optional[int], var.value()) for var in self.variables]

    def get_solution(self) -> Solution:
        """
        Returns the current solution as a list of variable values.

        Raises a ValueError if not all variables are fixed.

        Returns:
            A list of integers representing the solution.
        """
        if not all(var.dom.is_fixed() for var in self.variables):
            raise ValueError(
                "Not all variables are fixed. No solution available.")
        return [cast(int, v.value()) for v in self.variables]

    def first_not_fixed(self) -> Variable | None:
        """
        Finds the first variable that has a non-fixed domain.

        Returns:
            An Optional containing the first unfixed variable, or None if all are fixed.
        """
        # https://www.programiz.com/python-programming/methods/built-in/next
        return next((var for var in self.variables if not var.dom.is_fixed()), None)

    def smallest_not_fixed(self) -> Variable | None:
        """
        Finds the variable with the smallest domain size that is not fixed.

        Returns:
            An Optional containing the variable with the smallest domain, or None if all are fixed.
        """
        min_size = float("inf")
        smallest_var = None
        for var in self.variables:
            if not var.dom.is_fixed() and var.dom.size() < min_size:
                min_size = var.dom.size()
                smallest_var = var
        # return smallest_var if smallest_var else None
        return smallest_var

    def fix_point(self) -> bool:
        """
        Performs constraint propagation until no further changes occur.

        Returns:
            True if a fix point is reached (no more changes), False otherwise.
        """
        self.call_handlers("beforefixpoint", {"event": "before fixpoint"})

        fix = False
        while not fix:
            fix = True
            for constraint in self.constraints:
                was_usefull = constraint.propagate()
                # if only one propagation is usefull amongst all constraints,
                # fix will become false and the while
                # loop will continue
                fix &= not was_usefull
                self.call_handlers("propagate", {
                    "event": f"propagating",
                    "usefull": was_usefull,
                    "constraint": constraint,
                })

        self.call_handlers("afterfixpoint", {"event": "after fixpoint"})

        return fix

    def dfs(self, on_solution=None, on_fixpoint=None) -> None:
        """
        Performs Depth-First Search (DFS) to find all solutions to the CSP.

        Args:
            on_solution: A callback function that receives a solution (variable assignments).
        """
        self.n_recur += 1

        # Choisissez une variable non fixée (première rencontrée ou la plus petite)
        not_fixed = (
            self.first_not_fixed()
        )  # Essayer d'abord first_not_fixed (implémentation originale)

        if not not_fixed:
            # Toutes les variables sont fixées, une solution est trouvée
            self.call_handlers("solution", {})
        else:
            variable = not_fixed
            value = variable.dom.min()
            backup = self.backup_domains()

            # Branche gauche : affecter la valeur à la variable
            try:
                variable.dom.fix(value)
                self.fix_point()
                self.dfs()
            except Inconsistency:
                self.call_handlers(
                    "inconsistent", {"event": "inconsistent", "current_var": variable})

            # Restaurer les domaines avant d'explorer la branche droite
            self.restore_domains(backup)

            # Branche droite : retirer la valeur du domaine de la variable
            try:
                variable.dom.remove(value)
                self.fix_point()
                self.dfs()
            except Inconsistency:
                self.call_handlers(
                    "inconsistent", {"event": "inconsistent", "current_var": variable})

    ##############################################################################
    # Event handler registration and management

    def register_handler(self, event, handler) -> None:
        """Registers a handler function for a specific event."""
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]

    def call_handlers(self, event: str, infos: dict[str, Any]) -> None:
        """Calls all registered handlers for a specific event."""
        if event in self.handlers:
            handlers = self.handlers[event]
            for h in handlers:
                h(self, infos)

    def on(self, *events):
        """Decorator to register a function as a handler for one or more events."""
        def decorator(func):
            for event in events:
                self.register_handler(event, func)
        return decorator

    def no_op(self, csp: "ToyCSP", infos: dict[str, Any]) -> None:
        """A no-op handler that does nothing."""
        pass

    ##############################################################################


