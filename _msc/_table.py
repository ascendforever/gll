from __future__ import annotations

__all__ = [
    'Table'
]

from gll.__common import *
from gll.__static import *


class Table:
    """Easy text table
    [Created 5/30/21]"""
    __slots__    = ('frame','_longest_each','joining', '__weakref__')
    __match_args__=('frame','_longest_each','joining')
    def __init__(self, /, *columns:abcs.Iterable[str], joining:str=' | '):
        self.frame:list[list[str]] = list(map(list, columns))
        self._longest_each:t.Optional[array.array[int]] = None
        self.joining:str = joining
    @property
    def longest_each(self) -> array.array[int]:
        if (__self__longest_each:=self._longest_each) is None:
            # noinspection PyShadowingNames
            all = builtins.all # noqa
            isinstance = builtins.isinstance # noqa
            str = builtins.str # noqa
            if not all(all(isinstance(cell, str) for cell in colu) for colu in self.frame):
                raise TypeError("All cells must be strings")
            self._longest_each = __self__longest_each = array.array('H', map(lenlongestfrom, self.frame)) # should not be edited
        return __self__longest_each
    @classmethod
    def from_frame(cls, frame:list[list[str]], joining:str=' | ') -> Table:
        self = cls.__new__(cls)
        self.frame = frame
        self._longest_each = None
        self.joining = joining
        return self
    @classmethod
    def lenient_source(cls, *columns:abcs.Iterable, joining:str=' | ') -> Table:
        self = cls.__new__(cls)
        # self.frame = list(multimap(list, functools.partial(map, str), it=columns))
        # self.frame = list(map(list, map(functools.partial(map,str), columns)))
        __str = str
        self.frame = [[__str(cell) for cell in col] for col in columns] # likely faster
        self._longest_each = None
        self.joining = joining
        return self
    def format_each(self, /, *formats:str) -> Table:
        """Formats each column according to format strings entered
        Format strings are given two variable, format position `0` will be the item and argument `size` will be the size the is required
        If more are provided than columns that exist, they are discarded
        If less are provided, the columns that don't get a format string, do not get formatted
        Returns `self`"""
        if (lfo:=len(formats)) > (lfr:=len(self.frame)): # it is slower to do this if this condition is true, but faster if it is false; since it will usually be false, we this condtion; if it will usually be true we should just do the slicing
            formats = formats[:lfr]
        elif lfo < lfr: # fill if we need to fill
            formats = itertools.chain(formats, itertools.repeat("{:<{size}}"))
        fmt:str; column:list[str]
        str_format = str.format
        self.frame = [
            [str_format(fmt, cell, item=cell, size=size) for cell in column] for fmt,column,size in zip(formats, self.frame, self.longest_each)
        ]
        return self
    def edit_column(self, column:int, func:abcs.Callable[[str,int], str]) -> Table:
        """Replace each object in a column with `func(object_in_column:Any, desired_size_of_column:int)`
        Returns `self`"""
        frame = self.frame
        try: frame[column] = list(map(func, frame[column], itertools.repeat(self.longest_each[column])))
        except IndexError: raise IndexError(f"Invalid column index {column}")
        return self
    def format_column(self, column:int, fmt:str= "{:<{size}}") -> Table:
        """Same as `Table.format_each`, but targets a single column
        Returns `self`"""
        try: size = self.longest_each[column]
        except IndexError: raise IndexError(f"Invalid column index {column}")
        str_format = str.format
        frame = self.frame
        frame[column] = [str_format(fmt, cell, item=cell, size=size) for cell in frame[column]]
        return self
    def format_all_auto(self) -> Table:
        """Slightly faster than `Table.format_each` with no arguments"""
        self.frame = [
            [f"{obj:<{size}}" for obj in column]
            for column,size in zip(self.frame, self.longest_each)
        ]
        return self
    def __repr__(self, /):
        return f"{self.__class__.__name__}.{self.from_frame.__name__}(frame={self.frame!r}, joining={self.joining!r})"
    def columns(self) -> abcs.Generator[list[str], t.Any, None]:
        yield from self.frame
    def rows(self) -> tuple[abcs.Iterator[str], ...]:
        return more_itertools.unzip(self.frame)
    def joined_rows(self) -> abcs.Iterator[str]:
        """Useful for when each row is massive in size;
        Better to use `Table.fmt_all_auto` and `Table.string` for speed"""
        return map(self.joining.join, self.rows())
    def __str__(self) -> str: return '\n'.join(self.joined_rows())
    if t.TYPE_CHECKING:
        def string (self) -> str: ...
    else: string = __str__
    def dump_low_memory(self, stream:t.textio=sys.stdout) -> none:
        """dump without creating as a string first - slower than normal .dump(), but won't create a string in memory
        leaves a trailing newline in stream"""
        # do not use typing.textio.writelines it is garbage
        __stream__write = stream.write
        __self_joining = self.joining
        for row in self.rows():
            for cell in list(row)[:-1]:
                __stream__write(cell)
                __stream__write(__self_joining)
            __stream__write(row[-1])
            __stream__write('\n')
    def dump(self, stream:t.textio=sys.stdout) -> none:
        """leaves a trailing newline in stream"""
        __stream__write = stream.write
        for line in self.joined_rows():
            __stream__write(line)
            __stream__write('\n')
    # def copy_deep(self, /) -> table: # unnecessary
    #     inst = self.__class__.__new__(self.__class__)
    #     inst.frame = (col.copy() for col in self.frame)
    #     inst.longest_each = array.array('h', self.longest_each)
    #     return inst
