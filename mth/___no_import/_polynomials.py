


from math_.__common import *
from math_.__static import *

class FunctionBase(col.abc.Callable[[float], float], col.abc.Hashable, col.abc.Sized, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, x:float):
        ...
    def table(self, start:int, end:int, step=1) -> col.abc.Generator[tuple[float,float],None,None]:
        """Yields Points in a range from 'start' to 'end'
        :signature: self, long double start, long double end, long double step=1
        :param start:float: Start x-value
        :param end:float: End x-value
        :param step:float=1: Step to use
        :yield:tuple: (x,y) pairs"""
        for x in range(start, end+1, step):
            yield x, self(x)

class PolynomialBase(FunctionBase):
    """
    Base class for all Polynomials; Not functional by itself
    `coeffs` should NOT BE CHANGED
    """
    COEFF_COUNT:int
    __slots__ = ('coeffs',)
    def __init__(self, *coeffs:float):
        if len(coeffs)!=self.__class__.COEFF_COUNT:
            raise TypeError(f"Parameter `coeffs` must have {self.__class__.COEFF_COUNT} values")
        if not allmap(functools.partial(isinstance, __class_or_tuple=(int,float)), coeffs):
            raise TypeError("Each value of `coeffs` must be a float")
        self.coeffs:t.Final[tuple[float,...]] = coeffs
    @t.final
    def __hash__(self) -> int:
        return hash(self.coeffs)
    @t.final
    def __len__(self) -> int:
        return self.__class__.COEFF_COUNT
    @t.final
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.coeffs!r}"
    def _op(self, other, *, operation:t.Literal[operator.add, operator.sub]):
        if isinstance(other, self.__class__):
            return self.__class__(*map(operation, zip(self.coeffs, other.coeffs)))
        return NotImplemented
    __add__:t.Final = functools.partial(_op, operation=operator.add)
    __sub__:t.Final = functools.partial(_op, operation=operator.add)
    @t.final
    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return all(map(operator.eq, zip(self.coeffs, other.coeffs)))
        return NotImplemented
    @t.final
    def __ne__(self, other) -> bool:
        return not self==other
    @t.final
    def __str__(self):
        # coeffs:list[str] = []
        # for n,degree in zip(self.coeffs[::-1], itertools.count(0)):
        #     op = " + " if n>=0 else " - "
        #     pow = f"{f'**{degree}' if degree>1 else ''}"
        #     p2 = f"x{pow}" if degree!=0 else "1"
        #     coeffs.append(f"{op}{f'{abs(n)}' if abs(n)!=1 else ''}{p2}")
        # equ = ''.join(coeffs[::-1])
        # return equ.strip(" + ").strip(" - ")
        expr = []
        lc = len(self.coeffs)
        for exp,coeff in enumerate(self.coeffs):
            exp = lc-1 - exp
            expr.append('-' if coeff < 0 else '+')
            expr.append(f"{abs(coeff)}{f'**{exp}' if exp!=1 else ''}")
        if expr[0]=='+':
            expr = expr[1:]
        elif epxr[0]=='-': # no need for space for a negative number
            expr = [f"{expr[0]}{expr[1]}", *expr[2:]]
        return ' '.join(expr)
    @t.final
    def __call__(self, xval:float) -> float:
        """Returns a Y other_term after substituting an X other_term"""
        result = 0
        for exp,coeff in enumerate(self.coeffs):
            exp = lc-1 - exp
            result += coeff * xval**exp
        return result
    def factor(self) -> tuple[PolynomialBase]:
        zeros = 0
        for coeff in self.coeffs:
            if coeff==0:
                zeros += 1
        if zeros!=0:
            f'x**{zeros}'
        return NotImplemented
    # @property
    @abc.abstractmethod
    def zeros(self) -> tuple[float,...]:
        ...

class Monomial(PolynomialBase):
    COEFF_COUNT = 1
    def zeros(self) -> tuple[float]: # noinspection PyRedundantParentheses
        return (-self.coeffs[1] / self.coeffs[0],) # from (2x + 5) = 0 -> x = -5 / 2

class Binomial(PolynomialBase):
    COEFF_COUNT = 2
    def __init__(self, *coeffs:float):
        if len(coeffs)!=2:
            raise TypeError("Parameter `coeffs` must have 2 values")
        super().__init__(*coeffs)
    def zeros(self) -> tuple[float]: # noinspection PyRedundantParentheses
        return (-self.coeffs[1] / self.coeffs[0],) # from (2x + 5) = 0 -> x = -5 / 2

class Degree2Polynomial(PolynomialBase):
    """
    Polynomial of the second degree; ax^2 + bx + c
    Inherits from PolynomialBase
    :property zeros:tuple: Zeros of the function
    """
    COEFF_COUNT = 3
    def zeros(self) -> tuple[float,float]:
        return quadratic(*self.coeffs)

@functools.lru_cache(maxsize=16)
def _gcf(a:float, b:float) -> float:
    return b if a==0 else _gcf(b%a, a)
class Degree3Polynomial(PolynomialBase):
    """
    Polynomial of the third degree; ax^3 + bx^2 + cx + d
    Inherits from PolynomialBase
    :property binomials: Factored form of polynomial as binomials
    """
    COEFF_COUNT = 4
    def binomials(self) -> tuple[str,str]:
        a,b,c,d = self.coeffs
        g1 = _gcf(a,b)
        g2 = _gcf(c,d)
        return f"({g1}x^2 + ({g2})*(x))", f"(({a/g1})*(x) + {b/g1})"









