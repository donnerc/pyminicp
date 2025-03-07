"""
############### Importation dans WebTigerPython ############
from pyodide.http import open_url
gist_url = 'https://gist.githubusercontent.com/donnerc/c5ff613995da958b50103388327bedeb/raw/8c09531f2584f1208814e43366d94eece726c394/get_code_from_runestone.py'
with open('runestone.py', 'w') as fd: fd.write(open_url(gist_url).read())
from runestone import get_module
await get_module('turing-cp-2025', 'turingcp_stack', 'stack')
############################################################
"""

from stack import Stack

from util_types import Procedure
from state_types import *


class Copy[T](Storage, State[T]):

    class CopyStateEntry[T](StateEntry):

        def __init__(self, parent: "Copy") -> None:
            self._parent = parent
            self._v = parent._v

        def restore(self) -> None:
            self._parent._v = self._v

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self._v})"

    def __init__(self, init_value: T) -> None:
        self._v = init_value

    def set_value(self, value: T) -> T:
        self._v = value
        return value

    def value(self):
        return self._v

    def save(self) -> StateEntry:
        return self.CopyStateEntry(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._v)})"


class CopyInt(Copy[int], StateInt):

    def __init__(self, init_value: int) -> None:
        super().__init__(init_value)


class NewState:

    def __init__(self, sm: StateManager) -> None:
        self._level: int = -1
        self.sm: StateManager = sm

    def __enter__(self) -> None:
        self._level = self.sm.get_level()
        self.sm.save_state()
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.sm.restore_state_until(self._level)


class CopyStateManager(StateManager):
    """
    >>> sm = CopyStateManager()
    >>> sm.get_level()
    -1
    >>> x = sm.make_state_int(1)
    >>> x
    CopyInt(1)
    >>> x.value()
    1
    >>> sm.save_state()
    >>> sm.get_level()
    0
    >>> x.set_value(2)
    2
    >>> y = sm.make_state_int(10)
    >>> sm.save_state()
    >>> sm.get_level()
    1
    >>> x.set_value(3)
    3
    >>> x.value()
    3
    >>> y.set_value(20)
    20
    >>> sm.prior
    Stack([Backup([CopyStateEntry(1)]), Backup([CopyStateEntry(2), CopyStateEntry(10)])])
    >>> sm.store
    Stack([CopyInt(3), CopyInt(20)])
    >>> sm.restore_state()
    >>> x
    CopyInt(2)
    >>> y
    CopyInt(10)
    >>> sm.get_level()
    0
    >>> sm.restore_state()
    >>> x
    CopyInt(1)
    >>> y
    CopyInt(10)
    >>> sm.get_level()
    -1

    >>> sm = CopyStateManager()
    >>> z = [sm.make_state_int(2 * i) for i in range(3)]
    >>> sm.save_state()
    >>> for x in z: x.increment()
    1
    3
    5
    >>> z
    [CopyInt(1), CopyInt(3), CopyInt(5)]
    >>> sm.restore_state()
    >>> z
    [CopyInt(0), CopyInt(2), CopyInt(4)]
    """

    class Backup(Stack[StateEntry]):

        def __init__(self, store):
            super().__init__()
            self._store = store
            self._sz = len(self._store)
            for s in self._store:
                self.push(s.save())

        def restore(self) -> None:
            for state_entry in self:
                state_entry.restore()

    def __init__(self) -> None:
        self.store: Stack[Storage] = Stack[Storage]()
        self.prior: Stack[self.Backup] = Stack[self.Backup]()
        # à voir si on veut une LinkedList ici ...
        self.on_restore_listeners: list[Procedure] = []

    def notify_restore(self) -> None:
        for listener in self.on_restore_listeners:
            listener()

    def on_restore(self, listener: Procedure) -> None:
        self.on_restore_listeners.append(listener)

    def get_level(self) -> int:
        return len(self.prior) - 1

    def store_size(self) -> int:
        return len(self.store)

    def save_state(self) -> None:
        self.prior.push(self.Backup(self.store))

    def restore_state(self) -> None:
        self.prior.pop().restore()
        self.notify_restore()

    def restore_state_until(self, level: int) -> None:
        while self.get_level() > level:
            self.restore_state()

    def with_new_state(self, proc: Procedure) -> None:
        level: int = self.get_level()
        self.save_state()
        proc()
        self.restore_state_until(level)

    def make_state_int(self, init_value: int) -> StateInt:
        """
        Creates an Integer that can be restored in place on `restore_state()`
        """
        s: CopyInt = CopyInt(init_value)
        self.store.push(s)
        return s

    def make_state_obj[T](self, obj: T) -> State[T]:
        """
        >>> sm = CopyStateManager()
        >>> obj = sm.make_state_obj(True)
        >>> obj
        Copy(True)
        >>> sm.save_state()
        >>> obj.set_value(False)
        False
        >>> obj
        Copy(False)

        >>> sm = CopyStateManager()
        >>> obj = sm.make_state_obj([1, 2, 3])
        >>> obj
        Copy([1, 2, 3])
        >>> sm.save_state()
        >>> obj.set_value("this is a bad example")
        'this is a bad example'
        >>> obj
        Copy('this is a bad example')
        >>> sm.restore_state()
        >>> obj
        Copy([1, 2, 3])
        """
        r: Copy = Copy(init_value=obj)
        self.store.push(r)
        return r


if __name__ == "__main__":
    import doctest

    doctest.testmod()
