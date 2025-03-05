from typing import Generic, TypeVar
from collections.abc import Iterable

from stack import StackADT, StackException, EmptyStackError
from state_types import StateManager, StateInt
from state import CopyStateManager

T = TypeVar('T')

class StateStack(StackADT[T], Generic[T]):
    '''

    ``StateStack`` is a restorable stack that can be restored in O(1) time.

    >>> sm = CopyStateManager()
    >>> s: StateStack[int] = StateStack(sm)
    >>> s.push(1)
    >>> s
    StateStack([1])
    >>> s.push(2)
    >>> s
    StateStack([1, 2])
    >>> s.push(3)
    >>> s
    StateStack([1, 2, 3])
    >>> len(s)
    3
    >>> s.peek()
    3
    >>> s.pop()
    3
    >>> s
    StateStack([1, 2])
    >>> s.pop()
    2
    >>> s.pop()
    1
    >>> s
    StateStack([])
    >>> s.pop()
    Traceback (most recent call last):
        ...
    stack.EmptyStackError: Pop from an empty stack
    >>> s.peek()
    Traceback (most recent call last):
        ...
    stack.EmptyStackError: Peek an empty stack

    
    # Iterator protocol and stack initialization
    >>> sm = CopyStateManager()
    >>> s: StateStack[int] = StateStack(sm, [1,2,3])
    >>> [item for item in s]
    [1, 2, 3]

    '''

    def __init__(self, sm: StateManager, items: Iterable[T] | None = None) -> None:
        self._items: list[T] = list(items) if items is not None else []
        self._iter_position = 0

        # initially _item size is the real size
        self._real_size: StateInt = sm.make_state_int(len(self._items))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._items[:self._real_size.value()]})'

    def __len__(self) -> int:
        return self._real_size.value()

    def push(self, item: T) -> None:
        if self._real_size.value() < len(self._items):
            self._items[self._real_size.value()] = item
        else:
            self._items.append(item)
        self._real_size.increment()

    def pop(self) -> T:
        if self._real_size.value() == 0:
            raise EmptyStackError('Pop from an empty stack')

        item = self._items[self._real_size.value() - 1]
        self._real_size.decrement()
        return item

    def peek(self) -> T:
        if self._real_size.value() == 0:
            raise EmptyStackError('Peek an empty stack')
        return self._items[self._real_size.value() - 1]

    def is_empty(self) -> bool:
        return len(self) == 0

    def resize(self, new_size: int) -> None:
        '''
        >>> sm = CopyStateManager()
        >>> s = StateStack(sm, [1,2,3,4])
        >>> len(s)
        4
        >>> s.resize(2)
        >>> s
        StateStack([1, 2])
        >>> s.resize(4)
        >>> s
        StateStack([1, 2, 3, 4])
        >>> s.resize(6)
        Traceback (most recent call last):
          ...
        stack.StackException: Cannot resize above underlying collection size
        
        '''
        if new_size <= len(self._items):
            self._real_size.set_value(new_size)
            return 
        else:
            raise StackException("Cannot resize above underlying collection size")
            
    
    def __iter__(self):
        self._iter_position = 0
        return self
    
    def __next__(self):
        if self._iter_position < self._real_size.value():
            item: T = self._items[self._iter_position]
            self._iter_position += 1
            return item

        raise StopIteration
    
    
def test_restore():
    '''
    >>> sm = CopyStateManager()
    >>> s = StateStack(sm, [4, 6, 8])
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3)])])
    >>> s.pop()
    8
    >>> s
    StateStack([4, 6])
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3)]), Backup([CopyStateEntry(2)])])
    >>> s.pop()
    6
    >>> sm.save_state()
    Stack([Backup([CopyStateEntry(3)]), Backup([CopyStateEntry(2)]), Backup([CopyStateEntry(1)])])
    >>> s.pop()
    4
    >>> s
    StateStack([])
    >>> sm.restore_state()
    >>> s
    StateStack([4])
    >>> sm.restore_state()
    >>> s
    StateStack([4, 6])
    >>> sm.restore_state()
    >>> s
    StateStack([4, 6, 8])
    '''


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
