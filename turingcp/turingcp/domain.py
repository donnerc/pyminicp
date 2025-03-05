from abc import ABC, abstractmethod
from collections.abc import Iterable

from state_sparse_set import StateSparseSet
from state import StateManager, CopyStateManager

from cp_types import IntDomain, DomainListener


class SparseSetDomain(IntDomain):
    """
    >>> listener = DomainListener(change=lambda: print("changed"), change_max=lambda: print("max changed"), change_min=lambda: print("min changed"), fix=lambda: print("fixed"), empty=lambda: print("all values removed"))
    >>> sm = CopyStateManager()
    >>> d = SparseSetDomain(sm, range(5, 10))
    >>> d
    SparseSetDomain([5, 6, 7, 8, 9])
    >>> d.min()
    5
    >>> d.max()
    9
    >>> len(d)
    5
    >>> 7 in d
    True
    >>> d.remove(7, listener)
    changed
    >>> 7 in d
    False
    >>> d.remove(7, listener)
    >>> d.remove(5, listener)
    changed
    min changed
    >>> d
    SparseSetDomain([6, 8, 9])
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3), CopyStateEntry(1), CopyStateEntry(4)])])
    >>> d.remove_below(9, listener)
    fixed
    min changed
    changed
    >>> d
    SparseSetDomain([9])
    >>> d.remove(9, listener)
    all values removed
    changed
    min changed
    max changed
    >>> d
    SparseSetDomain([])
    >>> sm.restore_state()
    >>> d
    SparseSetDomain([6, 8, 9])
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3), CopyStateEntry(1), CopyStateEntry(4)])])
    >>> d.remove_above(6, listener)
    fixed
    min changed
    changed
    >>> d
    SparseSetDomain([6])
    >>> sm.restore_state()
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3), CopyStateEntry(1), CopyStateEntry(4)])])
    >>> d
    SparseSetDomain([6, 8, 9])
    >>> d.remove_all_but(8, listener)
    fixed
    changed
    fixed
    >>> d
    SparseSetDomain([8])
    >>> d.remove_all_but(9, listener)
    all values removed
    >>> d
    SparseSetDomain([])
    >>> sm.restore_state_until(-1)
    >>> d
    SparseSetDomain([6, 8, 9])
    """

    def __init__(self, sm: StateManager, values: Iterable[int]):
        self.domain: StateSparseSet = StateSparseSet(sm, values)

    def min(self) -> int:
        return self.domain.min()

    def max(self) -> int:
        return self.domain.max()

    def __len__(self) -> int:
        return len(self.domain)

    def __contains__(self, v: int) -> bool:
        return v in self.domain

    def is_fixed(self) -> bool:
        return len(self.domain) == 1

    def remove(self, v: int, listener: DomainListener) -> None:
        if v in self.domain:
            max_changed: bool = self.max() == v
            min_changed: bool = self.min() == v
            self.domain.remove(v)
            if len(self.domain) == 0:
                listener.empty()
            listener.change()
            if min_changed:
                listener.change_min()
            if max_changed:
                listener.change_max()
            if len(self.domain) == 1:
                listener.fix()

    def remove_all_but(self, v: int, listener: DomainListener) -> None:
        if v in self.domain:
            if len(self.domain) > 1:
                max_changed: bool = self.max() == v
                min_changed: bool = self.min() == v
                self.domain.remove_all_but(v)
                if len(self.domain) == 0:
                    listener.empty()
                listener.fix()
                listener.change()

                if min_changed:
                    listener.change_min()
                if max_changed:
                    listener.change_max()
                if len(self.domain) == 1:
                    listener.fix()
        else:
            self.domain.remove_all()
            listener.empty()

    def remove_below(self, v: int, listener: DomainListener) -> None:
        if v > self.domain.min():
            self.domain.remove_below(v)
            if len(self.domain) == 0:
                listener.empty()
            else:
                if len(self.domain) == 1:
                    listener.fix()

                listener.change_min()
                listener.change()

    def remove_above(self, v: int, listener: DomainListener) -> None:
        if v < self.domain.max():
            self.domain.remove_above(v)
            if len(self.domain) == 0:
                listener.empty()
            else:
                if len(self.domain) == 1:
                    listener.fix()

                listener.change_min()
                listener.change()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.domain.to_list()})"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
