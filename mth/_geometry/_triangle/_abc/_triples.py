from __future__ import annotations

__all__ = [
    'AllTripleABC',
    'TripleABC',
    'ImmutableTripleABC'
]

from gll.mth.__common import *
from gll.mth.__static import *


class AllTripleABC(t.Generic[T], abcs.Sequence[T], abcs.Sized, VHashable, metaclass=abc.ABCMeta):
    _type:t.ClassVar = ...
    __slots__ = ('a','b','c', '__weakref__')
    __match_args__ = ('a','b','c', 'known_amount', 'all_known')
    # @t.final
    def __init__(self, /, a:t.Optional[T]=None, b:t.Optional[T]=None, c:t.Optional[T]=None):
        self.a:t.Optional[T] = a
        self.b:t.Optional[T] = b
        self.c:t.Optional[T] = c
    @property
    # @functools.lru_cache(maxsize=6)
    # @memorized_method # too much overhead
    # @t.final
    def known_amount(self, /) -> t.Literal[0,1,2,3]:
        return (self.a is not None) + (self.b is not None) + (self.c is not None)
    @property
    # @functools.lru_cache(maxsize=6)
    # @memorized_method # too much overhead
    # @t.final
    def all_known(self, /) -> bool:
        return self.a is not None and self.b is not None and self.c is not None
    @classmethod
    @t.final
    def from_lenient(cls, a=None, b=None, c=None) -> AllTripleABC[T]:
        self = cls.__new__(cls)
        __self___class____type = self.__class__._type
        self.a = None if a is None else __self___class____type(a)
        self.b = None if b is None else __self___class____type(b)
        self.c = None if c is None else __self___class____type(c)
        return self
    @classmethod
    @t.final
    def from_iter(cls, it:abcs.Iterator[t.Optional[T]]) -> AllTripleABC[T]:
        next = builtins.next # noqa
        return cls(next(it), next(it), next(it))
    @classmethod
    @t.final
    def from_iterable(cls, it:abcs.Iterable[t.Optional[T]]) -> AllTripleABC[T]:
        it = iter(it)
        next = builtins.next # noqa
        return cls(next(it), next(it), next(it))
    @classmethod
    @t.final
    def from_iterable_lenient(cls, it:abcs.Iterable[t.Optional[T]]) -> AllTripleABC[T]:
        it = iter(it)
        next = builtins.next # noqa
        return cls.from_lenient(next(it), next(it), next(it))
    @classmethod
    @t.final
    def make_unknown(cls) -> AllTripleABC[T]:
        self = cls.__new__(cls)
        self.a = self.b = self.c = None
        return self
    @t.final
    def copy(self, /) -> AllTripleABC[T]:
        return self.__class__(a=self.a, b=self.b, c=self.c)
    @t.final
    def __vhash__(self, /):
        return hash((self.a,self.b,self.c))
    @t.final
    def __iter__(self, /) -> abcs.Generator[t.Optional[T], t.Any, None]:
        yield self.a
        yield self.b
        yield self.c
    @t.final
    def __contains__(self, /, item:t.Optional[T]) -> bool:
        return item==self.a or item==self.b or item==self.c
    @t.final
    def __getitem__(self, /, item:int) -> t.Optional[T]:
        return getattr(self, 'abc'[item])
    @t.final
    def __len__(self, /) -> t.Literal[3]:
        return 3
    @t.final
    def __str__(self, /):
        return f"(a={self.a!r}, b={self.b!r}, c={self.c!r})"
    @t.final
    def __repr__(self, /):
        return f"{self.__class__.__name__}(a={self.a!r}, b={self.b!r}, c={self.c!r})"

class TripleABC(t.Generic[T], AllTripleABC[T]):
    _type:t.ClassVar = ...
    __slots__ = ()
    @t.final
    def __setitem__(self, /, key:int, value:t.Optional[T]) -> None:
        setattr(self, 'abc'[key], (value if value is None else self.__class__._type(value)))
    def __init_subclass__(cls, **kwargs):
        if cls._type is ...:
            raise TypeError("Class var `_type` must be the underlying type, not \"...\"")
class ImmutableTripleABC(t.Generic[T], AllTripleABC[T]):
    _type:t.ClassVar = ...
    __slots__ = ('_known_amount','_all_known')
    def __init_subclass__(cls, **kwargs):
        if cls._type is ...:
            raise TypeError("Class var `_type` must be the underlying type, not \"...\"")
    # noinspection PyMissingConstructor
    def __init__(self, /, a:None|T=None, b:None|T=None, c:None|T=None):
        self.a:t.Final[T|None] = a
        self.b:t.Final[T|None] = b
        self.c:t.Final[T|None] = c
        ka = super().known_amount
        self._known_amount:t.Final[t.Literal[0,1,2,3]] = ka
        self._all_known:t.Final[bool] = ka==3
    @property
    def known_amount(self, /) -> t.Literal[0,1,2,3]:
        return self._known_amount
    @property
    def all_known(self, /) -> bool:
        return self._all_known
















