from __future__ import annotations

__all__ = [
    'TriangleABC',
]

from gll.mth.__common import *
from gll.mth.__static import *

from ._triples import TripleABC,ImmutableTripleABC


# noinspection PyPep8Naming
class TriangleABC(t.Generic[T], VHashable, metaclass=abc.ABCMeta):
    r"""
    Triangle
        <C          a,b,c are sides
      a / \ b       A,B,C are angles
       /___\        Note: all sides are opposite their same-named angles
     <B  c  <A
    Needs to be subclassed
    All subclasses need to implement the helper methods
        This is because sub-classes use their own numeric data types
        and thus trigonometric functions and square-roots need to be implemented
        for the specific data type
    Subclasses should be built like this: // `TYPE` must be an actual type that can be instantiated
        class MyTriangle(TriangleABC[TYPE]):
            __slots__ = TriangleABC.__slots__
            class Triple(TriangleABC.TripleABC[float]):
                type = float
                __slots__ = TriangleABC.TripleABC
            class ImmutableTriple(TriangleABC.ImmutableTripleABC[float]):
                type = float
                __slots__ = TriangleABC.ImmutableTripleABC
            @staticmethod
            def _degrees_acos_helper(value:TYPE) -> TYPE:
                return ????? # Must return the acos of `value` in DEGREES
            @staticmethod
            def _sqrt_helper(value:TYPE) -> TYPE:
                return ????? # Must return the square root of `value`
            @staticmethod
            def _degrees_sin_helper(angle:TYPE) -> TYPE:
                return ????? # Must return the sin of `value` (`value` is in DEGREES)
    [Created 2/29/20] cython // python 5/30/21 mass improvement
    """
    TripleABC:t.Final = TripleABC
    ImmutableTripleABC:t.Final = ImmutableTripleABC
    Triple:t.ClassVar
    ImmutableTriple:t.ClassVar
    __slots__    = ('__abc', '__ABC', '__weakref__')
    __match_args__=('__abc', '__ABC', 'abc_view', 'ABC_view', 'all_sides_known', 'all_angles_known', 'known_angles', 'known_sides', 'solved', 'is_right', 'is_isosceles', 'is_equilateral', 'perimeter', 'can_find_area', 'area')
    def __init__(self, /, a:t.Optional[T]=None, b:t.Optional[T]=None, c:t.Optional[T]=None,
                      A:t.Optional[T]=None, B:t.Optional[T]=None, C:t.Optional[T]=None):
        __self___class___Triple = self.__class__.Triple
        self.__abc:TripleABC[T] = __self___class___Triple(a=a,b=b,c=c)
        self.__ABC:TripleABC[T] = __self___class___Triple(a=A,b=B,c=C)
    # @staticmethod
    # @t.final
    # def __getter_check(cached:ImmutableTriple, actual:Triple) -> bool:
    #     return cached is None or cached.a!=actual.a or cached.b!=actual.b or cached.c!=actual.c
    @property
    @functools.lru_cache(maxsize=10)
    @t.final
    def abc_view(self, /) -> ImmutableTriple:
        __self___abc = self.__abc
        return self.__class__.ImmutableTriple(__self___abc.a, __self___abc.b, __self___abc.c)
    @property
    @functools.lru_cache(maxsize=10)
    @t.final
    def ABC_view(self, /) -> ImmutableTriple:
        __self___ABC = self.__ABC
        return self.__class__.ImmutableTriple(__self___ABC.a, __self___ABC.b, __self___ABC.c)
    @t.final
    def __setter_common(self, /, value:Triple|ImmutableTriple) -> Triple:
        __self___class___Triple = self.__class__.Triple
        return value if isinstance(value, __self___class___Triple) else __self___class___Triple.from_iterable(value)
    @abc_view.setter
    @t.final
    def abc_view(self, /, value:Triple|ImmutableTriple) -> None:
        self.validate_sides(value)
        self.__abc = self.__setter_common(value)
    @ABC_view.setter
    @t.final
    def ABC_view(self, /, value:Triple|ImmutableTriple) -> None:
        self.validate_angles(value)
        self.__ABC = self.__setter_common(value)
    @property
    @t.final
    def all_sides_known(self, /) -> bool:
        return self.__abc.all_known # already cached
    @property
    @t.final
    def all_angles_known(self, /) -> bool:
        return self.__ABC.all_known # already cached
    @property
    @t.final
    def known_angles(self, /) -> t.Literal[0,1,2,3]:
        return self.__ABC.known_amount # already cached
    @property
    @t.final
    def known_sides(self, /) -> t.Literal[0,1,2,3]:
        return self.__abc.known_amount # already cached
    @property
    @t.final
    def solved(self, /) -> bool:
        return self.__abc.all_known and self.__ABC.all_known
    @property
    @functools.lru_cache(maxsize=16)
    # @memorized_method
    @t.final
    def is_right(self, /) -> bool:
        """Determine whether or not the triangle is a right triangle"""
        ABC = self.__ABC
        if ABC.a==90 or ABC.b==90 or ABC.c==90:
            return True
        if self.all_sides_known:
            __self___abc = self.__abc
            if __self___abc.a**2 + __self___abc.b**2 == __self___abc.c**2:
                return True
        return False
    @property
    @functools.lru_cache(maxsize=8)
    # @memorized_method
    @t.final
    def is_isosceles(self, /) -> bool:
        """Determine whether or not the triangle is an isosceles triangle"""
        __self___abc = self.__abc
        if __self___abc.known_amount in (2,3) and any(itertools.starmap(operator.eq, ((__self___abc[i],__self___abc[j]) for i,j in self._pairs_i()))):
            return True
        __self___ABC = self.__ABC
        return __self___ABC.known_amount in (2,3) and any(itertools.starmap(operator.eq, ((__self___ABC[i],__self___ABC[j]) for i,j in self._pairs_i())))
    @property
    @functools.lru_cache(maxsize=8)
    # @memorized_method # too much overhead
    @t.final
    def is_equilateral(self, /) -> bool:
        """Determine whether or not the triangle is an equilateral triangle"""
        __self___abc = self.__abc
        if __self___abc.a is not None and __self___abc.a==__self___abc.b==__self___abc.c:
            return True
        __self___ABC = self.__ABC
        return __self___ABC.a is not None and __self___ABC.a==__self___ABC.b==__self___ABC.c
    can_find_perimeter:t.Final = all_sides_known
    @property
    # @functools.lru_cache(maxsize=16)
    # @memorized_method # too much overhead
    @t.final
    def perimeter(self, /) -> T:
        """Calculates perimeter and saves the value; If the triangle hasn't changed and this is asked again, will return the same value; If the triangle changes, it will recalculate when property is retrieved"""
        if not self.can_find_perimeter:
            raise ValueError("Cannot calculate perimeter of triangle in which all sides are not known")
        return sum(self.__abc)
    @property
    @functools.lru_cache(maxsize=16)
    # @memorized_method
    @t.final
    def can_find_area(self, /) -> T:
        """Check for whether or not area can be found"""
        if self.all_sides_known:
            return True
        a,b,c = self.__abc
        # noinspection PyPep8Naming
        A,B,C = self.__ABC
        return not anynone((a,C,b)) or not anynone((b,A,c)) or not anynone((c,B,a))

    @staticmethod
    @abc.abstractmethod
    def _degrees_sin_helper(angle:T) -> T:
        """Should return the value of `sin(angle)`; argument `angle` is in degrees"""
    @property
    @functools.lru_cache(maxsize=32)
    # @memorized_method
    @t.final
    def area(self, /) -> T:
        """Calculates area and saves the value; If the triangle hasn't changed and this is asked again, will return the same value; If the triangle changes, it will recalculate when property is retrieved"""
        a,b,c = self.__abc
        # Heron's formula - all sides known
        if self.all_sides_known:
            s = self.perimeter / 2
            return (s * (s-a) * (s-b) * (s-c)) ** (1/2)
        # sin method - two sides known and angle in between
        # noinspection PyPep8Naming
        A,B,C = self.__ABC
        for s1,angle,s2 in ( (a,C,b) , (b,A,c) , (c,B,a) ):
            if s1 is not None and angle is not None and s2 is not None:
                return s1 * s2 * self._degrees_sin_helper(angle) / 2
        raise ValueError('Not enough information to determine area')


    @classmethod
    @t.final
    def alt_init(cls, abc:t.Optional[t.Iterable[t.Optional[T]]]=None, ABC:t.Optional[t.Iterable[t.Optional[T]]]=None) -> TriangleABC[T]: # noqa shadowing
        """Alternate instantiation"""
        self = cls.__new__(cls)
        __self___class___Triple = self.__class__.Triple
        __self___class___Triple_make_unknown = self.__class__.Triple.make_unknown
        __self___class___Triple_from_iterable = self.__class__.Triple.from_iterable
        self.__abc = __self___class___Triple_make_unknown() if abc is None else __self___class___Triple_from_iterable(abc)
        self.__ABC = __self___class___Triple_make_unknown() if ABC is None else __self___class___Triple_from_iterable(ABC)
        return self
    @classmethod
    @t.final
    def make_unknown(cls) -> TriangleABC[T]:
        """Factory for an empty Triangle; slightly faster than normal instantiation"""
        self = cls.__new__(cls)
        __self___class___Triple_make_unknown = self.__class__.Triple.make_unknown
        self.__abc = __self___class___Triple_make_unknown()
        self.__ABC = __self___class___Triple_make_unknown()
        return self
    @classmethod
    @t.final
    def make_equilateral(cls, side_length:t.Optional[T]=None) -> TriangleABC[T]:
        """Factory for an equilateral triangle with a certain `side_length`; slightly faster than normal instantiation"""
        if side_length is not None and side_length <= 0:
            raise ValueError("Triangles must have sides of length greater than 0")
        self = cls.__new__(cls)
        __self___class___Triple_from_lenient = self.__class__.Triple.from_lenient
        self.__abc = __self___class___Triple_from_lenient(side_length, side_length, side_length)
        self.__ABC = __self___class___Triple_from_lenient(60, 60, 60)
        return self
    @classmethod
    @t.final
    def make_3_4_5(cls, size_multiplier:T=1.0) -> TriangleABC[T]:
        """Factory for a 3-4-5 triangle, with each side multiplied by `size_multiplier`; slightly faster than normal instantiation"""
        if size_multiplier <= 0:
            raise ValueError("Triangles must have sides of length greater than 0")
        self = cls.__new__(cls)
        __self___class___Triple_from_lenient = self.__class__.Triple.from_lenient
        self.__abc = __self___class___Triple_from_lenient(3*size_multiplier, 4*size_multiplier, 5*size_multiplier)
        self.__ABC = __self___class___Triple_from_lenient(None, None, 90) # we put none cuz it is some decimal
        return self
    @classmethod
    @t.final
    def make_30_60_90(cls, size_multiplier:T=1) -> TriangleABC[T]:
        """Factory for a 30-60-90 triangle, with each side multiplied by `size_multiplier`; slightly faster than normal instantiation"""
        if size_multiplier <= 0:
            raise ValueError("Triangles must have sides of length greater than 0")
        self = cls.__new__(cls)
        __cls_Triple = cls.Triple
        __cls_Triple_from_lenient = __cls_Triple.from_lenient
        # noinspection PyProtectedMember
        self.__abc = __cls_Triple_from_lenient(1*size_multiplier, cls._sqrt_helper(__cls_Triple._type(3))*size_multiplier, 2*size_multiplier)
        self.__ABC = __cls_Triple_from_lenient(30, 60, 90)
        return self
    @classmethod
    @t.final
    def make_45_45_90(cls, size_multiplier:T=1) -> TriangleABC[T]:
        """Factory for a 45-45-90 triangle, with each side multiplied by `size_multiplier`; slightly faster than normal instantiation"""
        if size_multiplier <= 0:
            raise ValueError("Triangles must have sides of length greater than 0")
        self = cls.__new__(cls)
        __cls_Triple = cls.Triple
        __self___class___Triple_from_lenient = __cls_Triple.from_lenient
        # noinspection PyProtectedMember
        self.__abc = __self___class___Triple_from_lenient(1*size_multiplier, 1*size_multiplier, cls._sqrt_helper(__cls_Triple._type(2))*size_multiplier)
        self.__ABC = __self___class___Triple_from_lenient(45, 45, 90)
        return self


    @t.final
    def __str__(self, /) -> str:
        __self___class__ = self.__class__
        if self.__abc.known_amount is self.__ABC.known_amount==0:
            return f"{__self___class__.__name__}.{__self___class__.make_unknown.__name__}()"
        __self___abc = self.__abc
        __self___ABC = self.__ABC
        return f"{__self___class__.__name__}(a={__self___abc.a}, b={__self___abc.b}, c={__self___abc.c}, " \
                                           f"A={__self___ABC.a}, B={__self___ABC.b}, C={__self___ABC.c})"
    @t.final
    def __repr__(self, /) -> str:
        __self___abc = self.__abc
        __self___ABC = self.__ABC
        return f"{self.__class__.__name__}(a={__self___abc.a!r}, b={__self___abc.b!r}, c={__self___abc.c!r}, " \
                                         f"A={__self___ABC.a!r}, B={__self___ABC.b!r}, C={__self___ABC.c!r})"
    @t.final
    def __vhash__(self, /) -> int:
        __self___abc = self.__abc
        __self___ABC = self.__ABC
        return hash((__self___abc.a, __self___abc.b, __self___abc.c, __self___ABC.a, __self___ABC.b, __self___ABC.c))
    @t.final
    def copy(self, /) -> TriangleABC[T]:
        return self.__class__.alt_init(abc=self.__abc, ABC=self.__ABC)
    @staticmethod
    @t.final
    def validate_sides(value:TripleABC[T] | ImmutableTripleABC[T]) -> None:
        """Raise `ValueError` for each impossibility in `value`; Called on every set to `self.abc`"""
        for v in filter_not_none(value):
            if v <= 0:
                raise ValueError(f"Triangles must have sides greater than zero (Got: {v})")
    @staticmethod
    @t.final
    def validate_angles(value:TripleABC[T] | ImmutableTripleABC[T]) -> None:
        """Raise `ValueError` for each impossibility in `value`; Called on every set to `self.ABC`"""
        for v in filter_not_none(value):
            if not (0 < v < 180):
                raise ValueError(f"Cannot set an angle outside of the range 0 < value < 180 degrees (Got: {v})")
        if not anynone(value):
            if sum(value)!=180:
                raise ValueError("All angles in a triangle must add to 180")
    @staticmethod
    @t.final
    def _pairs_i() -> abcs.Generator[tuple[t.Literal[0,1,2],t.Literal[0,1,2]],None,None]:
        yield (0,1) # noqa parentheses
        yield (1,2) # noqa parentheses
        yield (2,0) # noqa parentheses
    @staticmethod
    @t.final
    def _all_i() -> abcs.Generator[tuple[t.Literal[0,1,2],t.Literal[1,2,0],t.Literal[2,0,1]],None,None]:
        yield (0,1,2) # noqa parentheses
        yield (1,2,0) # noqa parentheses
        yield (2,0,1) # noqa parentheses
    @functools.lru_cache(maxsize=6)
    @memorize_method
    @t.final
    def congruent_sss(self, /, other:TriangleABC[T]) -> bool: # SSS & backwards
        if not self.all_sides_known or not other.all_sides_known:
            return False
        __self___abc = self.__abc
        __other___abc = other.__abc
        for ai,bi,ci in self._all_i():
            if (
                __self___abc.a==__other___abc[ai] and
                __self___abc.b==__other___abc[bi] and
                __self___abc.c==__other___abc[ci]
            ) or (
                __self___abc.a==__other___abc[ci] and
                __self___abc.b==__other___abc[bi] and
                __self___abc.c==__other___abc[ai]
            ):
                return True
        return False
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def congruent_aas(self, /, other:TriangleABC[T]) -> bool: # AAS * backwards
        __self___abc = self.__abc
        __self___ABC = self.__ABC
        __other___abc = other.__abc
        __other___ABC = other.__ABC
        for ai,bi in self._pairs_i():
            if __self___ABC[ai] is not None and __self___ABC[bi] is not None and __self___abc[ai] is not None: # == shouldn't work for None
                for ai2,bi2 in self._pairs_i():
                    if (
                        __self___ABC[ai]==__other___ABC[ai2] and
                        __self___ABC[bi]==__other___ABC[bi2] and
                        __self___abc[ai]==__other___abc[ai2]
                    ) or (
                        __self___ABC[ai]==__other___ABC[bi2] and
                        __self___ABC[bi]==__other___ABC[ai2] and
                        __self___abc[ai]==__other___abc[bi2]
                    ):
                        return True
        return False
    def _congruent_sandwich(self, /, tri1a:Triple,tri1b:Triple,tri2a:Triple,tri2b:Triple) -> bool:
        for ai,bi,ci in self._all_i():
            if tri1a[ai] is not None and tri1a[bi] is not None: # == shouldn't work for None
                for ai2,bi2,ci2 in self._all_i():
                    if (
                        tri1a[ai]==tri2a[ai2] and
                        tri1a[bi]==tri2a[bi2]
                    ) or (
                        tri1a[bi]==tri2a[bi2] and
                        tri1a[ai]==tri2a[ai2]) and \
                    tri1b[ci]==tri2b[ci2]:
                        return True
        return False
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def congruent_sas(self, /, other:TriangleABC[T]) -> bool: # SAS & backwards
        return self._congruent_sandwich(self.__abc, self.__ABC, other.__abc, other.__ABC)
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def congruent_asa(self, /, other:TriangleABC[T]) -> bool: # ASA & backwards
        return self._congruent_sandwich(self.__ABC,self.__abc, other.__ABC,other.__abc)
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def congruent_rhs(self, /, other:TriangleABC[T]) -> bool:
        if not self.is_right or not other.is_right:
            return False
        __self___abc = self.__abc
        __self___ABC = self.__ABC
        __other___abc = other.__abc
        __other___ABC = other.__ABC
        for ai,bi in self._pairs_i():
            if __self___abc[ai] is not None and __self___abc[bi] is not None: # == shouldn't work for None
                for ai2,bi2 in self._pairs_i():
                    if (
                        __self___abc[ai]==__other___abc[ai2] and
                        __self___abc[bi]==__other___abc[bi2] and
                        __self___ABC[ai]==__other___ABC[ai2]==90
                    ) or (
                        __self___abc[ai]==__other___abc[bi2] and
                        __self___abc[bi]==__other___abc[ai2] and
                        __self___ABC[ai]==__other___ABC[bi2]==90
                    ): return True
        return False
    @functools.lru_cache(maxsize=24)
    # @memorized_method
    @t.final
    def congruent(self, /, other:TriangleABC[T]) -> bool:
        # SSS AAS SAS ASA
        return any((
            self.congruent_sss(other),
            self.congruent_aas(other),
            self.congruent_sas(other),
            self.congruent_asa(other),
            self.congruent_rhs(other)
        ))
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def similar_aaa(self, /, other:TriangleABC[T]) -> bool: # AAA & backwards
        if not self.all_angles_known or not other.all_angles_known:
            return False
        __self___ABC = self.__ABC
        __other___ABC = other.__ABC
        for ai,bi,ci in self._all_i():
            if (
                __self___ABC.a==__other___ABC[ai] and
                __self___ABC.b==__other___ABC[bi] and
                __self___ABC.c==__other___ABC[ci]
            ) or (
                __self___ABC.a==__other___ABC[ci] and
                __self___ABC.b==__other___ABC[bi] and
                __self___ABC.c==__other___ABC[ai]
            ): return True
        return False
    @functools.lru_cache(maxsize=6)
    # @memorized_method
    @t.final
    def similar_sss(self, /, other:TriangleABC[T]) -> bool: # AAA & backwards
        if not self.all_sides_known or not other.all_sides_known:
            return False
        __self___abc = self.__abc
        __other___abc = other.__abc
        for ai,bi,ci in self._all_i():
            if (
                __self___abc.a/__other___abc[ai]==
                __self___abc.b/__other___abc[bi]==
                __self___abc.c/__other___abc[ci]
            ) or (
                __self___abc.a/__other___abc[ci]==
                __self___abc.b/__other___abc[bi]==
                __self___abc.c/__other___abc[ai]
            ): return True
        return False
    @functools.lru_cache(maxsize=24)
    # @memorized_method
    @t.final
    def similar(self, /, other:TriangleABC[T]) -> bool:
        if self.similar_aaa(other) or self.similar_sss(other):
            return True
        __self___class__ = self.__class__
        __self___class___alt_init = __self___class__.alt_init
        normalized_self,normalized_other = (
            (
                __self___class___alt_init(abc=(tri.__abc[i]/denominator for i in (0,1,2)) , ABC=tri.__ABC)
                if 1 not in tri.__abc else
                tri
            ) for tri,denominator in ( (tri,max(tri.__abc)) for tri in (self,other) )
        )
        if normalized_self.similar_aaa(other) or normalized_other.similar_sss(other):
            return __self___class__.congruent(normalized_self, normalized_other)
        return False
    @memorize_method
    @t.final
    def __find_angles_using__equilateral(self, /) -> None:
        if self.known_angles in (1,2) and self.is_equilateral and self.all_sides_known:
            known_angle_i = None
            __self___ABC = self.__ABC
            for angle_i in (0, 1, 2):
                if __self___ABC[angle_i] is not None:
                    known_angle_i = angle_i
                    break
            for angle_i in (0, 1, 2):
                if angle_i != known_angle_i:
                    __self___ABC[angle_i] = __self___ABC[known_angle_i]
    @memorize_method
    @t.final
    def __find_angles_using__180_degree_rule(self, /) -> None:
        if self.known_angles==2:
            total = 0;bad = 0
            __self___ABC = self.__ABC
            for i,u in enumerate(__self___ABC):
                if u is None:
                    bad = i
                else:
                    total += u
            __self___ABC[bad] = 180 - total
    @memorize_method
    @t.final
    def __find_angles_using__sohacahtoa(self, /) -> None:
        if self.known_angles in (1,2) and self.is_right and self.known_sides in (2,3):
            leg_angles_i:list[int] = []
            __self___ABC = self.__ABC
            for i,angle in enumerate(__self___ABC):
                if angle == 90:
                    right_angle_i = i
                else:
                    leg_angles_i.append(i)
            __self___abc = self.__abc
            for angle_i in leg_angles_i:
                other_angle_i = leg_angles_i[1] if angle_i == leg_angles_i[0] else leg_angles_i[0]
                opposite = __self___abc[angle_i]
                # noinspection PyUnboundLocalVariable
                hypotenuse = __self___abc[right_angle_i]
                adjacent = __self___abc[other_angle_i]
                if opposite is not None and hypotenuse is not None: # if sin is possible
                    __self___ABC[angle_i] = asin(opposite/hypotenuse)
                if adjacent is not None and hypotenuse is not None: # if cos is possible
                    __self___ABC[angle_i] = acos(adjacent/hypotenuse)
                if opposite is not None and adjacent is not None: # if tan is possible
                    __self___ABC[angle_i] = atan(opposite/adjacent)
    @staticmethod
    @abc.abstractmethod
    def _degrees_acos_helper(value:T) -> T:
        """Should return the degrees of the acos of the input"""
    @memorize_method
    @t.final
    def __find_angles_using__cosine_law(self, /) -> None:
        if self.known_angles in (1,2) and self.known_sides == 3:
            a,b,c = self.__abc
            __self___ABC = self.__ABC
            _degrees_acos_helper = self._degrees_acos_helper
            __self___ABC[0] = _degrees_acos_helper((b**2 + c**2 - a**2) / (2*b*c))
            __self___ABC[1] = _degrees_acos_helper((c**2 + a**2 - b**2) / (2*c*a))
            __self___ABC[2] = _degrees_acos_helper((a**2 + b**2 - c**2) / (2*a*b))
    @memorize_method
    @t.final
    def __find_sides_using__equilateral(self, /) -> None:
        if self.known_sides in (1,2) and self.is_equilateral and self.all_angles_known:
            __self___abc = self.__abc
            __anynone = anynone
            for combo_i0, combo_i1 in self._pairs_i():
                if __self___abc[combo_i0] != __self___abc[combo_i1] and not __anynone((__self___abc[combo_i0], __self___abc[combo_i1])):
                    raise ValueError("Equilateral triangle cannot have sides and angles not correspond")
            known_side_i = None
            for side_i in (0, 1, 2):
                if __self___abc[side_i] is not None:
                    known_side_i = side_i
                    break
            for side_i in (0, 1, 2):
                if side_i != known_side_i:
                    __self___abc[side_i] = __self___abc[known_side_i]
    @memorize_method
    @t.final
    def __find_sides_using__cosine_law(self, /) -> None:
        if self.known_sides==2:
            __self___abc = self.__abc
            a,b,c = __self___abc
            # noinspection PyPep8Naming
            A,B,C = self.__ABC
            __anynone = anynone
            for combo,unknown_i in ( ((a,C,b),2) , ((b,A,c),0) , ((c,B,a),1) ):
                # if allare(combo, isnotnone) and self.__abc[unknown_i] is None: # we don't need to work if we already know the side we are working with
                if not __anynone(combo) and __self___abc[unknown_i] is None: # we don't need to work if we already know the side we are working with
                    s1,angle,s2 = combo
                    __self___abc[unknown_i] = ((s1**2) + (s2**2) - (2*s1*s2*cos(angle))) ** (1/2)
    @staticmethod
    @abc.abstractmethod
    def _sqrt_helper(value:T) -> T:
        ...
    @memorize_method
    @t.final
    def __find_sides_using__right_triangle(self, /) -> None:
        other2:list = []
        if self.known_sides==2 and self.is_right:
            rc = None
            __self___ABC = self.__ABC
            for angle_i in (0,1,2):
                if __self___ABC[angle_i] == 90:
                    rc = angle_i
                else:
                    other2.append(angle_i)
            if rc is not None:
                __self___abc = self.__abc
                hypotenuse = __self___abc[rc] # because rc is the 90 degree angle and hypotenuse is opposite
                if hypotenuse is not None:
                    # pythagorean theorem finding leg method
                    if (__self___abc[other2[0]] is not None) != (__self___abc[other2[1]] is None): # ensures we know one and don't know the other
                        known_leg_i = other2[0] if __self___abc[other2[0]] is not None else other2[1]
                        unknown_i = (other2[1] if known_leg_i == other2[0] else other2[0]) # the opposite one
                        # just so we dont have to repeat in both Triangle types
                        __self___abc[unknown_i] = self._sqrt_helper(hypotenuse**2 - __self___abc[known_leg_i]**2)
    @memorize_method
    @t.final
    def _find_angles(self, /) -> None:
        """Attempt to find unknown angles"""
        self.__find_angles_using__180_degree_rule()
        self.__find_angles_using__cosine_law()
        self.__find_angles_using__equilateral()
        self.__find_angles_using__sohacahtoa()
    @memorize_method
    @t.final
    def _find_sides(self, /) -> None:
        """Attempt to find unknown sides"""
        self.__find_angles_using__cosine_law()
        self.__find_sides_using__equilateral()
        self.__find_sides_using__right_triangle()
    @memorize_method # we don't need to solve all over again if we already have solved with the same exact triangle and nothing changed!
    def _solve_one(self, /) -> bool:
        self._find_angles()
        self._find_sides()
        return self.solved
    @memorize_method('twice')
    @t.final
    def solve(self, /, twice:bool=True) -> bool:
        """Attempt to solve for the triangle's angles and sides
        Performed twice if `twice==True`, it is still not solved after the first round, and no new information was gained
        The only reason to have `twice` be False is if the calculations used to solve are desired to be called exactly one time"""
        if self._solve_one():
            return True
        if twice: # just check if we already solved it, might speed up
            return self._solve_one()
        return False























