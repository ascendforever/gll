from __future__ import annotations

__all__ = [
    'TriangleF'
]

from gll.mth.__common import *
from gll.mth.__static import *
from ._abc import *

class TriangleF(TriangleABC[float]):
    __slots__ = ()
    class Triple(TriangleABC.TripleABC[float]):
        __slots__ = ()
        _type = float
    class ImmutableTriple(TriangleABC.ImmutableTripleABC[float]):
        __slots__ = ()
        _type = float
    @staticmethod
    def _degrees_acos_helper(value:float) -> float:
        return degrees(acos(value))
    @staticmethod
    def _sqrt_helper(value:float) -> float:
        return math.sqrt(value)
    @staticmethod
    def _degrees_sin_helper(angle:float) -> float:
        return sin(angle)























