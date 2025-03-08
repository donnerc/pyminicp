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
    '''
    The StateManager exposes all the mechanisms and data-structures needed to
    implement a depth-first-search with reversible states.
    '''

    def save_state(self) -> None:
        '''
        Stores the current state such that it can be recovered using
        restore_state(). Increase the level by 1
        '''
        ...

    def restore_state(self) -> None:
        '''
        Restores state as it was at `get_level()-1`
        Decrease the level by 1
        '''
        ...

    def restore_state_until(self, level: int) -> None:
        '''
        Restores the state up the the given level.

        param: level the level, a non negative number between 0 and get_level
        '''
        ...

    def on_restore(self, listener: Procedure) -> None:
        '''
        Add a listener that is notified each time the `restore_state()` is
        called.
        '''
        ...

    def get_level(self) -> int:
        '''
        Returns the current level. It is increased at each `save_state()` and
        decreased at each `restore_state()`. It is initially equal to -1.
        
        returns current the level
        '''
        ...

    def make_state_int(self, init_value: int) -> StateInt:
        """
        Creates an Integer that can be restored in place on `restore_state()`
        """
        ...

    def make_state_obj[T](self, obj: T) -> State[T]:
        """
        Creates an object of type `T` that can be restored in place on
        `restore_state()`
        """
        ...