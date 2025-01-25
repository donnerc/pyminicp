from .constraint import Constraint  # Assuming constraint.py is in the same directory
from .variable import Variable  # Assuming variable.py is in the same directory

from typing import override


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
