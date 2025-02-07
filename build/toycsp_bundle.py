
#####################################################
# Single file bundle of toycsp generated on 2025-02-07 19:39:54.558902
# Do not modify file
# Regenerate with 
#   python bundler.py > csp_bundle.py
#####################################################


from collections.abc import Iterable
from abc import ABC, abstractmethod
from typing import override
from typing import List, Optional, Any, Callable

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
    
    def __init__(self, dom: Iterable[int], name: str = None) -> None:
        self.dom = Domain(set(dom))
        self.name = name or 'Var' + str(Variable.var_counter)
        Variable.var_counter += 1
        
    def value(self) -> int:
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
        Initializes the NotEqual constraint.

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

        self.constraints: List[Constraint] = []
        self.variables: List[Variable] = []
        self.n_recur = 0  # Number of recursive calls

        # collects all handlers (args beginning with `on_`)
        self.handlers = {
            arg.split('on_')[1]: [value] for arg, value in kwargs.items() if arg.startswith("on_")
        }

    def __repr__(self) -> str:
        #return f"ToyCSP(constraints={self.constraints}, variables={self.variables})"
        return f"ToyCSP : #vars = {len(self.variables)} / #constraints = {len(self.constraints)}"

    def register_handler(self, event, handler) -> None:
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]

    def call_handlers(self, event: str, infos: dict[str, Any]) -> None:
        if event in self.handlers:
            handlers = self.handlers[event]
            for h in handlers: h(self, infos)

    def on(self, *events):
        def decorator(func):
            for event in events:
                self.register_handler(event, func)
        return decorator
        

    def no_op(self, csp: "ToyCSP", infos: dict[str, Any]) -> None:
        pass

    def add_variable(self, domain: Iterable[int]) -> Variable:
        """
        Creates a variable with the given domain size.

        Args:
            dom_size: The number of values in the domain.

        Returns:
            A new Variable object.
        """
        var = Variable(domain)
        self.variables.append(var)
        return var

    def post(self, constraint: Constraint, schedule_fixpoint=True) -> Constraint:
        """
        Adds a not-equal constraint between two variables.

        Args:
            x: The first variable.
            y: The second variable.
            offset: The offset value. Defaults to 0.
        """
        self.constraints.append(constraint)
        if schedule_fixpoint:
            self.fix_point()

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

    def backup_domains(self) -> List[Domain]:
        """
        Creates a backup copy of all variable domains.

        Returns:
            A list of Domain objects representing the backed-up domains.
        """
        backup = [var.dom.clone() for var in self.variables]
        return backup

    def restore_domains(self, backup: List[Domain]) -> None:
        """
        Restores the domains of all variables from the backup.

        Args:
            backup: A list of Domain objects representing the backed-up domains.
        """
        for i, var in enumerate(self.variables):
            var.dom = backup[i]

    def first_not_fixed(self) -> Optional[Variable]:
        """
        Finds the first variable that has a non-fixed domain.

        Returns:
            An Optional containing the first unfixed variable, or None if all are fixed.
        """
        # https://www.programiz.com/python-programming/methods/built-in/next
        return next((var for var in self.variables if not var.dom.is_fixed()), None)

    def smallest_not_fixed(self) -> Optional[Variable]:
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

    def get_solution(self) -> list[int]:
        return [v.value() for v in self.variables]

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
                self.handlers.get("on_inconsistency", self.no_op)(
                    self, {"event": "inconsistent", "current_var": variable}
                )
                pass

            # Restaurer les domaines avant d'explorer la branche droite
            self.restore_domains(backup)

            # Branche droite : retirer la valeur du domaine de la variable
            try:
                variable.dom.remove(value)
                self.fix_point()
                self.dfs()
            except Inconsistency:
                self.handlers.get("on_inconsistency", self.no_op)(
                    self, {"event": "inconsitent", "current_var": variable}
                )
                pass
