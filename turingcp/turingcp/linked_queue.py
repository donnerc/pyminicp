from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class QueueADT(ABC, Generic[T]):

    @abstractmethod
    def enqueue(self, item: T) -> None:
        '''Enfile un nouvel objet dans la file'''
        pass


    @abstractmethod
    def dequeue(self) -> T:
        '''Défile le premier objet de la file'''
        pass


    @abstractmethod
    def first(self) -> T:
        '''Retourne le premier élément de la file sans le défiler'''
        pass


    @abstractmethod
    def is_empty(self) -> bool:
        '''Retourne ``True`` si la liste est vide et ``False`` sinon'''
        pass


    @abstractmethod
    def __len__(self) -> int:
        '''Retourne le nombre d'éléments de la file'''
        pass


    @abstractmethod
    def __repr__(self) -> str:
        '''Retourne la représentation interne de la file'''
        pass

class QueueException(Exception):
    pass

class EmptyQueueError(QueueException):
    pass

class QueueOverflowError(QueueException):
    pass


class LinkedQueue(QueueADT, Generic[T]):
    '''

    FIFO queue implementation using a singly linked list for storage.

    >>> q = LinkedQueue(items=[3, 4, 5])
    >>> q
    LinkedQueue(items=[3, 4, 5])
    >>> q = LinkedQueue()
    >>> q
    LinkedQueue(items=[])
    >>> q.enqueue(3)
    >>> q.enqueue(5)
    >>> q
    LinkedQueue(items=[3, 5])
    >>> len(q)
    2
    >>> for item in [7, 9, 11]: q.enqueue(item)
    >>> q
    LinkedQueue(items=[3, 5, 7, 9, 11])
    >>> q.first()
    3
    >>> q.dequeue()
    3
    >>> len(q)
    4
    >>> q
    LinkedQueue(items=[5, 7, 9, 11])
    >>> for _ in range(4): q.dequeue()
    5
    7
    9
    11
    >>> q
    LinkedQueue(items=[])
    >>> q.dequeue()
    Traceback (most recent call last):
    ...
    EmptyQueueError: Cannot dequeue from empty queue
    >>> q.first()
    Traceback (most recent call last):
    ...
    EmptyQueueError: Cannot get first element from empty queue
    >>> for n in range(2): q.enqueue(n)
    >>> q
    LinkedQueue(items=[0, 1])
    >>> q.is_empty()
    False
    >>> for _ in range(2): q.dequeue()
    0
    1
    >>> q
    LinkedQueue(items=[])
    >>> q.is_empty()
    True

    '''


    #-------------------------- nested Node class --------------------------
    class _Node(Generic[T]):
        '''Lightweight, nonpublic class for storing a singly linked node.'''

        __slots__ = '_element' , '_next' # streamline memory usage

        def __init__(self, element: T, next: '_Node') -> None:
            self._element = element
            self._next = next

        def __repr__(self) -> str:
            return f'_Node(element={self._element}, next={self._next})'

    #------------------------------- stack methods -------------------------------
    def __init__(self, items: list[T] | None = None) -> None:
        self.from_list(items or [])

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def first(self) -> T:
        if self.is_empty():
            raise EmptyQueueError("Cannot get first element from empty queue")

        return self._head._element

    def enqueue(self, item: T) -> None:
        new_node = self._Node(item, None)

        if self.is_empty():
            self._head = new_node
        else:
            self._tail._next = new_node

        self._tail = new_node
        self._size += 1

    def dequeue(self) -> T:
        if self.is_empty():
            raise EmptyQueueError("Cannot dequeue from empty queue")

        node = self._head

        second_node = node._next
        self._head = second_node

        if self._size == 1:
            self._tail = None

        self._size -= 1

        return node._element

    def to_list(self) -> list[T]:
        result = [None] * self._size
        current_node = self._head

        for i in range(self._size):
            result[i] = current_node._element
            current_node = current_node._next

        return result

    def _reset(self) -> None:
        self._head = None # reference to the head node
        self._tail = None # reference to the tail node
        self._size = 0 # number of queue elements


    def from_list(self, items: list[T]) -> None:
        self._reset()
        for item in items:
            self.enqueue(item)


    def __repr__(self) -> str:
        return f'LinkedQueue(items={self.to_list()})'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
