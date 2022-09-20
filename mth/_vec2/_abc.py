from __future__ import annotations

__all__ = [
    'Vector2ABC'
]

from gll.mth.__common import *
from gll.mth.__static import *

__T = t.TypeVar('__T')
class Vector2ABC(t.Generic[__T], abcs.Mapping[t.Literal[0,1,'x','y'], __T], abcs.Sequence[__T], abcs.Sized, VHashable):
    """
    Vector class ABC
    Should not receive extra instance attributes
    Subclassing should be done in this manner, where TYPE is the underlying numeric type (supports numeric operations with other instances and integers
        class VectorD2(Vector2ABC[TYPE]):
            __slots__ = Vector2ABC.__slots__
            _type = TYPE
            @staticmethod
            def _sqrt(item:TYPE):
                return SQUARE_ROOT_FUNCTION(item)
            @staticmethod
            def _sum(item:abcs.Iterable[TYPE]) -> TYPE:
                return SUM_FUNCTION(item)
    """
    _type:t.ClassVar
    @staticmethod
    @abc.abstractmethod
    def _sqrt(item:__T, /) -> __T:
        ...
    @staticmethod
    @abc.abstractmethod
    def _sum(item:abcs.Iterable[__T], /) -> __T:
        ...
    __slots__    = ('x','y', '__weakref__')
    __match_args__=('x','y')
    def __init__(self, /, x, y):
        __self___class____type = self.__class__._type
        self.x:__T = __self___class____type(x)
        self.y:__T = __self___class____type(y)
    @classmethod
    @t.final
    def from_exacts(cls, x:__T=0, y:__T=0) -> Vector2ABC[__T]:
        """Faster than standard instantiation"""
        self = cls.__new__(cls)
        self.x = x
        self.y = y
        return self
    @classmethod
    @t.final
    def from_iter(cls, it:abcs.Iterable) -> Vector2ABC[__T]:
        self = cls.__new__(cls)
        it = iter(it)
        __cls__type = cls._type
        self.x = __cls__type(next(it))
        self.y = __cls__type(next(it))
        return self
    @classmethod
    @t.final
    def from_single_value(cls, value) -> Vector2ABC[__T]:
        """Faster than standard instantiation"""
        self = cls.__new__(cls)
        # noinspection PyProtectedMember
        self.x = self.y = cls._type(value)
        return self
    @classmethod
    @t.final
    def from_exact(cls, value:__T) -> Vector2ABC[__T]:
        """Faster than `from_single_value` if `value` is already the correct type"""
        self = cls.__new__(cls)
        self.x = self.y = value
        return self
    @classmethod
    @t.final
    def origin(cls) -> Vector2ABC[__T]:
        """Faster (slightly) than `from_single_value` and `from_exact`"""
        self = cls.__new__(cls)
        self.x = self.y = cls._type('0')
        return self
    @t.final
    def __str__(self, /) -> str:
        return repr(self)
    @t.final
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}(x={self.x!r}, y={self.y!r})"
    @t.final
    def __vhash__(self, /) -> int:
        return hash(self.as_tuple())
    @t.final
    def __bool__(self, /) -> bool:
        return True
    @t.final
    def __format__(self, /, format_spec:str) -> str:
        return format_spec.replace('%t', self.__class__.__name__).replace('%x', self.x).replace('%y', self.y)
    @t.final
    def __iter__(self, /) -> abcs.Generator[__T, t.Any, None]:
        yield self.x
        yield self.y
    @t.final
    def __reversed__(self, /) -> abcs.Generator[__T, t.Any, None]:
        yield self.y
        yield self.x
    @t.final
    def __contains__(self, /, item) -> bool:
        return item==self.x or item==self.y
    @t.final
    def as_tuple(self, /) -> tuple[__T,__T]:
        return self.x,self.y
    @t.final
    def as_tuple_reversed(self, /) -> tuple[__T,__T]:
        return self.y,self.x
    @t.final
    def __len__(self, /) -> t.Literal[2]:
        return 2
    __x_index:t.Final[frozenset[t.Literal[0,'x']]] = frozenset((0,'x'))
    __y_index:t.Final[frozenset[t.Literal[0,'y']]] = frozenset((0,'y'))
    @t.final
    def __getitem__(self, /, index:t.Literal[0,1,'x','y']) -> __T:
        """Getting items from index; Faster to use the attributes `x` and `y`"""
        _self___class__ = self.__class__
        if index in _self___class__.__x_index:
            return self.x
        if index in _self___class__.__y_index:
            return self.y
        raise KeyError(f'Invalid index: {index!r}')
    @t.final
    def set_exact(self, /, index:t.Literal[0,1,'x','y'], value:__T) -> None:
        """Setting items from index; Faster to use the attributes `x` and `y`; Faster than `__setitem__` if `value` is already a `Decimal`"""
        _self___class__ = self.__class__
        if index in _self___class__.__x_index:
            self.x = value
        if index in _self___class__.__y_index:
            self.y = value
        raise KeyError(f'Invalid index: {index!r}')
    @t.final
    def __setitem__(self, /, index:t.Literal[0,1,'x','y'], value) -> None:
        """Setting items from index; Will convert to the necessary types; Faster to use the attributes `x` and `y` or `set_exact`"""
        self.set_exact(index, self.__class__._type(value))

    @t.final
    def __eq__(self, /, other:Vector2ABC[__T]) -> bool:
        if isinstance(other, self.__class__):
            return self.x==other.x and self.y==other.y
        return NotImplemented
    @t.final
    def __ne__(self, /, other:Vector2ABC[__T]) -> bool:
        if isinstance(other, self.__class__):
            return self.x!=other.x or self.y!=other.y
        return NotImplemented

    @t.final
    def __add__(self, /, other:Vector2ABC[__T]) -> Vector2ABC[__T]:
        __self___class__ = self.__class__
        if isinstance(other, __self___class__):
            return __self___class__.from_exacts(x=(self.x + other.x), y=(self.y + other.y))
        return NotImplemented
    @t.final
    def __iadd__(self, /, other:Vector2ABC[__T]) -> None:
        self.x += other.x
        self.y += other.y
    @t.final
    def translate(self, /, other:Vector2ABC[__T]) -> Vector2ABC[__T]:
        """Same as __add__"""
        return self.__add__(other) # this is because its literally the same
    @t.final
    def itranslate(self, /, other:Vector2ABC[__T]) -> None:
        """Same as __iadd__"""
        self.__iadd__(other) # this is because its literally the same

    @t.final
    def __sub__(self, /, other:Vector2ABC[__T]) -> Vector2ABC[__T]:
        __self___class__ = self.__class__
        if isinstance(other, __self___class__):
            return __self___class__.from_exacts(x=(self.x - other.x), y=(self.y - other.y))
        return NotImplemented
    @t.final
    def __isub__(self, /, other:Vector2ABC[__T]) -> None:
        self.x -= other.x
        self.y -= other.y
    @t.overload
    def __mul__(self, /, other:Vector2ABC[__T]) -> __T:
        ...
    @t.overload
    def __mul__(self, /, other:__T) -> Vector2ABC[__T]:
        ...
    @t.final
    def __mul__(self, /, other:Vector2ABC[__T] | __T):
        """Will find the dot product if `other` is the same class, else will multiply self.x and self.y by other.x and other.y"""
        if isinstance(other, self.__class__):
            return self.x*other.x + self.y*other.y
        return self.scale(other)
    @t.final
    def __imul__(self, /, other:__T) -> None:
        self.x *= other
        self.y *= other
    @t.final
    def scale(self, /, magnitude:__T=1) -> Vector2ABC[__T]:
        return self.__class__.from_exacts(self.x*magnitude, self.y*magnitude)
    @t.final
    def iscale(self, /, magnitude:__T=1) -> None:
        self.__imul__(magnitude)

    @t.final
    def __truediv__(self, /, other:__T) -> Vector2ABC[__T]:
        return self.__class__.from_exacts(self.x/other, self.y/other)
    @t.final
    def __itruediv__(self, /, other:__T) -> None:
        self.x /= other
        self.y /= other
    @t.final
    def invscale(self, /, magnitude:__T=1) -> Vector2ABC[__T]:
        return self.__truediv__(magnitude)
    @t.final
    def iinvscale(self, /, magnitude:__T=1) -> None:
        self.__itruediv__(magnitude)
    @t.final
    def __floordiv__(self, /, other:__T) -> Vector2ABC[__T]:
        return self.__class__.from_exacts(self.x//other, self.y//other)
    @t.final
    def __ifloordiv__(self, /, other:__T) -> None:
        self.x //= other
        self.y //= other
    @t.final
    def invscale_floor(self, /, magnitude:__T=1) -> Vector2ABC[__T]:
        return self.__floordiv__(magnitude)
    @t.final
    def iinvscale_floor(self, /, magnitude:__T=1) -> None:
        self.__ifloordiv__(magnitude)

    @functools.lru_cache(maxsize=4)
    @t.final
    def all_close(self, /, *others:Vector2ABC[__T], rel_tol:float=-1e-09, abs_tol:float=0.0) -> bool:
        """Whether x and y of each instance are considered `math.isclose`"""
        __functools_partial = functools.partial
        __math_isclose = math.isclose
        return all(itertools.chain( # this (all(itertools.chain(...)) takes the same amount of time as doing `all(...) and all(...)`
            map(__functools_partial(__math_isclose, self.x, rel_tol=rel_tol, abs_tol=abs_tol), ((other.x for other in others))),
            map(__functools_partial(__math_isclose, self.y, rel_tol=rel_tol, abs_tol=abs_tol), ((other.y for other in others)))
        ))
    @functools.lru_cache(maxsize=4)
    @t.final
    def all_equal(self, /, *others:Vector2ABC[__T]) -> bool:
        __self_x = self.x
        __self_y = self.y
        return all(itertools.chain((__self_x==other.x for other in others),
                                   (__self_y==other.y for other in others)))
    @t.final
    def rotate(self, /, degrees:t.Literal[90,180,270], direction:t.Literal['clockwise','counter','counterclockwise']) -> None: # noqa shadowing
        """Prioritize using designated functions if degrees and direction is already known"""
        if degrees==180:
            self.x = -self.x
            self.y = -self.y
        else:
            clockwise:bool = direction=='clockwise'
            counter:bool = not clockwise
            if degrees==90 and clockwise or degrees==270 and counter:
                self.x,self.y = self.y, -self.x
            elif degrees==270 and clockwise or degrees==90 and counter:
                self.x,self.y = -self.y,self.x
    @t.final
    def reflect_over_y_equals_x(self, /) -> None:
        self.x,self.y = self.y,self.x
    @t.final
    def reflect_over_x_axis(self, /) -> None:
        self.y = -self.y
    @t.final
    def reflect_over_y_axis(self, /) -> None:
        self.x = -self.x
    @t.final
    def rotate90(self, /) -> None:
        self.x,self.y = self.y, -self.x
    rotate270counter:t.Final = rotate90
    @t.final
    def rotate270(self, /) -> None:
        self.x,self.y = -self.y,self.x
    rotate90counter:t.Final = rotate270
    @t.final
    def rotate180(self, /) -> None:
        self.x = -self.x
        self.y = -self.y
    @t.final
    def _apply(self, /, func:abcs.Callable[...,t.Any]) -> None:
        self___class____type = self.__class__._type
        self.x = self___class____type(func(self.x))
        self.y = self___class____type(func(self.y))
    @t.final
    def _apply_no_construct(self, /, func:abcs.Callable[...,__T]) -> None:
        self.x = func(self.x)
        self.y = func(self.y)
    ceil:t.Final  = functools.partial(_apply, func=math.ceil)
    floor:t.Final = functools.partial(_apply, func=math.floor)
    int:t.Final   = functools.partial(_apply, func=int)
    trunc:t.Final = functools.partial(_apply, func=math.trunc)
    absolute:t.Final = functools.partial(_apply_no_construct, func=abs) # Decimal.copy_abs)
    @t.final
    def round(self, /, ndigits:t.Optional[int]=None) -> Vector2ABC[__T]:
        """Round x and y to `ndigits`"""
        self___class____type = self.__class__._type
        return self.__class__.from_exacts(self___class____type(round(self.x, ndigits=ndigits)),
                                          self___class____type(round(self.y, ndigits=ndigits)))
    @t.final
    def iround(self, /, ndigits:t.Optional[int]=None) -> None:
        """Round x and y to `ndigits`"""
        self___class____type = self.__class__._type
        self.x = self___class____type(round(self.x, ndigits=ndigits))
        self.y = self___class____type(round(self.y, ndigits=ndigits))
    @t.final
    def dot(self, /, *others:Vector2ABC[__T]) -> __T:
        """Find then dot product between this instance and others"""
        __self_x = self.x
        __self_y = self.y
        return self.__class__._sum(itertools.chain((__self_x * other.x for other in others), (__self_y * other.y for other in others)))
    @t.final
    def distance(self, /, other:Vector2ABC[__T]) -> __T:
        """Find the distance between this instance and another"""
        __self_x = self.x
        __self_y = self.y
        return self.__class__._sqrt((__self_x - other.x) ** 2 + (__self_y - other.y) ** 2)
    @t.final
    def midpoint(self, /, other:Vector2ABC[__T]) -> Vector2ABC[__T]:
        """Find the midpoint between this instance and another"""
        __self_x = self.x
        __self_y = self.y
        return self.__class__.from_exacts((__self_x + other.x) / 2, (__self_y + other.y) / 2)
    @t.final
    def imidpoint(self, /, other:Vector2ABC[__T]) -> None:
        """Set self to the midpoint between this instance and another"""
        self.x = (self.x + other.x) / 2
        self.y = (self.y + other.y) / 2
    @t.final
    def slope(self, /, other:Vector2ABC[__T]) -> __T:
        """Find the slope of a hypothetical line between this instance and another"""
        return (other.y-self.y)/(other.x-self.x)
    @t.final
    def copy(self, /) -> Vector2ABC[__T]:
        return self.__class__.from_exacts(x=self.x, y=self.y)
    @t.final
    def copies(self, /, count:int=1) -> abcs.Generator[Vector2ABC[__T], t.Any, None]:
        __self_x = self.x
        __self_y = self.y
        __self___class___from_exacts = self.__class__.from_exacts
        for _ in range(count):
            yield __self___class___from_exacts(x=__self_x, y=__self_y)











