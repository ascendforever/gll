
__all__ = [
    'rand_ints_that_add_ulonglong',
    'rand_ints_that_add_ulong',
    'rand_ints_that_add_uint',
    'rand_ints_that_add',
    'rand_ints_that_add_ushort',
    'rand_ints_that_add_uchar',
]

from gll.__common import *
from gll.__static.__cimports cimport *


cpdef (cython.ulonglong,cython.ulonglong) rand_ints_that_add_ulonglong(const cython.ulonglong sum, const cython.ulonglong max):
    cdef cython.ulonglong first = random.randint(sum // 2, max) # sum // 2
    return first, max - first
cpdef (cython.ulong,    cython.ulong    ) rand_ints_that_add_ulong    (const cython.ulong     sum, const cython.ulong     max):
    cdef cython.ulong first = random.randint(sum // 2, max) # sum // 2
    return first, max - first
cpdef (cython.uint,     cython.uint     ) rand_ints_that_add_uint     (const cython.uint      sum, const cython.uint      max):
    cdef cython.uint first = random.randint(sum // 2, max) # sum // 2
    return first, max - first
cpdef tuple rand_ints_that_add          (PyInt      sum, PyInt      max):
    cdef cython.uint first = random.randint(sum // 2, max) # sum // 2
    return first, max - first
cpdef (cython.ushort,   cython.ushort   ) rand_ints_that_add_ushort   (const cython.ushort    sum, const cython.ushort    max):
    cdef cython.ushort first = random.randint(sum // 2, max) # sum // 2
    return first, max - first
cpdef (cython.uchar,    cython.uchar    ) rand_ints_that_add_uchar    (const cython.uchar     sum, const cython.uchar     max):
    cdef cython.uchar first = random.randint(sum // 2, max) # sum // 2
    return first, max - first









