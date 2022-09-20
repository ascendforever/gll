from __future__ import annotations

__all__ = [
    'TimeoutDict',
]

from gll.__common import *
from gll.__static import *


_KT = t.TypeVar('_KT')
_VT = t.TypeVar('_VT')

time_mod = time
class TimeoutDict(t.Generic[_KT, _VT], abcs.MutableMapping[_KT, _VT]):
    """
    Wrapper for dictionary of data and separate dictionary of timeouts (epoch times) in which entries in the main dictionary will be deleted
    [Created (3?4?5?)/?/21]
    """
    __slots__ = ('_data','_timeouts', '__weakref__')
    __match_args__ =('_data','_timeouts')
    def __init__(self, /, ordered:bool=False):
        if ordered:
            self._data:col.OrderedDict[_KT, _VT] = col.OrderedDict()
            # self._timeouts:weakref.WeakKeyDictionary[_KT, float] = weakref.WeakKeyDictionary()
            self._timeouts:col.OrderedDict[_KT, float] = col.OrderedDict() # cant use the above because then you wouldnt be able to use non mutable objects as keys
        else:
            self._data:dict[_KT, _VT] = {}
            # self._timeouts:weakref.WeakKeyDictionary[_KT, float] = weakref.WeakKeyDictionary()
            self._timeouts:dict[_KT, float] = {} # cant use the above because then you wouldnt be able to use non mutable objects as keys
        self._data:dict[_KT, _VT] # just so type checker knows, since col.OrderedDict is basically dict
        self._timeouts:dict[_KT, float]
    @classmethod
    def from_instances(cls, *instances:TimeoutDict[_KT,_VT], ordered:bool=False) -> TimeoutDict[_KT,_VT]:
        """Build from existing TimeoutDicts; Evaluate from right to left"""
        inst = cls(ordered=ordered)
        cls_update_from_other = cls.update_from_other
        for instance in reversed(instances):
            cls_update_from_other(inst, instance)
        return inst
    # noinspection PyShadowingNames
    @classmethod
    def from_time(cls, mapping:abcs.Mapping[_KT,_VT] | abcs.Iterable[tuple[_KT,_VT]],
                       time:float, ordered:bool=False) -> TimeoutDict[_KT,_VT]:
        """Returns a TimeoutDict with predefined data & timeouts all set to `time`"""
        return cls.from_mappings(mapping, ((k,time) for k in mapping.keys()), ordered=ordered)
    @classmethod
    def from_times(cls, mapping:abcs.Mapping[_KT,_VT] | abcs.Iterable[tuple[_KT,_VT]],
                       times:abcs.Iterable[float], ordered:bool=False) -> TimeoutDict[_KT,_VT]:
        """Returns a TimeoutDict with predefined data & timeouts each set from `times`"""
        return cls.from_mappings(mapping, zip(mapping.keys(), times), ordered=ordered)
    @classmethod
    def from_mappings(cls, mapping:abcs.Mapping[_KT,   _VT] | abcs.Iterable[tuple[_KT,   _VT]],
                          timeouts:abcs.Mapping[_KT, float] | abcs.Iterable[tuple[_KT, float]], ordered:bool=False) -> TimeoutDict[_KT,_VT]:
        """Returns a TimeoutDict with predefined data & timeouts"""
        self = cls.__new__(cls)
        if ordered:
            self._data = col.OrderedDict(mapping)
            self._timeouts = col.OrderedDict(timeouts)
        else:
            self._data = dict(mapping)
            self._timeouts = dict(timeouts)
        return self
    def __repr__(self, /) -> str:                                                                           # this way of converting to str is slower, but will consume less memory of course
        return f"{self.__class__.__name__}.{self.__class__.from_time.__name__}(mapping={self._data!r}, time=[{', '.join(map(str, self._timeouts.values()))}])"
    def __str__(self, /) -> str:
        return str(self._data)
    # def __hash__(self, /) -> int:
    #     return hash((self._data,self._timeouts))
    def hash_data(self) -> int:
        return hash(self._data)
    def hash_timeouts(self) -> int:
        return hash(self._timeouts)
    def clear(self, /) -> None:
        self._data.clear()
        self._timeouts.clear()
    def __contains__(self, /, item:_KT) -> bool:
        return item in self._data
    def contains_timeout(self, /, item:float):
        return item in self._timeouts.values()
    def __iter__(self, /) -> abcs.KeysView[_KT]:
        return self._data.keys()
    def timeout_values(self) -> abcs.ValuesView[float]:
        return self._timeouts.values()
    def __len__(self, /) -> int:
        return len(self._data)
    def __reversed__(self, /) -> abcs.Iterator[_KT]:
        """Useless, unless underlying mappings are ordered"""
        return reversed(self._data.keys())
    def keys(self, /) -> abcs.KeysView[_KT]:
        return self._data.keys()
    def values(self, /) -> abcs.ValuesView[_VT]:
        return self._data.values()
    def items(self, /) -> abcs.ItemsView[_KT, _VT]:
        return self._data.items()
    # @property
    # @memorized_method
    def data(self, /) -> types.MappingProxyType[_KT, _VT]:
        """Immutable view of underlying data; Immutability should not be circumvented"""
        return types.MappingProxyType(self._data)
    # @property
    # @memorized_method
    def timeouts(self, /) -> types.MappingProxyType[_KT, _VT]:
        """Immutable view of underlying data; Immutability should not be circumvented"""
        return types.MappingProxyType(self._timeouts)
    def check(self) -> None:
        return self.check_from(time.time())
    def check_from(self, now:float) -> None:
        # for k,v in list(self._timeouts.items()): # type: _KT,float
        #     if now > v: # if we are past timeout
        #         del self._data[k]
        #         del self._timeouts[k]
        self._timeouts = self._timeouts.__class__((k,v) for k,v in self._timeouts.items() if v < now) # cant use dict construct, because we may be using col.OrderedDict
        self_timeouts = self._timeouts
        self._data = self._data.__class__((k,v) for k,v in self._data.items() if k in self_timeouts)
    def __getitem__(self, /, item:_KT) -> _VT:
        return self._data[item]
    @t.overload
    def get(self, /, item:_KT) -> _VT: ...
    @t.overload
    def get(self, /, item:_KT, default:T=sentinel) -> _VT|T: ...
    def get(self, /, item:_KT, default:T=sentinel) -> _VT|T:
        if default is sentinel:
            return self._data[item]
        return self._data.get(item, default)
    def get_timeout(self, /, item:_KT, default=sentinel) -> float:
        if default is sentinel:
            return self._timeouts[item]
        return self._timeouts.get(item, default)
    def __setitem__(self, /, key:_KT, value:tuple[_VT, float]) -> None:
        self._data[key] = value[0]
        self._timeouts[key] = value[1]
    def setitem(self, /, key:_KT, value:_VT, time:t.Optional[float]=None) -> None: # noqa shadowing
        self._data[key] = value
        self._timeouts[key] = time_mod.time() if time is None else time
    def __delitem__(self, /, key:_KT) -> None:
        del self._data[key]
        del self._timeouts[key]
    @functools.wraps(abcs.MutableMapping.pop)
    def pop(self, /, *args,**kwargs):
        res = super().pop(*args,**kwargs)
        self._timeouts.pop(*args,**kwargs)
        return res
    @t.overload
    def update(self, /, data:TimeoutDict[_KT, _VT]) -> None: ... # noqa method overriding
    @t.overload
    def update(self, /, data:abcs.Mapping[_KT, _VT], timeouts:abcs.Mapping[_KT, float]) -> None: ... # noqa method overriding
    def update(self, /, data:TimeoutDict[_KT,_VT] | abcs.Mapping[_KT,_VT], timeouts:None|abcs.Mapping[_KT, float]=None) -> None:
        if isinstance(data, self.__class__):
            self._data.update(data._data)
            self._timeouts.update(data._timeouts)
        else:
            self._data.update(data)
            self._timeouts.update(timeouts)
    def update_from_other(self, /, data:TimeoutDict[_KT, _VT]) -> None:
        self._data.update(data._data)
        self._timeouts.update(data._timeouts)
    def update_from_mappings(self, /, data:abcs.Mapping[_KT, _VT  ] | abcs.Iterable[tuple[_KT, _VT  ]],
                               timeouts:abcs.Mapping[_KT, float] | abcs.Iterable[tuple[_KT, float]]):
        self._data.update(data)
        self._timeouts.update(timeouts)
    def copy(self, /) -> TimeoutDict[_KT, _VT]:
        inst = self.__class__.__new__(self.__class__)
        inst._data = self._data.copy()
        inst._timeouts = self._timeouts.copy()
        return inst
    def deepcopy(self, /) -> TimeoutDict[_KT, _VT]:
        inst = self.__class__.__new__(self.__class__)
        inst._data = copy.deepcopy(self._data)
        inst._timeouts = copy.deepcopy(self._timeouts)
        return inst






