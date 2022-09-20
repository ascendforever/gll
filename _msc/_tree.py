from __future__ import annotations

__all__ = [
    'Tree',
    'PathTree'
]

from gll.__common import *
from gll.__static import *



class Tree:
    """Tree representation for objects with children and sub children - most often used for file systems or command trees
    [Created 11/?/21]"""
    __slots__ = ('label','children','len_children','len_children_zero','desc','_cached_cumulative_children_count')
    __match_args__ = ('label','children','len_children','len_children_zero','desc','cumulative_children_count')
    def __init__(self, label:str, children:abcs.Sequence[Tree], desc:t.Optional[str]=None):
        self.label:str = label
        self.children:abcs.Sequence[Tree] = children
        self.len_children:t.Final[int] = (len_children := len(children))
        self.len_children_zero:t.Final[bool] = len_children==0
        self.desc:t.Optional[str] = desc
    def __repr__(self):
        __self_desc = self.desc
        return f"{self.__class__.__name__}({f'desc={__self_desc}, ' if __self_desc else ''}children={self.children!r})"
    @property
    @memorize_method_first
    def cumulative_children_count(self) -> int:
        """Cached"""
        return self._cumulative_children_count()
    def _cumulative_children_count(self) -> int:
        """Not cached"""
        return self.len_children + sum(map(self.__class__._cumulative_children_count, self.children))
    @classmethod
    def alt(cls, label:str, desc:t.Optional[str], children:abcs.Sequence[Tree]) -> Tree:
        """Alternative initiation method"""
        return cls(label,children,desc)
    if t.TYPE_CHECKING:
        @classmethod
        @t.overload
        def rootwrite(cls, stream_write:abcs.Callable[[str], t.Any], branches:abcs.Sequence[Tree], *,
                  desc_spacing:int=2, desc_size:int=100, indent:str='') -> None: ...
        @t.overload
        def rootwrite(self, stream_write:abcs.Callable[[str], t.Any], *,
                      desc_spacing:int=2, desc_size:int=100, indent:str='') -> None: ...
        def rootwrite(*args, **kwargs) -> None: ...
    else:
        @cidispatchmethod
        def rootwrite(self, stream_write:abcs.Callable[[str], t.Any], *,
                      desc_spacing:int=2, desc_size:int=100, indent:str='') -> None:
            """Write these tree nodes with no main root"""
            branches = self.children
            self.__class__._recur_root(stream_write, branches, len_branches=len(branches), desc_spacing=' '*desc_spacing, desc_size=desc_size, indent=indent)
        @rootwrite # noqa
        @classmethod
        def rootwrite(cls, stream_write:abcs.Callable[[str], t.Any], branches:abcs.Sequence[Tree], *,
                      desc_spacing:int=2, desc_size:int=100, indent:str='') -> None:
            """Write these tree nodes with no main root"""
            cls._recur_root(stream_write, branches, len_branches=len(branches), desc_spacing=' '*desc_spacing, desc_size=desc_size, indent=indent)
    @staticmethod
    def __rr_gs_lamb(child:Tree) -> bool:
        return child.len_children_zero
    @classmethod
    def _recur_root(cls, stream_write:abcs.Callable[[str], t.Any], branches:abcs.Sequence[Tree], *, len_branches:int, desc_spacing:str, desc_size:int, indent:str) -> None:
        __branches___getitem__ = branches.__getitem__
        __cls__recur = cls._recur
        max = builtins.max # noqa
        len = builtins.len # noqa
        for c_slice in group_sliced_true(cls.__rr_gs_lamb, branches): # type: slice
            children:abcs.Sequence[Tree] = __branches___getitem__(c_slice)
            biggest_child_label_padding = max(len(child.label) for child in children)
            final_c_i:int = c_slice.stop - c_slice.start - 1
            if c_slice.stop==len_branches: # if this slice ends on the final i of the branches, this group is the last
                for child in children[:final_c_i-1]: # all children except the last
                    __cls__recur(child, stream_write, label_padding=biggest_child_label_padding, desc_spacing=desc_spacing, desc_size=desc_size,
                                 indent=indent, final=False)
                __cls__recur(children[final_c_i], stream_write, label_padding=biggest_child_label_padding, desc_spacing=desc_spacing, desc_size=desc_size,
                             indent=indent, final=True)
            else:
                for child in children:
                    __cls__recur(child, stream_write, label_padding=biggest_child_label_padding, desc_spacing=desc_spacing, desc_size=desc_size,
                                 indent=indent, final=False)
    def write(self, stream_write:abcs.Callable[[str],t.Any], *,
                  label_padding:t.Optional[int]=None,
                  desc_spacing:int=2, desc_size:int=100, indent:str='', final:bool=False) -> None: # 0xffffff = 8**8-1
        """Write this tree node and its children"""
        if label_padding is None:
            label_padding:int = len(self.label)
        self._recur(stream_write, label_padding=label_padding, desc_spacing=' '*desc_spacing, desc_size=desc_size, final=final, indent=indent)
    def _recur(self, stream_write:abcs.Callable[[t.AnyStr], int], *,
                  label_padding:int,
                  desc_spacing:str, desc_size:int, indent:str, final:bool) -> None:
        len_children_zero:t.Final[bool] = self.len_children_zero
        pref:str = f'''{indent} {"└" if final else "├"}─{self.label:<{label_padding}}{desc_spacing}'''
        pref_pref_later:str = f"{indent} {' ' if final else '│'}"
        stream_write(pref)
        __self_desc:t.Final = self.desc
        if __self_desc is not None:
            if len(__self_desc) <= desc_size: # if the desc fits instantly # # likely faster so we don't need to construct a TextPartition
                stream_write(__self_desc)
                stream_write("\n") # final newline
            else:
                chunks_help:t.Final[abcs.Iterator[str]] = TextPartition(__self_desc, size=desc_size, split=' ').chunks()
                first_help:t.Final[str] = next(chunks_help, None)
                if first_help is not None:
                    stream_write(first_help)
                stream_write("\n") # final newline before help junk
                pref:str = f"{pref_pref_later} {' ' if len_children_zero else '│'} {' ' * (len(pref)-len(indent)-4)}"
                for chunk in chunks_help:
                    stream_write(pref)
                    stream_write(chunk)
                    stream_write('\n')
        else:
            stream_write("\n") # final newline
        if not len_children_zero:
            self.__class__._recur_root(stream_write, branches=self.children, len_branches=self.len_children, indent=pref_pref_later, desc_spacing=desc_spacing, desc_size=desc_size)
    def map(self, func:abcs.Callable[[Tree], None]):
        func(self)
        _map = self.__class__.map
        for child in self.children:
            _map(child, func)


def _get_path_sizer() -> proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path], int]]:
    @functools.lru_cache(maxsize=8192) # we clear manually, this is just in case
    def path_size(path:pathlib.Path) -> int:
        """Needs to be cleared manually"""
        if path.is_dir():
            return sum(map(path_size, path.iterdir()))
        return path.stat().st_size
    # noinspection PyTypeChecker
    return path_size

class PathTree(Tree):
    __slots__ = ('path','_cached_size',)
    __match_args__ = Tree.__match_args__ + ('path','size')
    if t.TYPE_CHECKING:
        def __init__(self, path:pathlib.Path, label:str, children:abcs.Sequence[PathTree], desc:t.Optional[str]=None):
            self.path:t.Final[pathlib.Path] = path
            super().__init__(label=label, children=children, desc=desc)
            self.children:abcs.Sequence[PathTree] = self.children # for type checker
    else:
        def __init__(self, path:pathlib.Path, label:str, children:abcs.Sequence[PathTree], desc:t.Optional[str]=None):
            self.path:t.Final[pathlib.Path] = path
            super().__init__(label=label, children=children, desc=desc)
    @property
    @memorize_method_first
    def size(self) -> int:
        """Cached"""
        return self._size()
    def _size(self) -> int:
        """Not cached"""
        if self.path.is_dir():
            return sum(tree.size for tree in self.children)
        return self.path.stat().st_size
    @classmethod
    def from_path(cls, path:pathlib.Path) -> PathTree:
        """Create from path"""
        children:abcs.Sequence[PathTree] = LazySeq(map(cls.from_path, path.iterdir())) if path.is_dir() else []
        return cls(path=path, label=path.name, children=children, desc=None)
    # noinspection PyShadowingBuiltins
    @classmethod
    def from_path_filtered(cls, path:pathlib.Path, filter:abcs.Callable[[pathlib.Path],bool]) -> PathTree:
        if path.is_dir():
            cls_from_path_filtered = cls.from_path_filtered
            children:abcs.Sequence[PathTree] = LazySeq(cls_from_path_filtered(child, filter) for child in builtins.filter(filter, path.iterdir()))
        else:
            children:abcs.Sequence[PathTree] = []
        return cls(path=path, label=path.name, children=children, desc=None)
    @classmethod
    def _from_path_sized(cls, path:pathlib.Path, min_size:t.Optional[int]=None, *, _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]], _size:t.Optional[int]=None) -> PathTree:
        if path.is_dir():
            __temp = cls._from_path_sized
            children:abcs.Sequence[PathTree] = LazySeq(__temp(child, min_size=min_size, _path_sizer=_path_sizer, _size=size) for child, size in ((child, _path_sizer(child)) for child in path.iterdir()) if size >= min_size)
        else:
            children:abcs.Sequence[PathTree] = []
        return cls(path=path, label=path.name, children=children, desc=None)
    @classmethod
    def from_path_sized(cls, path:pathlib.Path, min_size:t.Optional[int]=None, *, _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]], _size:t.Optional[int]=None) -> PathTree:
        """Same as .from_path, but has a minimum size; Also slower for the obvious added calculations"""
        try: res = cls._from_path_sized(path=path, min_size=min_size, _path_sizer=_path_sizer, _size=_size)
        finally: _path_sizer.cache_clear()
        return res
    # noinspection PyShadowingBuiltins
    @classmethod
    def _from_path_sized_filtered(cls, path:pathlib.Path, filter:t.Optional[abcs.Callable[[tuple[pathlib.Path, int]], bool]]=None,
                                 min_size:t.Optional[int]=None, *, _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]], _size:t.Optional[int]=None) -> PathTree:
        if path.is_dir():
            children:list[pathlib.Path] = list(path.iterdir())
            sizes:list[int] = list(map(_path_sizer, children))
            __temp = cls._from_path_sized_filtered
            children:abcs.Sequence[PathTree] = LazySeq(__temp(child, filter, min_size=min_size, _path_sizer=_path_sizer, _size=size) for child, size in builtins.filter(filter, zip(children, sizes)))
        else:
            children:abcs.Sequence[PathTree] = []
        return cls(path=path, label=path.name, children=children, desc=None)
    # noinspection PyShadowingBuiltins
    @classmethod
    def from_path_sized_filtered(cls, path:pathlib.Path, filter:t.Optional[abcs.Callable[[tuple[pathlib.Path, int]], bool]]=None,
                                 min_size:t.Optional[int]=None, _size:t.Optional[int]=None) -> PathTree:
        """Same as .from_path, but passes (path,total_size) to filter; Also slower for the obvious added calculations"""
        _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]] = _get_path_sizer()
        try: res = cls._from_path_sized_filtered(path=path,filter=filter,min_size=min_size,_path_sizer=_path_sizer,_size=_size)
        finally: _path_sizer.cache_clear()
        return res
    @classmethod
    def rootwrite_from_path_sized(cls, stream_write:abcs.Callable[[str], t.Any], path:pathlib.Path,
                  min_size:t.Optional[int]=None, _size:t.Optional[int]=None,
                  desc_spacing:int=2, desc_size:int=100, indent:str='') -> None:
        """Uses .rootwrite and .from_path_sized"""
        if path.is_dir():
            __temp = cls.from_path_sized
            _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]] = _get_path_sizer()
            try:
                children:abcs.Sequence[Tree] = [__temp(child, min_size=min_size, _path_sizer=_path_sizer, _size=_path_sizer(child)) for child in path.iterdir()]
            finally:
                _path_sizer.cache_clear()
        else: children:list[Tree] = []
        cls.rootwrite(stream_write, children, desc_spacing=desc_spacing, desc_size=desc_size, indent=indent)
    # noinspection PyShadowingBuiltins
    @classmethod
    def rootwrite_from_path_sized_filtered(cls, stream_write:abcs.Callable[[str], t.Any], path:pathlib.Path,
                  filter:t.Optional[abcs.Callable[[tuple[pathlib.Path,int]],bool]]=None,
                  min_size:t.Optional[int]=None, _size:t.Optional[int]=None,
                  desc_spacing:int=2, desc_size:int=100, indent:str='') -> None:
        """Uses .rootwrite and .from_path_sized_filtered"""
        if path.is_dir():
            __temp = cls.from_path_sized_filtered
            _path_sizer:proto.functools.LRUCacheWrapper[abcs.Callable[[pathlib.Path],int]] = _get_path_sizer()
            try: children:abcs.Sequence[Tree] = [__temp(child, filter, min_size=min_size, _size=_path_sizer(child)) for child in path.iterdir()]
            finally: _path_sizer.cache_clear()
        else: children:list[Tree] = []
        cls.rootwrite(stream_write, children, desc_spacing=desc_spacing, desc_size=desc_size, indent=indent)



















