from abc import ABC, abstractmethod
from typing import Protocol
from collections import namedtuple

from util_types import Procedure
from state_types import StateManager


class Constraint(ABC):

    @abstractmethod
    def post(self) -> None: ...

    @abstractmethod
    def propagate(self) -> None: ...
    
    @abstractmethod
    def get_solver(self) -> 'CPSolver': ...    

    @abstractmethod
    def set_scheduled(self, scheduled: bool) -> None: ...

    @abstractmethod
    def is_scheduled(self) -> bool: ...

    @abstractmethod
    def set_active(self) -> None: ...

    @abstractmethod
    def is_active(self) -> bool: ...



class IntVar(ABC):

    @abstractmethod
    def get_solver(self) -> 'CPSolver': ...
    
    @abstractmethod
    def when_fixed(self, f: Procedure) -> None: ...

    @abstractmethod
    def when_bound_change(self, f: Procedure) -> None: ...

    @abstractmethod
    def when_domain_change(self, f: Procedure) -> None: ...

    @abstractmethod
    def propagate_on_domain_change(self, c: Constraint) -> None: ...

    @abstractmethod
    def propagate_on_fix(self, c: Constraint) -> None: ...

    @abstractmethod
    def propagate_on_bound_change(self, c: Constraint) -> None: ...

    @abstractmethod
    def min(self) -> int: ...

    @abstractmethod
    def max(self) -> int: ...

    @abstractmethod
    def is_fixed(self) -> bool: ...

    @abstractmethod
    def fix(self, v: int) -> None: ...

    @abstractmethod
    def remove(self, v: int) -> None: ...

    @abstractmethod
    def remove_below(self, v: int) -> None: ...

    @abstractmethod
    def remove_above(self, v: int) -> None: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __contains__(self, v: int) -> bool: ...

    @abstractmethod
    def __repr__(self) -> str: ...


class BoolVar(IntVar):

    @abstractmethod
    def is_true(self) -> bool: ...

    @abstractmethod
    def is_false(self) -> bool: ...

    @abstractmethod
    def fix(b: bool) -> None: ...


class CPSolver(ABC):
    @abstractmethod
    def post(self, c: Constraint | BoolVar, enforce_fix_point: bool = True) -> None: ...

    @abstractmethod
    def schedule(self, c: Constraint) -> None: ...

    @abstractmethod
    def fix_point(self) -> None: ...

    @abstractmethod
    def get_state_manager(self) -> StateManager: ...

    @abstractmethod
    def on_fix_point(self, listener: Procedure) -> None: ...

    """
    @abstractmethod
    def minimize(self, x: IntVar) -> Objective: ...

    @abstractmethod
    def maximize(self, x: IntVar) -> Objective: ...
    """


class Objective(Protocol):

    def tighten(self) -> None: ...


DomainListener = namedtuple(
    "DomainListener", ["change", "change_max", "change_min", "fix", "empty"]
)


class IntDomain(ABC):

    @abstractmethod
    def min(self) -> int: ...

    @abstractmethod
    def max(self) -> int: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __contains__(self, v: int) -> bool: ...

    @abstractmethod
    def is_fixed(self) -> bool: ...

    @abstractmethod
    def remove(self, v: int, listener: DomainListener) -> None: ...

    @abstractmethod
    def remove_all_but(self, v: int, listener: DomainListener) -> None: ...

    @abstractmethod
    def remove_below(self, v: int, listener: DomainListener) -> None: ...

    @abstractmethod
    def remove_above(self, v: int, listener: DomainListener) -> None: ...

    @abstractmethod
    def __repr__(self) -> str: ...
