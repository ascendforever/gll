from __future__ import annotations

__all__ = [
    'TextPartition',
]

from gll.__common import *
from gll.__static.__static import *

from ._Cbylen import PartitionLenUnsafe

class TextPartition(abcs.Iterable[str], VHashable):
    """ Helper class for partitioning text
    Allows for text to be chunked in particular sizes"""
    __slots__    = ('_source','size','split','lenient','first_size','max_chunk_size', '__weakref__')
    __match_args__=('_source','size','split','lenient','first_size','max_chunk_size', 'lengths')
    def __init__(self, /, text:str|abcs.Iterable[str], size:int=2000, split:str='\n', *, lenient:bool=False, first_size:None|int=None, max_chunk_size:None|int=None):
        r"""
        Initialize
        :param text: Source - may be a string or sequence of strings
        :param size: Max size of each chunk when joined
        :param split: Split between chunks - when source is str, it is split by this; when source is sequence, it is assumed to be split by this
        :param lenient: Allow going over `size` when it is impossible to fit into a chunk size
        :param first_size: Override the max size of the first chunk
        :param max_chunk_size: Max amount of strs in a chunk; ignored if source is str and split=''; (essentially max lines per chunk if split='\n' or max words per chunk if split=' ')
        """
        self._source:abcs.Sequence[str] = ...
        self.size:int = size
        self.split:t.Final[str] = split
        self.lenient:t.Final[bool] = lenient
        self.first_size:t.Final[int] = first_size
        self.max_chunk_size:t.Final[int] = max_chunk_size
        self.source = text
    @property
    def source(self, /) -> abcs.Sequence[str]:
        return self._source
    @source.setter
    def source(self, /, value:str|abcs.Iterable[str]) -> None:
        if isinstance(value, str):
            if (_split:=self.split)!='':
                value = value.split(_split)
        elif not isinstance(value, abcs.Sequence): # this is really just in case - just so it works if the type checker doesn't inform us we mess up
            # value = LazySeq.from_it(iter(value))
            value = list(value) # we just make it a list, not a lazy one because it is just going to be iterated immediately
        self._source = value
    @classmethod
    def regex_split(cls, /, text:str, size:int=2000, re_split:re.Pattern=re.compile(r'\n'), len_split:int=1) -> abcs.Generator[list[str],None,None]:
        """Shortcut to self.each_not_joined() with using re.split, instead of str.split
        Split size should be uniform and passed in len_split"""
        self = cls.__new__(cls)
        self._source = re_split.split(text)
        # noinspection PyFinal
        self.size = size
        # noinspection PyFinal
        self.split = 'x'*len_split
        return self.split_chunks()
    @classmethod
    def chunks_wrapped_oneshot(cls, /, text: str | abcs.Iterable[str], left:str, right:str, size:int=2000, split:str= '\n', *, lenient:bool=False, first_size: None | int=None, max_chunk_size: None | int=None) -> abcs.Iterator[str]:
        """Shortcut to cls(text, size-len(left)-len(right)-2*len(split), ...).chunks_wrapped(left, right)"""
        return cls(text, size:=(size-len(left)-len(right)-2*len(split)), lenient=lenient, first_size=first_size, max_chunk_size=max_chunk_size).chunks_wrapped(left,right)
    @classmethod
    def chunks_wrapped_post_oneshot(cls, /, text: str | abcs.Iterable[str], left:str, right:str, size:int=2000, split:str= '\n', *, lenient:bool=False, first_size: None | int=None, max_chunk_size: None | int=None) -> abcs.Iterator[str]:
        """Shortcut to cls(text, size-len(left)-len(right), ...).chunks_post_wrapped(left, right)"""
        return cls(text, size:=(size-len(left)-len(right)), lenient=lenient, first_size=first_size, max_chunk_size=max_chunk_size).chunks_post_wrapped(left,right)
    # @classmethod
    # def make_safe(cls, /, text:str|abcs.Sequence[str], size:int=2000, split:str='\n') -> TextPartition:
    #     """Checks type of input text; Useful because IDE type checkers may fail for this"""
    #     # noinspection PyShadowingBuiltins
    #     isinstance = builtins.isinstance
    #     if isinstance(text, str) or isinstance(text, abcs.Sequence):
    #         return cls(text,size,split)
    #     raise TypeError("`text` must be a sequence of strings or a string")
    # @classmethod
    # def make_safe_ultra(cls, /, text:str|abcs.Sequence[str], size:int=2000, split:str='\n') -> TextPartition:
    #     """Extreme type checking and value checking"""
    #     # noinspection PyShadowingBuiltins
    #     isinstance = builtins.isinstance
    #     # noinspection PyShadowingBuiltins
    #     str = builtins.str
    #     if isinstance(text, str) or isinstance(text, abcs.Sequence):
    #         if isinstance(size, int):
    #             if size > 0:
    #                 if isinstance(split, str):
    #                     return cls(text,size,split)
    #                 raise TypeError("`split` must be a string")
    #             raise ValueError("`size` must be greater than 0")
    #         raise TypeError("`size` must be an integer")
    #     raise TypeError("`text` must be a sequence of strings or a string")
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}(text={self._source!r}, size={self.size}, split={self.split!r})"
    def __vhash__(self) -> int:
        return hash((self._source if isinstance(self._source, str) else tuple(self._source), self.split, self.lenient, self.first_size or self.size, self.max_chunk_size))
    @MemorizedMethodFirst.with_proper_repr
    def lengths(self) -> array.array[int]:
        """Do not use if `source` is a string!"""
        if isinstance(self._source, str):
            raise TypeError("Lengths should not be calculated when the source is a string and split is '', as it will create a wasteful array of int 1s")
        return self._lengths_unsafe()
    def __eq__(self, other:TextPartition) -> bool:
        # all of these warnings are completely bs
        if isinstance(other, self.__class__) and \
                (self_split:=self.split)==(other_split:=other.split) and \
                self.lenient is other.lenient and \
                (self_size:=self.size)==(other_size:=other.size) and \
                (self.first_size or self_size)==(other.first_size or other_size) and \
                self.max_chunk_size==other.max_chunk_size:
            self_source = self._source
            self_source_is_str = isinstance(self_source, str)
            other_source = other._source
            other_source_is_str = isinstance(other_source, str)
            if self_source_is_str:
                if other_source_is_str:
                    return self_source==other_source
                return self_source==other_split.join(other_source)
            if other_source_is_str:
                return self_split.join(self_source)==other_source
            return self_split.join(self_source)==other_split.join(other_source)
        return NotImplemented
    def __ne__(self, other:TextPartition):
        return not self.__eq__(other)
    def chunks(self) -> abcs.Iterator[str]:
        return map(self.split.join, self.split_chunks())
    def __iter__(self) -> abcs.Iterator[str]:
        return map(self.split.join, self.split_chunks())
    def chunks_wrapped(self, left:str, right:str) -> abcs.Iterator[str]:
        """Add a string to the left/before and the right/after of a chunk, before joining occurs
        Equivalent to (but better for memory) (f'{left}{split}{chunk}{split}{right}' for chunk in self.each_joined())
        Make sure you take into account the size of the split and the size of `left` and `right`
            Ex: Final size should be 2000, so TextPartition(source, size=2000 - 11 - 2, split='\n').chunks_wrapped('BEFORE', 'AFTER')
                                    11 is from the size of 'BEFORE' and 'AFTER' ^^   ^ 2 is from the two '\n's placed in between the `left` and `right` and the chunk
        """
        __self_split_join = self.split.join
        __yyfy = yyfy
        return (__self_split_join(__yyfy(left,chunk,right)) for chunk in self.split_chunks())
    def chunks_post_wrapped(self, left:str, right:str) -> abcs.Iterator[str]:
        """Add a string to the left/before and the right/after of each post processing
        Equivalent to (but better for memory) (f'{left}{chunk}{right}' for chunk in self.each_joined())
        Make sure you take into account the size of the size of `left` and `right`
            Ex: Final size should be 2000, so TextPartition(source, size=2000 - 10, split='\n').chunks_wrapped('before', 'after')
            Note: Each chunk will be beforeCHUNKHEREafter"""
        __self_split_join = self.split.join
        return (f"{left}{__self_split_join(chunk)}{right}" for chunk in self.split_chunks())
    def _lengths_unsafe(self) -> list[int] | array.array:
        """Do not use if `source` is a string!"""
        lengths:list[int] = list(map(len,self._source))
        __array = array.array
        for tc in ('H','I','L'): # try each unsigned: short, int, long
            try: lengths:array.array[int] = __array(tc, lengths)
            except OverflowError: continue
            else: break
        return lengths
    @staticmethod
    def _chunk_too_big() -> t.NoReturn:
        raise OverflowError("Chunk too big")
    def split_chunks(self) -> abcs.Iterator[list[str]]:
        first_size:t.Final = self.first_size
        source = self._source
        if isinstance(source, str):
            if first_size is not None: # we do none check because we want an empty str if it is 0, as that is expected
                yield source[:first_size] # get rid of the first part
                source = source[first_size:]
            if source:
                return map(list, PartitionLenUnsafe(source, self.size))
            return
        current_pack:list[str] = []
        __current_pack_append = current_pack.append
        text_length:int = 0
        tl_plus_lx:int
        lcp:int = 0
        ls:int = len(self.split)
        max_pack_size:t.Final[int] = self.max_chunk_size
        lengths:array.array[int] = self._lengths_unsafe()
        it:abcs.Iterator[tuple[str,int,int]] = zip(source, lengths, (yyf(first_size, itertools.repeat(self.size)) if first_size else itertools.repeat(self.size)))
        if max_pack_size:
            if self.lenient:
                # ------------------
                for x,lx,size in it: # type: str,int,int
                    # %%%%%%%%%
                    if lcp*ls + (tl_plus_lx:=text_length+lx) > size or max_pack_size <= lcp:
                    # %%%%%%%%%
                        yield current_pack
                        current_pack = [x]
                        __current_pack_append = current_pack.append
                        text_length = lx
                        lcp = 1
                    else:
                        text_length = tl_plus_lx
                        __current_pack_append(x)
                        lcp += 1
                # ------------------
            else:
                # ------------------
                for x,lx,size in it: # type: str,int,int
                    # %%%%%%%%%
                    if lcp*ls + (tl_plus_lx:=text_length+lx) > size or max_pack_size <= lcp: # this will just raise if lcp==0 only when lcp can even be zero
                        if lcp==0:
                            self._chunk_too_big()
                    # %%%%%%%%%
                        # print(sum(map(len, current_pack)), text_length) # works
                        # print((lcp-1)*ls + text_length, len(self.split.join(current_pack))) # works
                        yield current_pack
                        current_pack = [x]
                        __current_pack_append = current_pack.append
                        text_length = lx
                        lcp = 1
                    else:
                        text_length = tl_plus_lx
                        __current_pack_append(x)
                        lcp += 1
                # ------------------
        else:
            if self.lenient:
                # ------------------
                for x,lx,size in it: # type: str,int,int
                    # %%%%%%%%%
                    tl_plus_lx = text_length+lx
                    if lcp!=0 and lcp*ls + tl_plus_lx > size:
                    # %%%%%%%%%
                        yield current_pack
                        current_pack = [x]
                        __current_pack_append = current_pack.append
                        text_length = lx
                        lcp = 1
                    else:
                        text_length = tl_plus_lx
                        __current_pack_append(x)
                        lcp += 1
                # ------------------
            else:
                # ------------------
                for x,lx,size in it: # type: str,int,int
                    # %%%%%%%%%
                    if lcp*ls + (tl_plus_lx:=text_length+lx) > size:
                        if lcp==0:
                            self._chunk_too_big()
                    # %%%%%%%%%
                        # print(sum(map(len, current_pack)), text_length) # works
                        # print((lcp-1)*ls + text_length, len(self.split.join(current_pack))) # works
                        yield current_pack
                        current_pack = [x]
                        __current_pack_append = current_pack.append
                        text_length = lx
                        lcp = 1
                    else:
                        text_length = tl_plus_lx
                        __current_pack_append(x)
                        lcp += 1
                # ------------------
        if text_length: # !=0
            yield current_pack
