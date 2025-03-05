

from collections.abc import Iterable

from state import StateManager, StateInt, CopyStateManager


class NoSuchElementException(Exception):
    pass


class StateSparseSet:
    """
    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, range(4, 8))
    >>> s._values
    [0, 1, 2, 3]
    >>> s
    StateSparseSet([4, 5, 6, 7])
    >>> len(s)
    4
    >>> len(s)
    4
    >>> s.to_list()
    [4, 5, 6, 7]
    >>> s.to_set() == {4, 5, 6, 7}
    True
    >>> s._min.value()
    0
    >>> s._max.value()
    3
    >>> s.min()
    4
    >>> s.max()
    7

    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, [2, 4, 6])
    >>> s
    StateSparseSet([2, 4, 6])
    >>> s._values
    [0, 4, 2, 3, 1]
    >>> len(s)
    3
    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, [])
    Traceback (most recent call last):
        ...
    ValueError: Set cannot be initialized with empty iterable
    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, [1])
    >>> 1 in s
    True
    >>> s.remove(1)
    True
    >>> 1 in s
    False
    >>> len(s)
    0
    >>> s.min()
    Traceback (most recent call last):
        ...
    NoSuchElementException: Unable to find min of empty set

    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, {3, 5, 7})
    >>> len(s)
    3
    >>> s._min.value()
    0
    >>> s.min()
    3
    """

    def __init__(self, sm: StateManager, values: Iterable[int]) -> None:
        if len(values) > 0:
            a = min(values)
            b = max(values)
        else:
            raise ValueError("Set cannot be initialized with empty iterable")

        self._size: StateInt = sm.make_state_int(b - a + 1)
        self._min: StateInt = sm.make_state_int(0)
        self._max: StateInt = sm.make_state_int(b - a)
        
        self._offset: int = a
        self._values: list[int] = list(range(0, b + 1 - a))
        self._indices: list[int] = self._values[:]

        # remove all the values that are not present in values
        for intern_value in self._values:
            val = intern_value + self._offset
            if val not in values:
                self.remove(val)

    def min(self) -> int:
        if self.is_empty():
            raise NoSuchElementException("Unable to find min of empty set")
        return self._min.value() + self._offset

    def max(self) -> int:
        if self.is_empty():
            raise NoSuchElementException("Unable to find max of empty set")
        return self._max.value() + self._offset

    def __len__(self) -> int:
        return self._size.value()

    def is_empty(self) -> bool:
        return len(self) == 0

    def remove(self, value: int) -> bool:
        """
        Removes `value` from set if possible in O(1) time.
        Returns `True` if it has been removed and `False` otherwise.

        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1, 2, 3, 4])
        >>> s
        StateSparseSet([1, 2, 3, 4])
        >>> s.remove(0)
        False
        >>> s.remove(2)
        True
        >>> 2 in s
        False
        >>> s.min()
        1
        >>> s.max()
        4
        >>> s
        StateSparseSet([1, 3, 4])
        >>> s._values
        [0, 3, 2, 1]
        >>> s.remove(2)
        False
        >>> s.remove(1)
        True
        >>> s.min()
        3
        >>> s.remove(4)
        True
        >>> s.max()
        3

        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [3, 5, 7])
        >>> s
        StateSparseSet([3, 5, 7])
        >>> s.remove(7)
        True
        >>> s
        StateSparseSet([3, 5])
        >>> 5 in s
        True
        >>> s.remove(5)
        True
        >>> s
        StateSparseSet([3])

        """
        if value not in self:
            return False

        intern_value = value - self._offset
        s = len(self)
        self._swap_positions(intern_value, self._values[s - 1])
        self._size.decrement()
        self._update_min(intern_value)
        self._update_max(intern_value)
        return True

    def _swap_positions(self, v1: int, v2: int) -> None:
        i1: int = self._indices[v1]
        i2: int = self._indices[v2]
        self._values[i1] = v2
        self._values[i2] = v1
        self._indices[v1] = i2
        self._indices[v2] = i1

    def remove_all_but(self, value: int) -> None:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1,2,3,4,5])
        >>> s.remove_all_but(3)
        >>> s
        StateSparseSet([3])
        >>> s.min()
        3
        >>> s.max()
        3
        >>> s.remove(3)
        True
        >>> s.remove_all_but(3)
        Traceback (most recent call last):
            ...
        NoSuchElementException: Value is not in set
        """
        if value not in self:
            raise NoSuchElementException("Value is not in set")
        _v: int = value - self._offset
        index: int = self._indices[_v]
        self._indices[_v] = 0
        self._indices[self._values[0]] = index
        self._values[index], self._values[0] = self._values[0], self._values[index]
        self._size.set_value(1)
        self._min.set_value(_v)
        self._max.set_value(_v)

    def remove_all(self) -> None:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [2, 3, 4])
        >>> len(s)
        3
        >>> s.remove_all()
        >>> s
        StateSparseSet([])
        """
        self._size.set_value(0)

    def remove_above(self, value: int) -> None:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [3, 4, 5, 6, 7])
        >>> s.remove_above(5)
        >>> s
        StateSparseSet([3, 4, 5])
        
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1, 3, 5, 6, 7])
        >>> s.remove_above(5)
        >>> s
        StateSparseSet([1, 3, 5])
        >>> s.remove_above(0)
        >>> s
        StateSparseSet([])
        """
        if value < self.min():
            self.remove_all()
        else:
            v = self.max()
            while v > value:
                self.remove(v)
                v -= 1

    def remove_below(self, value: int) -> None:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [3, 4, 5, 6, 7])
        >>> s.remove_below(5)
        >>> s
        StateSparseSet([5, 6, 7])
        
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1, 3, 5, 6, 7])
        >>> s.remove_below(5)
        >>> s
        StateSparseSet([5, 6, 7])
        >>> s.remove_below(10)
        >>> s
        StateSparseSet([])
        """
        if value > self.max():
            self.remove_all()
        else:
            v = self.min()
            while v < value:
                self.remove(v)
                v += 1

    def _update_min(self, intern_value: int) -> None:
        if not self.is_empty() and intern_value == self._min.value():
            val = self._min.value() + 1
            while not self._raw_contains(val):
                val += 1
            self._min.set_value(val)

    def _update_max(self, intern_value: int) -> None:
        if not self.is_empty() and intern_value == self._max.value():
            val = self._max.value() - 1
            while not self._raw_contains(val):
                val -= 1
            self._max.set_value(val)

    def _raw_contains(self, value: int) -> bool:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1])
        >>> s._values
        [0]
        >>> len(s)
        1
        >>> s._min.value()
        0
        >>> s._raw_contains(-1)
        False
        >>> s._raw_contains(1)
        False
        >>> s._raw_contains(0)
        True
        >>> s._size.set_value(0)
        0
        >>> s._raw_contains(0)
        False
        """
        if value < self._min.value() or value > self._max.value():
            return False
        else:
            return self._indices[value] < len(self)

    def _index_of(self, value: int) -> int:
        return self._indices[value]

    def __contains__(self, value: int) -> bool:
        return self._raw_contains(value - self._offset)

    def to_list(self) -> list[int]:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1, 2, 3])
        >>> s.to_list()
        [1, 2, 3]
        """
        return sorted([x + self._offset for x in self._values[:len(self)]])

    def to_set(self) -> set[int]:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [2, 4, 6])
        >>> s.to_set() == {2, 4, 6}
        True
        """
        return set(self.to_list())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_list()})"

    def __str__(self) -> str:
        """
        >>> sm = CopyStateManager()
        >>> s = StateSparseSet(sm, [1, 2, 3])
        >>> str(s)
        '{1, 2, 3}'
        """
        return "{" + ", ".join(str(x) for x in self.to_list()) + "}"

def intern_tests():
    '''
    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, range(8))
    >>> s
    StateSparseSet([0, 1, 2, 3, 4, 5, 6, 7])
    >>> s._values
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> s._indices
    [0, 1, 2, 3, 4, 5, 6, 7]
    
    [0, 4, 2, 3, 1]
    >>> s._size.value()
    8
    >>> s.remove(4)
    True
    >>> s._values
    [0, 1, 2, 3, 7, 5, 6, 4]
    >>> s._indices
    [0, 1, 2, 3, 7, 5, 6, 4]

    >>> s.remove(7)
    True
    >>> s._values
    [0, 1, 2, 3, 6, 5, 7, 4]
    >>> s._indices
    [0, 1, 2, 3, 7, 5, 4, 6]
    >>> s._max.value()
    6
    >>> s.remove_below(2)
    >>> s._values
    [5, 6, 2, 3, 1, 0, 7, 4]
    >>> s._indices
    [5, 4, 2, 3, 7, 0, 1, 6]
    >>> s._size.value()
    4
    >>> s._min.value()
    2
    >>> s.remove_all_but(6)
    >>> s._values
    [6, 5, 2, 3, 1, 0, 7, 4]
    >>> s._indices
    [5, 4, 2, 3, 7, 1, 0, 6]
    
    '''
    ...
    

def state_tests():
    '''
    >>> sm = CopyStateManager()
    >>> s = StateSparseSet(sm, range(5))
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(5), CopyStateEntry(0), CopyStateEntry(4)])])
    >>> s.remove(3)
    True
    >>> s
    StateSparseSet([0, 1, 2, 4])
    >>> s.remove(1)
    True
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(5), CopyStateEntry(0), CopyStateEntry(4)]), Backup([CopyStateEntry(3), CopyStateEntry(0), CopyStateEntry(4)])])
    >>> s.remove(4)
    True
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(5), CopyStateEntry(0), CopyStateEntry(4)]), Backup([CopyStateEntry(3), CopyStateEntry(0), CopyStateEntry(4)]), Backup([CopyStateEntry(2), CopyStateEntry(0), CopyStateEntry(2)])])
    >>> s.remove(0)
    True
    >>> s
    StateSparseSet([2])
    >>> sm.get_level()
    2
    >>> sm.restore_state()
    >>> s
    StateSparseSet([0, 2])
    >>> sm.restore_state_until(0)
    >>> s
    StateSparseSet([0, 2, 4])
    >>> sm.restore_state()
    >>> sm.get_level()
    -1
    >>> s
    StateSparseSet([0, 1, 2, 3, 4])
    '''

if __name__ == "__main__":
    import doctest
    doctest.testmod()
