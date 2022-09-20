from __future__ import annotations

__all__ = [
    'WeakSeq',
]

from gll.__common import *
from gll.__static import *

Y = t.TypeVar('Y')

class WeakSeq(t.Generic[T], abcs.Collection[T]):
    __slots__ = ('_data', '__weakref__')
    __match_args__ = ('_data',)
    def __init__(self, /, iterable:t.Optional[abcs.Iterable[T]]=None):
        self._data:list[weakref.ref[T]] = [] if iterable is None else list(map(weakref.ref, iterable))
    @classmethod
    def blank(cls) -> WeakSeq[T]:
        """Factory for creation of empty instances"""
        self = cls.__new__(cls)
        self._data = []
        return self
    @classmethod
    def from_weakrefs(cls, iterable:abcs.Iterable[weakref.ref[T]]) -> WeakSeq[T]:
        self = cls.__new__(cls)
        self._data = list(iterable)
        return self
    @classmethod
    def from_any(cls, iterable:abcs.Iterable[T | weakref.ref[T]]) -> WeakSeq[T]:
        self = cls.__new__(cls)
        __weakref_ref = weakref.ref
        self._data = [(ior if isinstance(ior, __weakref_ref) else __weakref_ref(ior)) for ior in iterable]
        return self
    def refs(self) -> abcs.Iterator[weakref.ref[T]]:
        return iter(self._data)
    def objs(self) -> abcs.Generator[T, t.Any, None]:
        for ref in self._data:
            if (r:=ref()) is not None: # ref might be killed by the time this is yielded
                yield r
    def __iter__(self, /) -> abcs.Generator[T, t.Any, None]:
        return self.objs()
    def refs_reversed(self) -> abcs.Iterator[weakref.ref[T]]:
        return reversed(self._data)
    def objs_reversed(self) -> abcs.Generator[T, t.Any, None]:
        for ref in reversed(self._data):
            if (r:=ref()) is not None: # ref might be killed by the time this is yielded
                yield r
    def __reversed__(self, /) -> abcs.Generator[T, t.Any, None]:
        return self.objs_reversed()
    def __len__(self, /) -> int:
        return len(self._data)
    def __str__(self, /) -> str:
        return f"[{', '.join(repr(ref()) for ref in self._data)}]"
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}({self!s})"
    def __contains__(self, item:T | weakref.ref[T]):
        if isinstance(item, weakref.ref):
            return self.contains_ref(item)
        return self.contains(item)
    def contains(self, item:T) -> bool:
        """Check if an item is referenced"""
        for x in self._data:
            if x()==item:
                return True
        return False
    def contains_ref(self, item:weakref.ref[T]) -> bool:
        """Check if a reference is contained"""
        return item in self._data
    def append(self, /, item:T) -> None:
        self._data.append(weakref.ref(item))
    def append_ref(self, /, ref:weakref.ref[T]) -> None:
        self._data.append(ref)
    def append_any(self, /, item_or_ref:T | weakref.ref[T]) -> None:
        __weakref_ref = weakref.ref
        self._data.append(item_or_ref if isinstance(item_or_ref, __weakref_ref) else __weakref_ref(item_or_ref))
    def extend(self, /, iterable:abcs.Iterable[T]) -> None:
        self._data.extend(map(weakref.ref, iterable))
    def extend_refs(self, /, refs:abcs.Iterable[weakref.ref[T]]) -> None:
        self._data.extend(refs)
    def extend_any(self, /, mix:abcs.Iterable[T | weakref.ref[T]]) -> None:
        __weakref_ref = weakref.ref
        self._data.extend((ior if isinstance(ior, __weakref_ref) else __weakref_ref(ior)) for ior in mix)
    def copy(self, /) -> WeakSeq[T]:
        """Performs auto cleaning"""
        cls = self.__class__
        inst = cls.__new__(cls)
        self.clean()
        inst._data = self._data.copy()
        return inst
    def copies(self, /, count:int=1) -> list[WeakSeq[T]]:
        """Performs auto cleaning"""
        if count < 1: raise ValueError("`count` must be 1 or greater")
        cls = self.__class__
        __cls___new__ = cls.__new__
        # noinspection PyArgumentList
        insts:list[WeakSeq[T]] = [__cls___new__(cls) for _ in range(count)]
        self.clean()
        __self__data_copy = self._data.copy
        for inst in insts:
            inst._data = __self__data_copy()
        return insts
    def reversed_copy(self, /) -> WeakSeq[T]:
        """Performs auto cleaning"""
        cls = self.__class__
        inst = cls.__new__(cls)
        self.clean()
        inst._data = self._data.copy() # proven to be faster than using list(reversed(...))
        inst._data.reverse()
        return inst
    def reversed_copies(self, /, count:int=1) -> list[WeakSeq[T]]:
        """Performs auto cleaning"""
        if count < 1: raise ValueError("`count` must be 1 or greater")
        cls = self.__class__
        __cls___new__ = self.__class__.__new__
        # noinspection PyArgumentList
        insts:list[WeakSeq[T]] = [__cls___new__(cls) for _ in range(count)]
        first = insts[0]
        self.clean()
        first._data = self._data.copy()
        __first__data = first._data
        __first__data.reverse()
        if len(insts) > 1:
            __first__data_copy = __first__data.copy
            for inst in insts[1:]:
                inst._data = __first__data_copy()
        return insts
    def reverse(self, /) -> None:
        """Reverse in-place"""
        self._data.reverse()
    def clear(self, /) -> None:
        self._data.clear()
    def count_refs(self, /, item:weakref.ref[T]) -> int:
        """Return the number of occurrences of a reference"""
        return self._data.count(item)
    def count(self, /, item:T) -> int:
        """Return the number of occurrences of a value"""
        i = 0
        for x in self.objs():
            if x()==item:
                i += 1
        return i
    def sort_refs(self, /,       key:t.Optional[abcs.Callable[weakref.ref[T], proto.SupportsLessThan]]=None, reverse:bool=False) -> None:
        """Sort in-place; auto cleans"""
        self.clean()
        self._data.sort(key=key, reverse=reverse)
    def sort(self, /, key:t.Optional[abcs.Callable[T , proto.SupportsLessThan]]=None, reverse:bool=False) -> None:
        """Sort in-place; auto cleans; Better than `sort_refs` if `key` is predefined, but worse if `key` was just defined for this call"""
        self.clean()
        self._data.sort(key=(None if key is None else lambda ref : key(ref())), reverse=reverse)
    def clean(self, /) -> None:
        """Fast clean - does no counting"""
        data = self._data
        __data_pop = data.pop
        for i in range(len(self._data), -1, -1):
            if data[i]() is None:
                __data_pop(i)
    def clean_counting(self, /) -> int:
        """Returns the amount dead references removed"""
        __self__data = self._data
        bef = (__len:=len)(__self__data)
        self.clean()
        return bef - __len(__self__data)
