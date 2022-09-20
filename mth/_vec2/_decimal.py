from __future__ import annotations

__all__ = [
    'VectorD2'
]

from gll.mth.__common import *
from gll.mth.__static import *
from ._abc import *

dT_num = Decimal|float|str
dT_it = abcs.Iterable[Decimal|float|str]

class VectorD2(Vector2ABC[Decimal]):
    """Vector 2 representation using Decimals
    [Created 5/30/21]"""
    __slots__ = ()
    _type = Decimal
    # @staticmethod
    # def _sqrt(item:Decimal) -> Decimal:
    #     return Decimal.sqrt(item)
    _sqrt = staticmethod(Decimal.sqrt)
    # @staticmethod
    # def _sum(item:abcs.Iterable[Decimal]) -> Decimal:
    #     return sum(item) # better than math.fsum because this keeps the objects as `Decimal`s
    _sum = staticmethod(sum) # better than math.fsum because this keeps the objects as `Decimal`s
    normalize:t.Final = functools.partialmethod(Vector2ABC._apply_no_construct, Decimal.normalize)
    normalize.__doc__ = """Convert 0e0 to 0 and remove trailing zeros for x and y"""
    def fma(self, /, mult:int=1, add:int=0, decimal_context:t.Optional[decimal.Context]=None) -> None:
        """Decimal fused-multiply-add; Multiplies inplace `mult` and adds `add`"""
        __Decimal_fma = Decimal.fma
        self.x = __Decimal_fma(self.x, mult, add, context=decimal_context)
        self.y = __Decimal_fma(self.y, mult, add, context=decimal_context)


















































