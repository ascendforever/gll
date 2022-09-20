# noinspection PyUnusedLocal
__all__ = [
    'partition',
    'partition_unsafe',
    'partition_ultra_unsafe',
]

from gll.__common import *
from gll.__static.__static import *

SequenceT = t.TypeVar('Sequence_T', bound=abcs.Sequence) # VERY IMPORTANT - MAKES Sequence_T HAVE TO BE A SUBCLASS OF SEQUENCE
def partition(iterable:SequenceT, splits:int) -> SizedIterator[SequenceT]:
    """
    Partition an iterable into a certain amount of chunks
    :param iterable: Source
    :param splits: Amount of chunks desired
    :return: Iterator containing each chunk
    """
def partition_unsafe(iterable:SequenceT, splits:int) -> SizedIterator[SequenceT]:
    """Use if splits is guaranteed to >= 0
    [Created 11/12/21]"""
def partition_ultra_unsafe(iterable:SequenceT, splits:int) -> SizedIterator[SequenceT]:
    """Use if splits is guaranteed to >= 0 and splits is guarranteed <= iterable length
    [Created 11/12/21]"""
def _common(iterable:SequenceT, splits:int, l:int) -> SizedIterator[SequenceT]:
    """Use if splits is guaranteed to >= 0 and splits is guarranteed <= iterable length
    [Created 11/12/21]"""
