from __future__ import annotations

__all__ = [
    'VectorF2'
]

from gll.mth.__common import *
from gll.mth.__static import *
from ._abc import *

fT_num = Decimal|float
fT_it = abcs.Iterable[Decimal|float]

class VectorF2(Vector2ABC[float]):
    """Vector 2 representation using floats
    [Created 10/10/20] - cython // python 5/31/21"""
    __slots__ = ()
    _type = float
    # @staticmethod
    # def _sqrt(item:float) -> float:
    #     return math.sqrt(item)
    _sqrt = staticmethod(math.sqrt)
    # @staticmethod
    # def _sum(item:col.abc.Iterable[float]) -> float:
    #     return math.fsum(item)
    _sum = staticmethod(math.fsum)








