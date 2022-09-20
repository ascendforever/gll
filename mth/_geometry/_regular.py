"""
2D geometric shapes
(None refers to being unknown)
"""

from __future__ import annotations

__all__ = [
    'Square',
    'RegularPentagon',
    'RegularHexagon',
    'RegularHeptagon'
]

from gll.mth.__common import *
from gll.mth.__static import *


DT = t.TypeVar('DT')
def angles_from_sides(side_count:DT) -> DT:
    """Calculate angle values from side count"""
    return ((side_count - 2) * 180) / side_count

class RegularPolygonBase(t.Generic[DT], VHashable, metaclass=abc.ABCMeta):
    """`x` should be greater than zero at all times
    [Created 5/31/21]"""
    SIDE_COUNT:int
    ANGLES:float
    __slots__ = ('x', '__weakref__')
    __match_args__ = ('x','perimeter')
    def __init__(self, /, x:t.Optional[DT]=None):
        self.x:t.Optional[DT] = x
    @property
    @t.final
    def perimeter(self, /) -> DT:
        return self.__class__.SIDE_COUNT * self.x
    @perimeter.setter
    @t.final
    def perimeter(self, /, value:DT) -> None:
        self.x = value / self.__class__.SIDE_COUNT
    @t.final
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}(x={self.x!r})"
    @t.final
    def __vhash__(self, /):
        return hash(self.x)
    @abc.abstractmethod
    def area(self, /) -> DT:
        ...
    @abc.abstractmethod
    def set_area(self, /, value:DT, sqrt=math.sqrt) -> None:
        ...


class Square(RegularPolygonBase):
    """Square
    [Created 2/29/20] cython // python 5/30/21"""
    SIDE_COUNT:t.Final[t.Literal[4]] = 4
    ANGLES:t.Final[t.Literal[90]] = 90
    __slots__ = ()
    def area(self, /) -> DT:
        __self_x = self.x
        if __self_x is None:
            raise ValueError("Cannot calculate area with unknown sides")
        return __self_x**2
    def set_area(self, /, value:DT, *, sqrt=math.sqrt) -> None:
        self.x = sqrt(value)

class RegularPentagon(RegularPolygonBase):
    """Regular pentagon
    [Created 2/29/20] cython // python 5/30/21"""
    SIDE_COUNT:t.Final[t.Literal[5]] = 5
    ANGLES:t.Final[float] = angles_from_sides(5)
    __slots__ = ()
    # @memorized_method # too much overhead
    def area(self, /, *, sqrt=math.sqrt) -> DT:
        __self_x = self.x
        if __self_x is None:
            raise ValueError("Cannot calculate area with unknown sides")
        return sqrt(5 * (5+2*sqrt(5)) ) * (__self_x**2) / 4
    # @memorized_method # too much overhead
    def set_area(self, /, value:DT, *, sqrt=math.sqrt) -> None:
        self.x = sqrt(value / (  sqrt(5 * (2*sqrt(5) + 5)) / 4  ))

class RegularHexagon(RegularPolygonBase):
    """Regular hexagon
    [Created 2/29/20] cython // python 5/30/21"""
    SIDE_COUNT:t.Final[t.Literal[6]] = 6
    ANGLES:t.Final[float] = angles_from_sides(6)
    __slots__ = ()
    # @memorized_method # too much overhead
    def area(self, /, *, sqrt=math.sqrt) -> DT:
        __self_x = self.x
        if __self_x is None:
            raise ValueError("Cannot calculate area with unknown sides")
        return 3 * sqrt(3) * __self_x**2 / 2
    # @memorized_method # too much overhead
    def set_area(self, /, value:DT, *, sqrt=math.sqrt) -> None:
        self.x = sqrt(sqrt(3)) * sqrt( 2 * value / 9 )


class RegularHeptagon(RegularPolygonBase):
    """Regular heptagon
    [Created 3/1/20] cython // python 5/30/21"""
    SIDE_COUNT:t.Final[t.Literal[7]] = 7
    ANGLES:t.Final[float] = angles_from_sides(7)
    __slots__ = ()
    # @memorized_method # too much overhead
    def area(self, /, *, sqrt=math.sqrt, radians=math.radians, cot=cot) -> DT: # noqa shadowing
        __self_x = self.x
        if __self_x is None:
            raise ValueError("Cannot calculate area with unknown sides")
        return 7 / 4 * __self_x**2 * cot(radians(180/7))
    # @memorized_method # too much overhead
    def set_area(self, /, value:DT, *, sqrt=math.sqrt, radians=math.radians, cot=cot) -> None: # noqa shadowing
        self.x = sqrt(value / ( 7/4 * cot(radians(180/7)) ))














