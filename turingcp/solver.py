from typing import Deque

from collections import deque

from cp_types import CPSolver, IntVar, BoolVar, Constraint

from state import StateManager
from util_types import Procedure
from state_stack import StateStack
from linked_queue import LinkedQueue

from utils import InconsistencyException


class TuringCP(CPSolver):

    def __init__(self, sm: StateManager) -> None:
        self._propagation_queue: Deque[Constraint] = deque()
        self._fix_point_listeners: LinkedQueue[Procedure] = LinkedQueue()
        self._sm = sm
        
        self.vars: StateStack[IntVar] = StateStack(sm)
        
    def add_variable(self, var: IntVar) -> None:
        self.vars.push(var)

    def get_state_manager(self) -> StateManager:
        return self._sm

    def schedule(self, c: Constraint) -> None:
        if c.is_active() and not c.is_scheduled():
            c.set_scheduled(True)
            self._propagation_queue.append(c)

    def on_fix_point(self, listener: Procedure) -> None:
        self._fix_point_listeners.enqueue(listener)

    def _notify_fix_point(self) -> None:
        for listener in self._fix_point_listeners:
            listener()

    def fix_point(self) -> None:
        """

        Applies the fix point algorithm to all constraints scheduled in the
        propagation queue until no propagation is possible (propagation queue
        empty) or until reaching inconsistency. On inconsistency, unschedules
        all the constraints.

        """
        try:
            self._notify_fix_point()
            while len(self._propagation_queue) > 0:
                self._propagate(self._propagation_queue.popleft())
        except InconsistencyException as e:
            # set all the constraints in propagation queue to unscheduled
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

    def __repr__(self) -> str:
        return f'TuringCP(prop_q={repr(self._propagation_queue)})'