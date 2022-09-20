
__all__ = [
    'quadraticl',
    'quadraticd',
    'quadratic',
    'quadraticf',
    "sinl", "sind", "sin", 'sinf', "asinl", 'asind', 'asin', 'asinf', 
    "cosl", "cosd", "cos", 'cosf', "acosl", 'acosd', 'acos', 'acosf', 
    "tanl", "tand", "tan", 'tanf', "atanl", 'atand', 'atan', 'atanf', 
    "cotl", "cotd", "cot", 'cotf', "acotl", 'acotd', 'acot', 'acotf', 
    "cscl", "cscd", "csc", 'cscf', "acscl", 'acscd', 'acsc', 'acscf', 
    "secl", "secd", "sec", 'secf', "asecl", 'asecd', 'asec', 'asecf', 
]

from gll.__common import *
from gll.__static.__cimports cimport *
# from libc.math cimport (
#     sinl as __Clibcmath.sinl, asinl as __Clibcmath.asinl, sin as __Clibcmath.sin, asin as __Clibcmath.asin, sinf as __Clibcmath.sinf, asinf as __Clibcmath.asinf, 
#     cosl as __Clibcmath.cosl, acosl as __Clibcmath.acosl, cos as __Clibcmath.cos, acos as __Clibcmath.acos, cosf as __Clibcmath.cosf, acosf as __Clibcmath.acosf, 
#     tanl as __Clibcmath.tanl, atanl as __Clibcmath.atanl, tan as __Clibcmath.tan, atan as __Clibcmath.atan, tanf as __Clibcmath.tanf, atanf as __Clibcmath.atanf
# )
# cimport libc.math as cmath
from . cimport __Clibcmath


cpdef (cython.longdouble, cython.longdouble) quadraticl(const cython.longdouble a, const cython.longdouble b, const cython.longdouble c) nogil:
    cdef cython.longdouble disc = __Clibcmath.sqrtl((b**2)-(4*a*c))
    cdef cython.longdouble a2 = a*2 # 2*a
    cdef cython.longdouble nb = -b
    return (nb+disc)/a2 , (nb-disc)/a2
cpdef (cython.double, cython.double) quadraticd(const cython.double a, const cython.double b, const cython.double c) nogil:
    cdef cython.double disc = __Clibcmath.sqrt((b**2)-(4*a*c))
    cdef cython.double a2 = a*2 # 2*a
    cdef cython.double nb = -b
    return (nb+disc)/a2 , (nb-disc)/a2
cpdef tuple quadratic(object a, object b, object c):
    cdef object disc = sqrt((b**2)-(4*a*c))
    cdef object a2 = a << 1
    cdef object nb = -b
    return (nb+disc)/a2 , (nb-disc)/a2
cpdef (cython.float, cython.float) quadraticf(const cython.float a, const cython.float b, const cython.float c) nogil:
    cdef cython.float disc = __Clibcmath.sqrtf((b**2)-(4*a*c))
    cdef cython.float a2 = a*2 # 2*a
    cdef cython.float nb = -b
    return (nb+disc)/a2 , (nb-disc)/a2

cpdef cython.longdouble  sinl(const cython.longdouble x) nogil: return __Clibcmath.sinl(x)
cpdef cython.longdouble asinl(const cython.longdouble x) nogil: return __Clibcmath.asinl(x)
cpdef cython.double      sind(const cython.double     x) nogil: return __Clibcmath.sin(x)
cpdef cython.double     asind(const cython.double     x) nogil: return __Clibcmath.asin(x)
sin = math.sin
asin = math.asin
cpdef cython.float       sinf(const cython.float      x) nogil: return __Clibcmath.sinf(x)
cpdef cython.float      asinf(const cython.float      x) nogil: return __Clibcmath.asinf(x)

cpdef cython.longdouble  cosl(const cython.longdouble x) nogil: return __Clibcmath.cosl(x)
cpdef cython.longdouble acosl(const cython.longdouble x) nogil: return __Clibcmath.acosl(x)
cpdef cython.double      cosd(const cython.double     x) nogil: return __Clibcmath.cos(x)
cpdef cython.double     acosd(const cython.double     x) nogil: return __Clibcmath.acos(x)
cos = math.cos
acos = math.acos
cpdef cython.float       cosf(const cython.float      x) nogil: return __Clibcmath.cosf(x)
cpdef cython.float      acosf(const cython.float      x) nogil: return __Clibcmath.acosf(x)

cpdef cython.longdouble  tanl(const cython.longdouble x) nogil: return __Clibcmath.tanl(x)
cpdef cython.longdouble atanl(const cython.longdouble x) nogil: return __Clibcmath.atanl(x)
cpdef cython.double      tand(const cython.double     x) nogil: return __Clibcmath.tan(x)
cpdef cython.double     atand(const cython.double     x) nogil: return __Clibcmath.atan(x)
tan = math.tan
atan = math.atan
cpdef cython.float       tanf(const cython.float      x) nogil: return __Clibcmath.tanf(x)
cpdef cython.float      atanf(const cython.float      x) nogil: return __Clibcmath.atanf(x)

cpdef cython.longdouble  cotl(const cython.longdouble x) nogil: return 1 / __Clibcmath.tanl(x)
cpdef cython.longdouble acotl(const cython.longdouble x) nogil: return __Clibcmath.atanl(1/x)
cpdef cython.double      cotd(const cython.double     x) nogil: return 1 / __Clibcmath.tan(x)
cpdef cython.double     acotd(const cython.double     x) nogil: return __Clibcmath.atan(1/x)
cpdef object             cot (      object            x)      : return 1       / tan(x)
cpdef object            acot (      object            x)      : return atan(1/x)
cpdef cython.float       cotf(const cython.float      x) nogil: return 1 / __Clibcmath.tanf(x)
cpdef cython.float      acotf(const cython.float      x) nogil: return __Clibcmath.atanf(1/x)

cpdef cython.longdouble  cscl(const cython.longdouble x) nogil: return 1 / __Clibcmath.sinl(x)
cpdef cython.longdouble acscl(const cython.longdouble x) nogil: return __Clibcmath.asinl(1/x)
cpdef cython.double      cscd(const cython.double     x) nogil: return 1 / __Clibcmath.sin(x)
cpdef cython.double     acscd(const cython.double     x) nogil: return __Clibcmath.asin(1/x)
cpdef object             csc (      object            x)      : return 1       / sin(x)
cpdef object            acsc (      object            x)      : return asin(1/x)
cpdef cython.float       cscf(const cython.float      x) nogil: return 1 / __Clibcmath.sinf(x)
cpdef cython.float      acscf(const cython.float      x) nogil: return __Clibcmath.asinf(1/x)

cpdef cython.longdouble  secl(const cython.longdouble x) nogil: return 1 / __Clibcmath.cosl(x)
cpdef cython.longdouble asecl(const cython.longdouble x) nogil: return __Clibcmath.acosl(1/x)
cpdef cython.double      secd(const cython.double     x) nogil: return 1 / __Clibcmath.cos(x)
cpdef cython.double     asecd(const cython.double     x) nogil: return __Clibcmath.acos(1/x)
cpdef object             sec (      object            x)      : return 1       / cos(x)
cpdef object            asec (      object            x)      : return acos(1/x)
cpdef cython.float       secf(const cython.float      x) nogil: return 1 / __Clibcmath.cosf(x)
cpdef cython.float      asecf(const cython.float      x) nogil: return __Clibcmath.acosf(1/x)

















