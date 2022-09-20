from __future__ import annotations

__all__ = [
    'Circle',
    'Rectangle'
]

from gll.mth.__common import *
from gll.mth.__static import *

DT = t.TypeVar('DT', float, Decimal)

class Circle(t.Generic[DT], VHashable):
    """
    Circle
    `radius` should be greater than zero at all times
    [Created 2/29/20] cython // python 5/30/21
    """
    __slots__ = ('radius', '__weakref__')
    __match_args__ = ('radius', 'diameter')
    def __init__(self, /, radius:t.Optional[DT]=None):
        self.radius:t.Optional[DT] = radius
    @property
    def diameter(self, /) -> DT:
        return self.radius * 2
    @diameter.setter
    def diameter(self, /, value:DT) -> None:
        self.radius = value / 2
    @classmethod
    def from_diameter(cls, diameter:DT) -> Circle[DT]:
        self = cls()
        self.diameter = diameter
        return self
    @classmethod
    def from_circumference(cls, circumference:DT, *, pi=math.pi) -> Circle[DT]:
        self = cls()
        self.set_circumference(circumference, pi=pi)
        return self
    @classmethod
    def from_area(cls, area:DT, *, pi=math.pi, sqrt=math.sqrt) -> Circle[DT]:
        self = cls()
        self.set_area(area, pi=pi, sqrt=sqrt)
        return self
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}(radius={self.radius!r})"
    def __eq__(self, /, other:Circle[DT]) -> bool:
        if isinstance(other, self.__class__):
            return self.radius==other.radius
        raise NotImplementedError
    def __ne__(self, /, other:Circle[DT]) -> bool:
        return self.radius!=other.radius
    def __vhash__(self, /) -> int:
        return hash(self.radius)
    def circumference(self, /, *, pi=math.pi) -> DT:
        __self_radius = self.radius
        if __self_radius is None:
            raise ValueError("Cannot calculate circumference without radius")
        return __self_radius * pi * 2
    def set_circumference(self, /, value:DT, *, pi=math.pi) -> None:
        self.radius = value / (pi * 2)
    def area(self, /, pi=math.pi) -> DT:
        __self_radius = self.radius
        if __self_radius is None:
            raise ValueError("Cannot calculate area without radius")
        return __self_radius**2 * pi
    def set_area(self, /, value:DT, *, pi=math.pi, sqrt=math.sqrt) -> None:
        self.radius = sqrt(value / pi)

class Rectangle(t.Generic[DT], VHashable):
    """Rectangle
    `x` and `y` should be greater than zero at all times
    [Created 2/29/20]"""
    SIDE_COUNT:t.Final[t.Literal[4]] = 4
    ANGLES:t.Final[t.Literal[90]] = 90
    __slots__ = ('x','y', '__weakref__')
    __match_args__ = ('x','y','dimensions','perimeter','area')
    def __init__(self, /, x:t.Optional[DT]=None, y:t.Optional[DT]=None):
        self.x:t.Optional[DT] = x
        self.y:t.Optional[DT] = y
    def __repr__(self, /):
        return f"{self.__class__.__name__}(x={self.x!r}, y={self.y!r})"
    @property
    def dimensions(self, /) -> tuple[t.Optional[DT],t.Optional[DT]]:
        return (self.x, self.y) # noqa parentheses
    @dimensions.setter
    def dimensions(self, /, value:tuple[t.Optional[DT],t.Optional[DT]]) -> None:
        self.x, self.y = value
    @property
    def perimeter(self, /) -> DT:
        __self_x = self.x
        __self_y = self.y
        if __self_x is None or __self_y is None:
            raise ValueError("Cannot calculate perimeter with unknown sides")
        return (__self_x*2) + (__self_y*2)
    @property
    def area(self, /) -> DT:
        __self_x = self.x
        __self_y = self.y
        if __self_x is None or __self_y is None:
            raise ValueError("Cannot calculate area with unknown sides")
        return __self_x * __self_y
    def __vhash__(self, /):
        return hash((self.x,self.y))
    def diagonal(self, /, sqrt=math.sqrt) -> DT:
        __self_x = self.x
        __self_y = self.y
        if __self_x is None or __self_y is None:
            raise ValueError("Cannot calculate diagonal with unknown sides")
        return sqrt(__self_x**2 + __self_y**2)



