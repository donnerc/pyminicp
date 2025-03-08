from typing import Protocol

from util_types import Procedure


class State[T](Protocol):

    def set_value(self, v: T) -> T: ...

    def value(self) -> T: ...

    def __str__(self) -> str: ...


class StateEntry(Protocol):

    def restore(self) -> None: ...


class Storage(Protocol):

    def save(self) -> StateEntry: ...
    

class StateInt(State[int]):

    def increment(self) -> int:
        return self.set_value(self.value() + 1)

    def decrement(self) -> int:
        return self.set_value(self.value() - 1)

class StateManager(Protocol):

    def save_state(self) -> None: ...

    def restore_state(self) -> None: ...

    def restore_state_until(self, level: int) -> None: ...

    def on_restore(self, listener: Procedure) -> None: ...

    def get_level(self) -> int: ...

    def make_state_int(self, init_value: int) -> StateInt: ...
