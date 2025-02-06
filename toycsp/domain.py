from typing import Set

from .exceptions import Inconsistency


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
            raise TypeError("Argument must be int or Domain")

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