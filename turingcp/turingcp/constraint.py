
from abc import ABC, abstractmethod

class Constraint(ABC):

    @abstractmethod
    def post(self) -> None: ...

    @abstractmethod
    def propagate(self) -> None: ...

    @abstractmethod
    def set_scheduled(self, scheduled: bool) -> None: ...

    @abstractmethod
    def is_scheduled(self) -> bool: ...

    @abstractmethod
    def set_active(self) -> None: ...

    @abstractmethod
    def is_active(self) -> None: ...

