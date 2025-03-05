from abc import ABC, abstractmethod
from typing import Protocol, Deque

from collections import deque

from state import StateManager
from utils import Procedure, InconsistencyException
from state_stack import StateStack
from linked_queue import LinkedQueue
from constraint import Constraint
from variable import IntVar, BoolVar



class Objective(Protocol):

    def tighten(self) -> None: ...


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

    @abstractmethod
    def minimize(self, x: IntVar) -> Objective: ...

    @abstractmethod
    def maximize(self, x: IntVar) -> Objective: ...


class TuringCP(CPSolver):

    def __init__(self, sm: StateManager) -> None:
        self._propagation_queue: Deque[Constraint] = deque()
        self._fix_point_listeners: LinkedQueue[Procedure]
        self._sm = sm
        self.vars: StateStack[IntVar] = StateStack(sm)

    def get_state_manager(self) -> StateManager:
        return self._sm

    def schedule(self, c: Constraint) -> None:
        if c.is_active() and not c.is_scheduled():
            c.set_scheduled(True)
            self._propagation_queue.append(c)

    def on_fix_point(self, listener: Procedure) -> None:
        self._fix_point_listeners.enqueue(listener)

    def _notify_fix_point(self):
        for listener in self._fix_point_listeners:
            listener()

    def fix_point(self) -> None:
        try:
            self._notify_fix_point()
            while len(self._propagation_queue) > 0:
                self._propagate(self._propagation_queue.popleft())
        except InconsistencyException as e:
            while len(self._propagation_queue) > 0:
                self._propagation_queue.popleft().set_scheduled(False)
            raise e

    def _propagate(self, c: Constraint) -> None:
        # shouldn't this be part of the fix_point method ...
        c.set_scheduled(False)
        if c.is_active():
            c.propagate()

    def post(self, c: Constraint, enforce_fix_point: bool = True) -> None:
        c.post()
        if enforce_fix_point:
            self.fix_point()
