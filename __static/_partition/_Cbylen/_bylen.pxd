





cimport cython
from cpython cimport int as PyInt



cdef class PartitionLen:
    cdef:
        readonly object iterable
        readonly PyInt length
        readonly PyInt iterations
        readonly PyInt remainder
        readonly PyInt sizes
cdef class PartitionLenUnsafe(PartitionLen):
    pass






