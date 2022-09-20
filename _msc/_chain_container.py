from __future__ import annotations

__all__ = [
    'ChainContainer',
    'ChainCollection'
]

from gll.__common import *
from gll.__static import *

class ChainContainer(t.Generic[T], abcs.Container[T]):
    """View of multiple containers
    Used for container lookups
    [Created 11/?/21]"""
    __slots__ = __match_args = ('data',)
    def __init__(self, *data:abcs.Container[T]):
        """Leftmost container is priority"""
        self.data:col.deque[abcs.Container[T]] = col.deque(data)
    @classmethod
    def blank(cls) -> ChainContainer:
        self = cls.__new__(cls)
        self.data = col.deque()
        return self
    @classmethod
    def from_deque(cls, deque:col.deque[abcs.Container[T]]) -> ChainContainer[T]:
        self = cls.__new__(cls)
        self.data = deque
        return self
    def new_child(self, child:abcs.Container[T]) -> None:
        self.data.appendleft(child)
    def new_parent(self, parent:abcs.Container[T]) -> None:
        self.data.append(parent)
    @t.final
    def __contains__(self, item:T) -> bool:
        for container in self.data:
            if item in container:
                return True
        return False
class ChainCollection(t.Generic[T], ChainContainer[T], abcs.Collection[T]):
    """View of multiple collections
    [Created 11/?/21]"""
    __slots__ = ()
    if t.TYPE_CHECKING:
        def __init__(self, *data:abcs.Collection[T]): # noqa
            """Leftmost collection is priority"""
            self.data:col.deque[abcs.Collection[T]] = col.deque(data)
        @classmethod
        def blank(cls) -> ChainCollection: ...
        @classmethod
        def from_deque(cls, deque:col.deque[abcs.Collection[T]]) -> ChainCollection[T]: ...
        def new_child(self, container:abcs.Collection[T]) -> None: self.data.appendleft(container)
        def new_parent(self, container:abcs.Collection[T]) -> None: self.data.append(container)
    def __iter__(self) -> abcs.Iterator[T]:
        return itertools.chain.from_iterable(self.data)
    def __len__(self) -> int:
        return sum(map(len,self.data))





