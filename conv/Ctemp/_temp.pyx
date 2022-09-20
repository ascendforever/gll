
__all__ = [
    'c_to_f',
    'c_to_k',
    'f_to_c',
    'f_to_k',
    'k_to_c',
    'k_to_f',
]

from gll.__common import *
from gll.__static.__cimports cimport *
# from libc.math cimport fmal # maybe a good idea

# cimport cython
# from cpython cimport int as PyInt

# all [Created 8/6/20] # cythonization 12/7/21
cpdef cython.longdouble c_to_f(const cython.longdouble num) nogil: return (9/5) * num + 32
cpdef cython.longdouble c_to_k(const cython.longdouble num) nogil: return num + 273
cpdef cython.longdouble f_to_c(const cython.longdouble num) nogil: return (5/9) * (num-32)
cpdef cython.longdouble f_to_k(const cython.longdouble num) nogil: return (5/9) * (num-32) + 273
cpdef cython.longdouble k_to_c(const cython.longdouble num) nogil: return num - 273
cpdef cython.longdouble k_to_f(const cython.longdouble num) nogil: return (9/5) * (num-273) + 32










