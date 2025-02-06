from collections.abc import Iterable
from typing import List, Optional, Any, Callable

from .constraint import Constraint
from .variable import Variable
from .exceptions import Inconsistency
from .domain import Domain
from .not_equal import NotEqual


class ToyCSP:
    """
    Class representing a Tiny Constraint Satisfaction Problem (TCSP).
    """

    def __init__(self):
        self.constraints: List[Constraint] = []
        self.variables: List[Variable] = []
        self.n_recur = 0  # Number of recursive calls

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
    
    def add_constraint(self, constraint: Constraint) -> Constraint:
        """
        Adds a not-equal constraint between two variables.

        Args:
            x: The first variable.
            y: The second variable.
            offset: The offset value. Defaults to 0.
        """
        self.constraints.append(constraint)
        self.fix_point()
        

    def fix_point(self) -> bool:
        """
        Performs constraint propagation until no further changes occur.

        Returns:
            True if a fix point is reached (no more changes), False otherwise.
        """
        fix = False
        while not fix:
            fix = True
            for constraint in self.constraints:
                fix &= not constraint.propagate()
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
        min_size = float('inf')
        smallest_var = None
        for var in self.variables:
            if not var.dom.is_fixed() and var.dom.size() < min_size:
                min_size = var.dom.size()
                smallest_var = var
        #return smallest_var if smallest_var else None
        return smallest_var
    
    
    def dfs(self, on_solution: Callable[[List[int]], Any]) -> None:
        """
        Performs Depth-First Search (DFS) to find all solutions to the CSP.

        Args:
            on_solution: A callback function that receives a solution (variable assignments).
        """
        self.n_recur += 1

        # Choisissez une variable non fixée (première rencontrée ou la plus petite)
        not_fixed = self.first_not_fixed()  # Essayer d'abord first_not_fixed (implémentation originale)

        if not not_fixed:
            # Toutes les variables sont fixées, une solution est trouvée
            solution = [var.dom.min() for var in self.variables]
            on_solution(solution)
        else:
            variable = not_fixed
            value = variable.dom.min()
            backup = self.backup_domains()

            # Branche gauche : affecter la valeur à la variable
            try:
                variable.dom.fix(value)
                self.fix_point()
                self.dfs(on_solution)
            except Inconsistency:
                pass

            # Restaurer les domaines avant d'explorer la branche droite
            self.restore_domains(backup)

            # Branche droite : retirer la valeur du domaine de la variable
            try:
                variable.dom.remove(value)
                self.fix_point()
                self.dfs(on_solution)
            except Inconsistency:
                pass
