

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from collections.abc import Iterable

T = TypeVar('T')

class StackADT(ABC, Generic[T]):

    @abstractmethod
    def push(self, item: T) -> None:
        pass


    @abstractmethod
    def pop(self) -> T:
        pass


    @abstractmethod
    def peek(self) -> T:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

class StackException(Exception):
    pass

class EmptyStackError(StackException):
    pass


class ListStack(StackADT[T], Generic[T]):
    '''

    ``ListStack`` implements a stack by using a list as the container.

    >>> s: ListStack[int] = ListStack()
    >>> s.push(1)
    >>> s
    ListStack([1])
    >>> s.push(2)
    >>> s
    ListStack([1, 2])
    >>> s.push(3)
    >>> s
    ListStack([1, 2, 3])
    >>> s.peek()
    3
    >>> s.pop()
    3
    >>> s
    ListStack([1, 2])
    >>> s.pop()
    2
    >>> s.pop()
    1
    >>> s
    ListStack([])
    
    >>> s: ListStack[int] = ListStack([1,2,3])
    >>> [item for item in s]
    [1, 2, 3]
    '''

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._items = list(items) if items is not None else []
        self._iter_position = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._items})'

    def __len__(self) -> int:
        return len(self._items)

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        try:
            return self._items.pop()
        except IndexError as e:
            raise EmptyStackError('Pop from an empty stack') from e

    def peek(self) -> T:
        try:
            return self._items[-1]
        except IndexError as e:
            raise EmptyStackError('Peek an empty stack') from e

    def is_empty(self) -> bool:
        return len(self) == 0
    
    def __iter__(self):
        self._iter_position = 0
        return self
    
    def __next__(self):
        if self._iter_position < len(self):
            item: T = self._items[self._iter_position]
            self._iter_position += 1
            return item

        raise StopIteration
            
    

class Stack(StackADT[T], Generic[T]):
    '''

    ``Stack`` implements a stack by using a list as the container.

    >>> s: Stack[int] = Stack()
    >>> s.push(1)
    >>> s
    Stack([1])
    >>> s.push(2)
    >>> s
    Stack([1, 2])
    >>> s.push(3)
    >>> s
    Stack([1, 2, 3])
    >>> len(s)
    3
    >>> s.peek()
    3
    >>> s.pop()
    3
    >>> s
    Stack([1, 2])
    >>> s.pop()
    2
    >>> s.pop()
    1
    >>> s
    Stack([])
    >>> s.pop()
    Traceback (most recent call last):
        ...
    EmptyStackError: Pop from an empty stack
    >>> s.peek()
    Traceback (most recent call last):
        ...
    EmptyStackError: Peek an empty stack

    
    # Iterator protocol and stack initialization
    >>> s: Stack[int] = Stack([1,2,3])
    >>> [item for item in s]
    [1, 2, 3]

    '''

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._items: list[T] = list(items) if items is not None else []
        self._iter_position = 0

        # initially _item size is the real size
        self._real_size = len(self._items)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._items[:self._real_size]})'

    def __len__(self) -> int:
        return self._real_size

    def push(self, item: T) -> None:
        if self._real_size < len(self._items):
            self._items[self._real_size] = item
        else:
            self._items.append(item)
        self._real_size += 1

    def pop(self) -> T:
        if self._real_size == 0:
            raise EmptyStackError('Pop from an empty stack')

        item = self._items[self._real_size - 1]
        self._real_size -= 1
        return item

    def peek(self) -> T:
        if self._real_size == 0:
            raise EmptyStackError('Peek an empty stack')
        return self._items[self._real_size - 1]

    def is_empty(self) -> bool:
        return len(self) == 0

    def resize(self, new_size: int) -> None:
        '''
        >>> s = Stack([1,2,3,4])
        >>> len(s)
        4
        >>> s.resize(2)
        >>> s
        Stack([1, 2])
        >>> s.resize(4)
        >>> s
        Stack([1, 2, 3, 4])
        >>> s.resize(6)
        Traceback (most recent call last):
          ...
        StackException: Cannot resize above underlying collection size
        
        '''
        if new_size <= len(self._items):
            self._real_size = new_size
            return 
        else:
            raise StackException("Cannot resize above underlying collection size")
            
    
    def __iter__(self):
        self._iter_position = 0
        return self
    
    def __next__(self):
        if self._iter_position < self._real_size:
            item: T = self._items[self._iter_position]
            self._iter_position += 1
            return item

        raise StopIteration
    
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()