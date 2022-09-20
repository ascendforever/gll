
__all__ = [
    'partition',
    'partition_unsafe',
    'partition_ultra_unsafe',
]

from gll.__common import *
from gll.__static.__static.__cimports cimport *

cimport cython
from cpython cimport int as PyInt

# T = t.TypeVar("T")
# # DO NOT MODIFY THIS - IT WORKS PERFECTLY
cpdef object partition(object iterable, const cython.uint splits): # (iterable:col.abc.Sequence[T], splits:cython.uint):
    cdef cython.uint l = len(iterable)
    # ------------------------------------------------------------------------
    if splits == 0: # <= 0:
        raise ValueError("`splits` must be an integer greater than 0")
    if splits > l:
        raise ValueError("`splits` must be less than total iterable length")
    return sized_iterator_from_raw_unsafe(_common(iterable, splits, len(iterable)), splits)
cpdef object partition_unsafe(object iterable, const cython.uint splits): # (iterable:col.abc.Sequence[T], splits:cython.uint) -> col.abc.Generator[col.abc.Sequence[T],None,None]:
    cdef cython.uint l = len(iterable)
    # ------------------------------------------------------------------------
    if splits > l:
        raise ValueError("`splits` must be less than total iterable length")
    return sized_iterator_from_raw_unsafe(_common(iterable, splits, len(iterable)), splits)
cpdef object partition_ultra_unsafe(object iterable, const cython.uint splits): # (iterable:col.abc.Sequence[T], splits:cython.uint) -> col.abc.Generator[col.abc.Sequence[T],None,None]:
    return sized_iterator_from_raw_unsafe(_common(iterable, splits, len(iterable)), splits)
def _common(object iterable, const cython.uint splits, const cython.uint l) -> col.abc.Generator: # (iterable:col.abc.Sequence[T], splits:cython.uint, l:cython.uint) -> col.abc.Generator[col.abc.Sequence[T],None,None]:
    cdef object range = builtins.range
    cdef cython.uint i
    cdef cython.ushort chunk_size
    cdef cython.ushort remainder
    chunk_size,remainder = divmod(l, splits)
    cdef cython.ushort boosted_am
    cdef cython.uint starting_i_for_rest
    cdef cython.uint chunk_size_plus1
    if remainder:
        boosted_am = splits - remainder
        for i in range(boosted_am):
            yield iterable[                    i*chunk_size      :(i+1)*chunk_size]
        starting_i_for_rest = chunk_size*boosted_am # where we start based off the previous loop
        chunk_size_plus1 = chunk_size+1
        for i in range(splits-boosted_am):
            yield iterable[starting_i_for_rest+i*chunk_size_plus1:(i+1)*chunk_size_plus1+starting_i_for_rest]
    else:
        for i in range(splits):
            yield iterable[i*chunk_size:(i+1)*chunk_size]
