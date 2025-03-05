from abc import ABC, abstractmethod
from collections.abc import Iterable

# SparseSet implementation
# Inspired by MiniCP SparseSets
# Cédric Donner, February 2025


class CPException(Exception):
    pass


class NoSuchElementException(CPException):
    pass


class SparseSet:
    """
    >>> s = SparseSet(range(4, 8))
    >>> s._values
    [0, 1, 2, 3]
    >>> s
    SparseSet([4, 5, 6, 7])
    >>> len(s)
    4
    >>> len(s)
    4
    >>> s.to_list()
    [4, 5, 6, 7]
    >>> s.to_set() == {4, 5, 6, 7}
    True
    >>> s._min
    0
    >>> s._max
    3
    >>> s.min()
    4
    >>> s.max()
    7

    >>> s = SparseSet([2, 4, 6])
    >>> s
    SparseSet([2, 4, 6])
    >>> s._values
    [0, 4, 2, 3, 1]
    >>> s._size
    3
    >>> s = SparseSet([])
    Traceback (most recent call last):
        ...
    ValueError: Set cannot be initialized with empty iterable
    >>> s = SparseSet([1])
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

    >>> s = SparseSet({3, 5, 7})
    >>> len(s)
    3
    >>> s._min
    0
    >>> s.min()
    3
    """

    def __init__(self, values: Iterable[int]) -> None:
        if len(values) > 0:
            a = min(values)
            b = max(values)
        else:
            raise ValueError("Set cannot be initialized with empty iterable")

        self._size: int = b - a + 1

        self._min = 0
        self._max = b - a
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
        return self._min + self._offset

    def max(self) -> int:
        if self.is_empty():
            raise NoSuchElementException("Unable to find max of empty set")
        return self._max + self._offset

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return len(self) == 0

    def remove(self, value: int) -> bool:
        """
        Removes `value` from set if possible in O(1) time.
        Returns `True` if it has been removed and `False` otherwise.

        >>> s = SparseSet([1, 2, 3, 4])
        >>> s
        SparseSet([1, 2, 3, 4])
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
        SparseSet([1, 3, 4])
        >>> s._values
        [0, 3, 2, 1]
        >>> s.remove(2)
        False
        >>> s.remove(1)
        True
        >>> s.min()
        3<<x
        >>> s.remove(4)
        True
        >>> s.max()
        3

        >>> s = SparseSet([3, 5, 7])
        >>> s
        SparseSet([3, 5, 7])
        >>> s.remove(7)
        True
        >>> s
        SparseSet([3, 5])
        >>> 5 in s
        True
        >>> s.remove(5)
        True
        >>> s
        SparseSet([3])

        """
        if value not in self:
            return False

        intern_value = value - self._offset
        s = len(self)
        self._swap_positions(intern_value, self._values[s - 1])
        self._size -= 1
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
        >>> s = SparseSet([1,2,3,4,5])
        >>> s.remove_all_but(3)
        >>> s
        SparseSet([3])
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
        self._size = 1
        self._min = _v
        self._max = _v

    def remove_all(self) -> None:
        """
        >>> s = SparseSet([2, 3, 4])
        >>> len(s)
        3
        >>> s.remove_all()
        >>> s
        SparseSet([])
        """
        self._size = 0

    def remove_above(self, value: int) -> None:
        """
        >>> s = SparseSet([3, 4, 5, 6, 7])
        >>> s.remove_above(5)
        >>> s
        SparseSet([3, 4, 5])
        >>> s = SparseSet([1, 3, 5, 6, 7])
        >>> s.remove_above(5)
        >>> s
        SparseSet([1, 3, 5])
        >>> s.remove_above(0)
        >>> s
        SparseSet([])
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
        >>> s = SparseSet([3, 4, 5, 6, 7])
        >>> s.remove_below(5)
        >>> s
        SparseSet([5, 6, 7])
        >>> s = SparseSet([1, 3, 5, 6, 7])
        >>> s.remove_below(5)
        >>> s
        SparseSet([5, 6, 7])
        >>> s.remove_below(10)
        >>> s
        SparseSet([])
        """
        if value > self.max():
            self.remove_all()
        else:
            v = self.min()
            while v < value:
                self.remove(v)
                v += 1

    def _update_min(self, intern_value: int) -> None:
        if not self.is_empty() and intern_value == self._min:
            val = self._min + 1
            while not self._raw_contains(val):
                val += 1
            self._min = val

    def _update_max(self, intern_value: int) -> None:
        if not self.is_empty() and intern_value == self._max:
            val = self._max - 1
            while not self._raw_contains(val):
                val -= 1
            self._max = val

    def _raw_contains(self, value: int) -> bool:
        """
        >>> s = SparseSet([1])
        >>> s._values
        [0]
        >>> s._size
        1
        >>> s._min
        0
        >>> s._raw_contains(-1)
        False
        >>> s._raw_contains(1)
        False
        >>> s._raw_contains(0)
        True
        >>> s._size = 0
        >>> s._raw_contains(0)
        False
        """
        if value < self._min or value > self._max:
            return False
        else:
            return self._indices[value] < self._size

    def _index_of(self, value: int) -> int:
        return self._indices[value]

    def __contains__(self, value: int) -> bool:
        return self._raw_contains(value - self._offset)

    def to_list(self) -> list[int]:
        """
        >>> s = SparseSet([1, 2, 3])
        >>> s.to_list()
        [1, 2, 3]
        """
        return sorted([x + self._offset for x in self._values[: self._size]])

    def to_set(self) -> set[int]:
        """
        >>> s = SparseSet([2, 4, 6])
        >>> s.to_set() == {2, 4, 6}
        True
        """
        return set(self.to_list())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_list()})"

    def __str__(self) -> str:
        """
        >>> s = SparseSet([1, 2, 3])
        >>> str(s)
        '{1, 2, 3}'
        """
        return "{" + ", ".join(str(x) for x in self.to_list()) + "}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
