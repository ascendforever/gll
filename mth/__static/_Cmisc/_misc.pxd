

from gll.__static.__cimports cimport *

cpdef (cython.ulonglong,cython.ulonglong) rand_ints_that_add_ulonglong(const cython.ulonglong sum, const cython.ulonglong max)
cpdef (cython.ulong,    cython.ulong    ) rand_ints_that_add_ulong    (const cython.ulong     sum, const cython.ulong     max)
cpdef (cython.uint,     cython.uint     ) rand_ints_that_add_uint     (const cython.uint      sum, const cython.uint      max)
cpdef tuple rand_ints_that_add          (PyInt      sum, PyInt      max)
cpdef (cython.ushort,   cython.ushort   ) rand_ints_that_add_ushort   (const cython.ushort    sum, const cython.ushort    max)
cpdef (cython.uchar,    cython.uchar    ) rand_ints_that_add_uchar    (const cython.uchar     sum, const cython.uchar     max)












