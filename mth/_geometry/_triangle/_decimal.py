from __future__ import annotations

__all__ = [
    'TriangleD'
]

from gll.mth.__common import *
from gll.mth.__static import *
from ._abc import *

class TriangleD(TriangleABC[Decimal]):
    __slots__ = ()
    class Triple(TriangleABC.TripleABC[Decimal]):
        __slots__ = ()
        _type = Decimal
    class ImmutableTriple(TriangleABC.ImmutableTripleABC[Decimal]):
        __slots__ = ()
        _type = Decimal
    def __init__(self, /, a:t.Optional[Decimal]=None, b:t.Optional[Decimal]=None, c:t.Optional[Decimal]=None,
                       A:t.Optional[Decimal]=None, B:t.Optional[Decimal]=None, C:t.Optional[Decimal]=None):
        super().__init__(a,b,c,A,B,C)
        warnings.warn('decimal.Decimal precision will not be retained due to there being no trigonometric functions for decimal.Decimal')
    @staticmethod
    def _degrees_acos_helper(value:Decimal) -> Decimal:
        return Decimal(degrees(acos(value)))
    @staticmethod
    def _sqrt_helper(value:Decimal) -> Decimal:
        return Decimal.sqrt(value)
    @staticmethod
    def _degrees_sin_helper(angle:Decimal) -> Decimal:
        return Decimal(sin(angle))






















