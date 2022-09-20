
__all__ = [
    # 'short_byte_units',
    # 'long_byte_units',
    'bits',
    'kilobytes',
    'megabytes',
    'gigabytes',
    'petabytes',
    'exabytes',
    'zetabytes',
    'yottabytes',
]

from gll.__common import *
from gll.__static.__cimports cimport *

cimport cython

# This replaced below 11/12/21 # og cythonization 12/7/21
cpdef cython.longdouble bits      (const cython.longdouble num): return num * 8
cpdef cython.longdouble kilobytes (const cython.longdouble num): return num / 0x400
cpdef cython.longdouble megabytes (const cython.longdouble num): return num / 0x100000 # 1024**2
cpdef cython.longdouble gigabytes (const cython.longdouble num): return num / 0x40000000 # 1024**3
cpdef cython.longdouble terabytes (const cython.longdouble num): return num / 0x10000000000 # 1024**4
cpdef cython.longdouble petabytes (const cython.longdouble num): return num / 0x4000000000000 # 1024**5
cpdef cython.longdouble exabytes  (const cython.longdouble num): return num / 0x1000000000000000 # 1024**6
cpdef cython.longdouble zetabytes (const cython.longdouble num): return num / 0x400000000000000000 # 1024**7
cpdef cython.longdouble yottabytes(const cython.longdouble num): return num / 0x100000000000000000000 # 1024**8