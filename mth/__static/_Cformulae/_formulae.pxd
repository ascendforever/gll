
from gll.__static.__cimports cimport *
from . cimport __Clibcmath


cpdef (cython.longdouble, cython.longdouble) quadraticl(const cython.longdouble a, const cython.longdouble b, const cython.longdouble c) nogil
cpdef (cython.double, cython.double) quadraticd(const cython.double a, const cython.double b, const cython.double c) nogil
cpdef tuple quadratic(object a, object b, object c)
cpdef (cython.float, cython.float) quadraticf(const cython.float a, const cython.float b, const cython.float c) nogil

cpdef cython.longdouble  sinl(const cython.longdouble x) nogil
cpdef cython.longdouble asinl(const cython.longdouble x) nogil
cpdef cython.double      sind(const cython.double     x) nogil
cpdef cython.double     asind(const cython.double     x) nogil
cpdef cython.float       sinf(const cython.float      x) nogil
cpdef cython.float      asinf(const cython.float      x) nogil

cpdef cython.longdouble  cosl(const cython.longdouble x) nogil
cpdef cython.longdouble acosl(const cython.longdouble x) nogil
cpdef cython.double      cosd(const cython.double     x) nogil
cpdef cython.double     acosd(const cython.double     x) nogil
cpdef cython.float       cosf(const cython.float      x) nogil
cpdef cython.float      acosf(const cython.float      x) nogil

cpdef cython.longdouble  tanl(const cython.longdouble x) nogil
cpdef cython.longdouble atanl(const cython.longdouble x) nogil
cpdef cython.double      tand(const cython.double     x) nogil
cpdef cython.double     atand(const cython.double     x) nogil
cpdef cython.float       tanf(const cython.float      x) nogil
cpdef cython.float      atanf(const cython.float      x) nogil

cpdef cython.longdouble  cotl(const cython.longdouble x) nogil
cpdef cython.longdouble acotl(const cython.longdouble x) nogil
cpdef cython.double      cotd(const cython.double     x) nogil
cpdef cython.double     acotd(const cython.double     x) nogil
cpdef cython.float       cotf(const cython.float      x) nogil
cpdef cython.float      acotf(const cython.float      x) nogil

cpdef cython.longdouble  cscl(const cython.longdouble x) nogil
cpdef cython.longdouble acscl(const cython.longdouble x) nogil
cpdef cython.double      cscd(const cython.double     x) nogil
cpdef cython.double     acscd(const cython.double     x) nogil
cpdef cython.float       cscf(const cython.float      x) nogil
cpdef cython.float      acscf(const cython.float      x) nogil

cpdef cython.longdouble  secl(const cython.longdouble x) nogil
cpdef cython.longdouble asecl(const cython.longdouble x) nogil
cpdef cython.double      secd(const cython.double     x) nogil
cpdef cython.double     asecd(const cython.double     x) nogil
cpdef cython.float       secf(const cython.float      x) nogil
cpdef cython.float      asecf(const cython.float      x) nogil






























