
__all__ = [
    'PartitionLen',
    # 'partition_len',
    'PartitionLenUnsafe',
    # 'partition_len_unsafe',
]

from gll.__common import *
from gll.__static.__static.__cimports cimport *

cimport cython
from cpython cimport int as PyInt

cdef class PartitionLen:
    def __init__(self, object iterable, PyInt sizes):
        if sizes <= 0:
            raise ValueError("`sizes` must be an integer greater than zero")
        # ------------------------------------------------------------------------------------
        cdef cython.uint iterations
        cdef cython.uint remainder
        iterations,remainder = divmod(len(iterable), sizes)
        self.iterable = iterable
        self.length = iterations + (not not remainder)
        self.iterations = iterations
        self.remainder = remainder
        self.sizes = sizes
    def __iter__(self):
        cdef cython.uint i
        cdef object iterable = self.iterable
        cdef PyInt sizes = self.sizes
        cdef PyInt iterations =  self.iterations
        for i in range(self.iterations):
            yield iterable[i*sizes:(i+1)*sizes]
        if remainder!=0:
            yield iterable[sizes*iterations:]
    def __len__(self) -> PyInt:
        return self.length
# cpdef PartitionLen partition_len(object iterable, PyInt sizes):
#     return PartitionLen(object iterable, PyInt sizes)
cdef class PartitionLenUnsafe(PartitionLen):
    def __init__(self, object iterable, PyInt sizes):
        # ------------------------------------------------------------------------------------
        cdef cython.uint iterations
        cdef cython.uint remainder
        iterations,remainder = divmod(len(iterable), sizes)
        self.iterable = iterable
        self.length = iterations + (not not remainder)
        self.iterations = iterations
        self.remainder = remainder
        self.sizes = sizes
# cpdef PartitionLenUnsafe partition_len_unsafe(object iterable, PyInt sizes):
#     return PartitionLenUnsafe(object iterable, PyInt sizes)
# # DO NOT MODIFY THIS - IT WORKS PERFECTLY
# def partition_len(object iterable, const cython.uint sizes) -> col.abc.Generator:
#     if sizes <= 0:
#         raise ValueError("`sizes` must be an integer greater than zero")
#     # ------------------------------------------------------------------
#     cdef cython.uint iterations
#     cdef cython.uint remainder
#     iterations,remainder = divmod(len(iterable), sizes)
#     cdef cython.uint i
#     for i in range(iterations):
#         yield iterable[i*sizes:(i+1)*sizes]
#     if remainder!=0:
#         yield iterable[sizes*iterations:]
#     # ------------------------------------------------------------------
# def partition_len_unsafe(object iterable, const cython.uint sizes) -> col.abc.Generator:
#     """Use this if sizes is guaranteed >= 0"""
#     # ------------------------------------------------------------------
#     cdef cython.uint iterations
#     cdef cython.uint remainder
#     iterations,remainder = divmod(len(iterable), sizes)
#     cdef cython.uint i
#     for i in range(iterations):
#         yield iterable[i*sizes:(i+1)*sizes]
#     if remainder!=0:
#         yield iterable[sizes*iterations:]
#     # ------------------------------------------------------------------
