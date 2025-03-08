from abc import ABC, abstractmethod

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