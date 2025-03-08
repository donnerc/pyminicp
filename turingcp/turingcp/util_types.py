from collections.abc import Callable

type Procedure = Callable[[], None]
type Predicate[T] = Callable[[T], bool]
type Supplier[T] = Callable[[], T]

