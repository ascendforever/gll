from __future__ import annotations

__all__ = [
    'SuperAsync',
    'SuperAsyncList',
    'SuperAsyncSafe',
    'SuperAsyncListSafe',
    'AsyncTasks',
    'nullasynccontext',
]

from gll.__common import *
from gll.__static import *
from .__Cstatic import *

# # OLD
# class AsyncManager(t.Generic[T], abcs.Sized, abcs.Container[abcs.Awaitable[T]], abcs.Awaitable[T]):
#     """
#     Handle a collection of awaitables
#     [Created 5/?/21]
#     """
#     __slots__ = ('_aws', '_emptied', '_awaited', '__weakref__')
#     def __init__(self, /, awaitables:abcs.Iterable[abcs.Awaitable[T]], single_use:bool=True, _emptied:bool=False, _already_awaited:bool=False):
#         """Do not modify keyword args with _ in the beginning"""
#         if single_use:
#             self._aws:abcs.Iterator[abcs.Awaitable[T]] = iter(awaitables)
#         else:
#             self._aws:list[abcs.Awaitable[T]] = list(awaitables)
#         self._emptied:bool = _emptied
#         self._awaited:bool = _already_awaited
#     @classmethod
#     def unsafe(cls, awaitables:t.Union[abcs.Iterator[abcs.Awaitable[T]], list[abcs.Awaitable[T]]], _emptied:bool=False, _already_awaited:bool=False):
#         """Use this if you know that `awaitables` is an iterator/list that won't be used outside of this instance"""
#         self = cls.__new__(cls)
#         self._aws = awaitables
#         self._emptied = _emptied
#         self._awaited = _already_awaited
#         return self
#     def __repr__(self, /):
#         return f"{self.__class__.__name__}({self._aws!r}, single_use={isinstance(self._aws, list)}, _emptied={self._emptied}, _already_awaited={self._awaited})"
#     def extend(self, /, *aws:abcs.Iterable[abcs.Awaitable[T]], guaranteed_extension:bool=False) -> AsyncManager[T]:
#         """Extend self by each iterable
#         `guaranteed_extension` should be true if it is absolutely guaranteed that a non empty iterable will be passed
#         Returns self"""
#         if isinstance(self._aws, list):
#             self_aws = self._aws
#             for aw_s in aws: # type: abcs.Iterable[abcs.Awaitable[T]]
#                 self_aws.extend(aw_s)
#             del self_aws
#         else:
#             self._aws:abcs.Iterator[abcs.Awaitable[T]] = itertools.chain.from_iterable(yyf(self._aws, aws))
#             if guaranteed_extension:
#                 self._emptied = False
#             elif self._emptied:
#                 for aw_len in (len(aw) for aw in aws if isinstance(aw, abcs.Sized)): # type: int
#                     if aw_len!=0:
#                         self._emptied = False
#                         break
#                 else:
#                     try: first:abcs.Awaitable[T] = next(self._aws) # this may be better than the comment block below
#                     except StopIteration: pass
#                     else:
#                         self._aws = yyf(first, self._aws)
#                         self._emptied = False
#                     # self._aws,tee = itertools.tee(self._aws, 2)
#                     # try: next(tee)
#                     # except StopIteration: pass
#                     # else: self._emptied = False # means we did indeed make ourselves not empty
#         return self
#     def __await__(self, /) -> abcs.Generator[t.Any,t.Any,None]:
#         return self.execute().__await__()
#     def __len__(self, /) -> int:
#         if self.single_use:
#             raise TypeError("Cannot retrieve length of single use AsyncManager; Consider converting using AsyncManager.make_reusable(...)")
#         return len(self._aws)
#     def __contains__(self, /, aw) -> bool: # for some dumb reason we can't type hint this
#         if self.single_use:
#             raise TypeError("Cannot check containing of an item of single use AsyncManager; Consider converting using AsyncManager.make_reusable(...)")
#         return aw in self._aws
#     @classmethod
#     def using_list(cls, /, awaitables:list[abcs.Awaitable[T]], _already_awaited:bool=False) -> AsyncManager[T]:
#         """Create **using** an existing list; no new list is generated"""
#         inst = cls.__new__(cls)
#         inst._aws = awaitables
#         inst._emptied = False
#         inst._awaited = _already_awaited
#         return inst
#     @classmethod
#     def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable, single_use:bool=True) -> AsyncManager[T]:
#         inst = cls.__new__(cls)
#         _aws = map(func, *iterables)
#         if not single_use:
#             _aws = list(_aws)
#         inst._aws = _aws
#         inst._emptied = False
#         inst._awaited = False
#         return inst
#     def make_reusable(self, /) -> AsyncManager[T]:
#         self_aws = self._aws
#         if isinstance(self_aws, abcs.Iterator):
#             self._aws = list(self_aws)
#             self._emptied = False # len(self._aws)==0 # Cuz it will be empty! # NOTE : do not uncomment this - Emptied should always be false for non-single-use
#         return self
#     def make_single_use(self, /) -> AsyncManager[T]:
#         self_aws = self._aws
#         if isinstance(self_aws, list):
#             if len(self_aws)==0:
#                 self._emptied = True # because it will be!
#             self._aws = iter(self_aws)
#         return self
#     def clear(self, /) -> None:
#         if self.single_use:
#             for _ in self._aws:
#                 pass
#         else:
#             self._aws.clear()
#         self._emptied = True
#     def aws_not_single_use(self, /) -> list[abcs.Awaitable[T]]:
#         """Use if single use guaranteed not true"""
#         return self._aws
#     def aws_for_awaiting_not_single_use(self, /) -> list[abcs.Awaitable[T]]:
#         """Use if single use guaranteed not true"""
#         if self._awaited:
#             raise RuntimeError("Coroutines have already awaited")
#         self._awaited = True
#         return self._aws
#     def aws_for_awaiting(self, /) -> abcs.Iterable[abcs.Awaitable[T]] | list[abcs.Awaitable[T]]]:#         """Handles getting awaitables for awaiting"""
#         if self.single_use:
#             if self._emptied:
#                 raise StopIteration("Contents already iterated")
#             self._emptied = True
#         if self._awaited:
#             # # async def corof(): pass
#             # # async def main():
#             # #     coro = corof()
#             # #     await coro
#             # #     await coro
#             # # asyncio.run(main())
#             # # RuntimeError: cannot reuse already awaited coroutine
#             # This is a RuntimeError because ^^^^^^^^^^
#             raise RuntimeError("Coroutines have already awaited")
#         self._awaited = True
#         return self._aws
#     def aws(self, /) -> abcs.Iterable[abcs.Awaitable[T]] | list[abcs.Awaitable[T]]]:#         """Handles getting awaitables NOT FOR AWAITING"""
#         if self.single_use:
#             if self._emptied:
#                 raise StopIteration("Contents already iterated")
#             self._emptied = True
#         return self._aws
#     @property
#     def awaited(self, /) -> bool:
#         """Returns whether or not contents have been awaited
#         Does not need to be used for checks, because it is handled within AsyncManager.aws(...)"""
#         return self._awaited
#     @property
#     def emptied(self, /) -> bool:
#         """Whether or not the contents have been consumed
#         If not `single_use`, then this is always False"""
#         return self._emptied
#     @property
#     def single_use(self, /) -> bool:
#         return isinstance(self._aws, abcs.Iterator)
#     async def await_each(self, /) -> abcs.AsyncGenerator[T, t.Any, None]:
#         """Equivalent to `(await coro for coro in self.aws(for_awaiting=True))`"""
#         for coro in self.aws_for_awaiting():
#             yield await coro
#     def gather(self, /) -> asyncio.Future[list[T|BaseException]]:
#         """Returns `asyncio.gather(*self.aws())`"""
#         return asyncio.gather(*self.aws_for_awaiting())
#     def chunked_gather(self, /, chunk_sizes:int) -> AsyncManager[tuple[T|BaseException,...]]:
#         """Gather in chunks - makes self reusable"""
#         self.make_reusable()
#         aws:list[abcs.Awaitable] = self.aws_for_awaiting_not_single_use()
#         asyncio_gather = asyncio.gather
#         # coros:abcs.Generator[abcs.Awaitable[list[T]], t.Any, None] = (asyncio_gather(*chunk) for chunk in PartitionLen(aws, chunk_sizes))
#         coros:abcs.Iterator[asyncio.Future[tuple[T|BaseException,...]]] = itertools.starmap(asyncio_gather, PartitionLen(aws, chunk_sizes))
#         return AsyncManager(coros, single_use=self.single_use)
#     def as_completed(self, /, timeout:t.Optional[float]=None) -> abcs.Iterator[asyncio.Future[T]]:
#         return asyncio.as_completed(self.aws_for_awaiting(), timeout=timeout)
#     async def flatten(self, /) -> list[T]:
#         return [await coro for coro in self.aws_for_awaiting()]
#     async def execute(self, /) -> None:
#         for coro in self.aws_for_awaiting():
#             await coro
#     def to_tasks(self, /, rename_tasks:bool=True) -> AsyncTasks[T]:
#         return AsyncTasks(self.aws_for_awaiting(), rename_tasks=rename_tasks)

# └ ┌  ┐ ┘ ─ │ ┴ ┬ ┼

#                   SABaseRoot
#          ┌────────────┴─────────┐
#     SASafeBase    SAStdBase    SAFastBase
#  ┌───┘   └────┬────┘     └────┬─┘      └┐
#  │ SuperAsyncSafe SAListBase SuperAsync │
#  └────────┬────────┘      └─┬───────────┘
#    SuperAsyncListSafe    SuperAsyncList


class SABaseRoot(t.Generic[T], abcs.Awaitable[T], metaclass=abc.ABCMeta):
    """
    Handle a collection of awaitable
    Root implementation
    all subclasses should define a property/attribute called `aws`
    [Created 11/12/21] // original all-encompassing class created 5/?/21"""
    __slots__ = ('__weakref__',)
    @classmethod
    @abc.abstractmethod
    def safe(cls, awaitables:abcs.Iterable[abcs.Awaitable[T]]) -> SABaseRoot[T]:
        """Use if awaitables is not guaranteed to be the proper type"""
    @classmethod
    @abc.abstractmethod
    def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SABaseRoot[T]:
        """Same as `cls(map(func,*iterables), ...)`"""
    @classmethod
    @abc.abstractmethod
    def starmap(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SABaseRoot[T]:
        """Same as `cls(itertools.starmap(func,*iterables), ...)`"""
        ...
    @abc.abstractmethod
    def map_inplace(self, func:abcs.Callable[[abcs.Awaitable[T]],abcs.Awaitable[T]]) -> SABaseRoot[T]:
        """Map inplace - returns `self`"""
    @abc.abstractmethod
    def __repr__(self, /): ...
    @t.final
    def __await__(self, /) -> abcs.Generator[t.Any,t.Any,None]:
        """Same as calling `self.execute()`"""
        return self.execute().__await__()
    @abc.abstractmethod
    def append(self, /, aw:abcs.Awaitable[T]) -> SASafeBase[T]:
        """Append an awaitable to the end - costly, prefer using `self.extend` if multiple appends are needed"""
    @abc.abstractmethod
    def extend(self, /, *aws:abcs.Iterable[abcs.Awaitable[T]]) -> SABaseRoot[T]: ...
    @abc.abstractmethod
    def clear(self, /) -> None: ...
    @abc.abstractmethod
    async def await_each(self, /) -> abcs.AsyncGenerator[T, t.Any, None]:
        ... # docstring in subclass
    @abc.abstractmethod
    def gather(self, /) -> asyncio.Future[tuple[T|BaseException,...]]:
        ... # docstring in subclass
    @abc.abstractmethod
    def chunked_gather(self, /, chunk_sizes:int) -> SuperAsync[tuple[T|BaseException, ...]]: ...
    @abc.abstractmethod
    def partitioned_gather(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException, ...]]: ...
    @abc.abstractmethod
    def chunked_gather_safe(self, /, chunk_sizes:int) -> SuperAsync[tuple[T|BaseException, ...]]:
        """Use if `chunk_sizes` could be less than 1"""
    @abc.abstractmethod
    def partitioned_gather_safe(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException, ...]]:
        """Use if `chunks` could be less than 1"""
    @abc.abstractmethod
    def as_completed(self, /, timeout:t.Optional[float]=None) -> abcs.Iterator[asyncio.Future[T]]:
        ... # docstring in subclass
    @abc.abstractmethod
    async def flatten(self, /) -> list[T]:
        """await each and flatten to list"""
    @abc.abstractmethod
    async def execute(self, /) -> None:
        """await each and exit"""
    @abc.abstractmethod
    def to_tasks(self, /, rename_tasks:bool=True) -> AsyncTasks[T]:
        """Pass data to AsyncTasks; instance probably should not be used afterwards"""


def _gather_common(partitioner:t.Literal[PartitionLenUnsafe,partition_unsafe,partition_ultra_unsafe,PartitionLen,partition], aws:list[abcs.Awaitable[T]], sizes:int) -> list[abcs.Awaitable[tuple[T|BaseException, ...]]]:
    return list(itertools.starmap(asyncio.gather, partitioner(aws, sizes)))

class SASafeBase(t.Generic[T], SABaseRoot[T], metaclass=abc.ABCMeta):
    """Use subclasses if source awaitables are shared by other areas of code, and awaiting/iteration may be performed outside of instance"""
    def __init_subclass__(cls, **kwargs):
        if not '_awaited' in cls.__slots__:
            raise TypeError(f"`_awaited` must be in __slots__; {cls.__qualname__}")
    # __slots__ = ('_awaited')
    __slots__ = ()
    # noqa
    @abc.abstractmethod
    def to_fast(self, /) -> SAFastBase[T]:
        """Convert to 'Fast' counterpart"""
    @property
    @abc.abstractmethod
    def aws_for_awaiting(self, /) -> abcs.Iterable[abcs.Awaitable[T]] | list[abcs.Awaitable[T]]:
        """Handles getting awaitables for awaiting"""
    @property
    @t.final
    def awaited(self, /) -> bool:
        """Returns whether or not contents have been awaited
        Does not need to be used for checks, because it is handled within AsyncManager.aws(...)"""
        return self._awaited
    @t.final
    async def await_each(self, /) -> abcs.AsyncGenerator[T, t.Any, None]:
        """Equivalent to `(await coro for coro in self.aws_for_awaiting)`"""
        for coro in self.aws_for_awaiting:
            yield await coro
    @t.final
    def gather(self, /) -> asyncio.Future[tuple[T|BaseException,...]]:
        """Returns `asyncio.gather(*self.aws_for_awaiting)`"""
        return asyncio.gather(*self.aws_for_awaiting)
    @t.final
    def as_completed(self, /, timeout:None|float=None) -> abcs.Iterator[asyncio.Future[T]]:
        """Same as `asyncio.as_completed(self.aws_for_awaiting, timeout=timeout)`"""
        return asyncio.as_completed(self.aws_for_awaiting, timeout=timeout)
    @t.final
    async def flatten(self, /) -> list[T]:
        return [await coro for coro in self.aws_for_awaiting]
    @t.final
    async def execute(self, /) -> None:
        for coro in self.aws_for_awaiting:
            await coro
    @t.final
    def to_tasks(self, /, rename_tasks:bool=True) -> AsyncTasks[T]:
        return AsyncTasks(self.aws_for_awaiting, rename_tasks=rename_tasks)
class SAFastBase(t.Generic[T], SABaseRoot[T], abcs.Iterable[abcs.Awaitable[T]], metaclass=abc.ABCMeta):
    __slots__ = ('aws',) if t.TYPE_CHECKING else ()
    def __init_subclass__(cls, **kwargs):
        if 'aws' not in cls.__slots__:
            raise TypeError(f"`aws` must be in __slots__; {cls.__qualname__}")
    @abc.abstractmethod
    def __iter__(self) -> abcs.Iterator[abcs.Awaitable[T]]:
        ...
    @abc.abstractmethod
    def to_safe(self, /) -> SASafeBase[T]:
        """Convert to 'Safe' counterpart"""
    @t.final
    def __repr__(self, /):
        return f"{self.__class__.__name__}({self.aws!r})"
    @t.final
    async def await_each(self, /) -> abcs.AsyncGenerator[T, t.Any, None]:
        """Equivalent to `(await coro for coro in self.aws)`"""
        for coro in self.aws:
            yield await coro
    @t.final
    def gather(self, /) -> asyncio.Future[tuple[T|BaseException,...]]:
        """Returns `asyncio.gather(*self.aws)`"""
        return asyncio.gather(*self.aws)
    @t.final
    def as_completed(self, /, timeout:None|float=None) -> abcs.Iterator[asyncio.Future[T]]:
        """Same as `asyncio.as_completed(self.aws, timeout=timeout)`"""
        return asyncio.as_completed(self.aws, timeout=timeout)
    @t.final
    async def flatten(self, /) -> list[T]:
        return [await coro for coro in self.aws]
    @t.final
    async def execute(self, /) -> None:
        for coro in self.aws:
            await coro
    @t.final
    def to_tasks(self, /, rename_tasks:bool=True) -> AsyncTasks[T]:
        return AsyncTasks(self.aws, rename_tasks=rename_tasks)
# above two are mutually exclusive as well as the below two
class SAListBase(t.Generic[T], abcs.Sized, abcs.Container[abcs.Awaitable[T]], metaclass=abc.ABCMeta):
    """Same as standard counterpart but uses list as underlying data type rather than an iterator
    Much faster for `.append` as this gets piped down to `list.append`
    [Created 11/12/21]"""
    __slots__ = ('aws',) if t.TYPE_CHECKING else ()
    def __init_subclass__(cls, **kwargs):
        if 'aws' not in cls.__slots__:
            raise TypeError(f"`aws` must be in __slots__; {cls.__qualname__}")
    @t.final
    def to_std_fast(self, /) -> SuperAsync[T]:
        return SuperAsync(iter(self.aws))
    @t.final
    def to_std_safe(self, /) -> SuperAsyncSafe[T]:
        return SuperAsyncSafe(iter(self.aws))
    @t.final
    def __len__(self, /) -> int:
        return len(self.aws)
    @t.final
    def __contains__(self, /, aw) -> bool: # for some dumb reason we can't type hint this
        return aw in self.aws
    @t.final
    def extend(self, /, *aws:abcs.Iterable[abcs.Awaitable[T]]):
        __self__aws_extend = self.aws.extend
        for aw_s in aws: # type: abcs.Iterable[abcs.Awaitable[T]]
            __self__aws_extend(aw_s)
        return self
    @t.final
    def append(self, /, aw:abcs.Awaitable[T]):
        self.aws.append(aw)
        return self
    @t.final
    def clear(self, /) -> None:
        self.aws.clear()
    @t.final
    def map_inplace(self, func:abcs.Callable[[abcs.Awaitable[T]],abcs.Awaitable[T]]):
        # noinspection PyAttributeOutsideInit
        self.aws = list(map(func, self.aws))
        return self
class SAStdBase (t.Generic[T], metaclass=abc.ABCMeta):
    __slots__ = ()
    def __init_subclass__(cls, **kwargs):
        if 'aws' not in cls.__slots__ and not isinstance(vars(cls).get('aws'), property):
            raise TypeError(f"`aws` must be in __slots__ or be a property; {cls.__qualname__}")
    @t.final
    def map_inplace(self, func:abcs.Callable[[abcs.Awaitable[T]],abcs.Awaitable[T]]):
        # noinspection PyAttributeOutsideInit
        self.aws = map(func, self.aws)
        return self

class SuperAsync    (t.Generic[T], SAFastBase[T], SAStdBase[T], abcs.Iterator[abcs.Awaitable[T]]):
    """Fastest of all counterparts
    [Created 11/12/21]"""
    map_inplace = SAStdBase.map_inplace # for IDE to understand
    __slots__ = __match_args__ = ('aws',)
    def __init__(self, /, awaitables:abcs.Iterator[abcs.Awaitable[T]]):
        self.aws:abcs.Iterator[abcs.Awaitable[T]] = awaitables
    def chunked_gather(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLenUnsafe(list(self.aws), chunk_sizes)))
    def partitioned_gather(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition_unsafe(list(self.aws), chunks     )))
    def chunked_gather_safe(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLen(list(self.aws), chunk_sizes)))
    def partitioned_gather_safe(self,/,chunks:int)->SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition    (list(self.aws), chunks)))
    def __next__(self) -> abcs.Awaitable[T]:
        return next(self.aws)
    def __iter__(self) -> abcs.Iterator[abcs.Awaitable[T]]:
        return self.aws
    @classmethod
    def safe(cls, awaitables:abcs.Iterable[abcs.Awaitable[T]]) -> SuperAsync[T]: # noqa crying not same args as base
        self = cls.__new__(cls)
        self.aws = iter(awaitables)
        return self
    @classmethod
    def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsync[T]:
        inst = cls.__new__(cls)
        inst.aws = map(func, *iterables)
        return inst
    @classmethod
    def multi_map(cls, /, final:abcs.Callable[[t.Any], abcs.Coroutine[t.Any,t.Any,T]], *funcs:abcs.Callable[[t.Any], t.Any], it:abcs.Iterable) -> SuperAsync[T]:
        inst = cls.__new__(cls)
        inst.aws = iter(multimap(final, *funcs, it=it))
        return inst
    @classmethod
    def starmap(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], iterable:abcs.Iterable) -> SuperAsync[T]:
        inst = cls.__new__(cls)
        inst.aws = itertools.starmap(func, iterable)
        return inst
    def to_safe(self, /) -> SuperAsyncSafe[T]:
        return SuperAsyncSafe(self.aws)
    def to_salist(self, /) -> SuperAsyncList[T]:
        return SuperAsyncList(list(self.aws))
    def to_salist_safe(self, /) -> SuperAsyncListSafe[T]:
        return SuperAsyncListSafe(list(self.aws))
    def append(self, /, aw:abcs.Awaitable[T]) -> SuperAsync[T]:
        self.aws:abcs.Iterator[abcs.Awaitable[T]] = yfy(self.aws, aw)
        return self
    def extend(self, /, *aws:abcs.Iterable[abcs.Awaitable[T]]) -> SuperAsync[T]:
        self.aws:abcs.Iterator[abcs.Awaitable[T]] = itertools.chain.from_iterable(yyf(self.aws, aws))
        return self
    def clear(self, /) -> None:
        for _ in self.aws: pass
class SuperAsyncSafe(t.Generic[T], SASafeBase[T], SAStdBase[T]):
    """Same as SuperAsync but watches whether contents have been emptied or awaited already - unnecessary if you know what you are doing
    [Created 11/12/21]"""
    map_inplace = SAStdBase.map_inplace # for IDE to understand
    __slots__ = ('_aws', '_awaited')
    # __match_args__ =
    def __init__(self, /, awaitables:abcs.Iterator[abcs.Awaitable[T]], _already_awaited:bool=False):
        self._aws:SmartIterator[abcs.Awaitable[T]] = SmartIterator(awaitables)
        self._awaited:bool = _already_awaited
    def chunked_gather(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLenUnsafe(list(self.aws_for_awaiting), chunk_sizes)))
    def partitioned_gather(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition_unsafe(list(self.aws_for_awaiting), chunks     )))
    def chunked_gather_safe(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLen(list(self.aws_for_awaiting), chunk_sizes)))
    def partitioned_gather_safe(self,/,chunks:int)->SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition    (list(self.aws_for_awaiting), chunks)))
    @property
    def emptied(self, /) -> bool:
        """Whether or not the contents have been consumed"""
        return not self._aws
    @property
    def aws(self, /) -> abcs.Iterable[abcs.Awaitable[T]] | list[abcs.Awaitable[T]]:
        if not (aws:=self._aws):
            raise StopIteration("Contents already iterated")
        return aws
    @property
    def aws_for_awaiting(self, /) -> abcs.Iterable[abcs.Awaitable[T]] | list[abcs.Awaitable[T]]:
        if not (aws:=self._aws):
            raise StopIteration("Contents already iterated")
        if self._awaited:
            # # async def corof(): pass
            # # async def main():
            # #     coro = corof()
            # #     await coro
            # #     await coro
            # # asyncio.run(main())
            # # RuntimeError: cannot reuse already awaited coroutine
            # This is a RuntimeError because ^^^^^^^^^^
            raise RuntimeError("Coroutines have already awaited")
        self._awaited = True
        return aws
    def __repr__(self, /):
        return f"{self.__class__.__name__}({self._aws!r}, _already_awaited={self._awaited})"
    @classmethod
    def safe(cls, awaitables:abcs.Iterable[abcs.Awaitable[T]], _emptied:bool=False, _already_awaited:bool=False):
        self = cls.__new__(cls)
        self._aws = iter(awaitables)
        self._emptied=_emptied
        self._awaited = _already_awaited
        return self
    @classmethod
    def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncSafe[T]:
        inst = cls.__new__(cls)
        inst._aws = smart_iterator_from_raw(map(func, *iterables))
        inst._awaited = False
        return inst
    @classmethod
    def starmap(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncSafe[T]:
        inst = cls.__new__(cls)
        inst._aws = smart_iterator_from_raw(itertools.starmap(func, *iterables))
        inst._awaited = False
        return inst
    def to_fast(self, /) -> SuperAsync[T]:
        return SuperAsync(self._aws)
    def to_salist_fast(self, /) -> SuperAsyncList[T]:
        return SuperAsyncList(list(self._aws))
    def to_salist(self, /) -> SuperAsyncListSafe[T]:
        return SuperAsyncListSafe(list(self._aws))
    def append(self, /, aw:abcs.Awaitable[T]) -> SuperAsyncSafe[T]:
        self._aws:abcs.Iterator[abcs.Awaitable[T]] = smart_iterator_from_raw(yfy(self._aws.iter_unsafe(), aw))
        return self
    def extend(self, /, *aws:abcs.Iterable[abcs.Awaitable[T]], guaranteed_extension:bool=False) -> SuperAsyncSafe[T]:
        self._aws:SmartIterator[abcs.Awaitable[T]] = smart_iterator_from_raw(itertools.chain.from_iterable(yyf(self._aws.iter_unsafe(), aws)))
        return self
    def clear(self, /) -> None:
        for _ in self._aws: pass

class SuperAsyncList    (t.Generic[T], SAFastBase[T], SAListBase[T]):
    extend = SAListBase.extend # for IDE to understand
    append = SAListBase.append # for IDE to understand
    clear  = SAListBase.clear # for IDE to understand
    map_inplace = SAListBase.map_inplace # for IDE to understand
    __slots__ = __match_args__ = ('aws',)
    def __init__(self, /, awaitables:list[abcs.Awaitable[T]]):
        self.aws:list[abcs.Awaitable[T]] = awaitables
    def chunked_gather(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLenUnsafe(self.aws, chunk_sizes)))
    def partitioned_gather(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition_unsafe(self.aws, chunks     )))
    def chunked_gather_safe(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLen(self.aws, chunk_sizes)))
    def partitioned_gather_safe(self,/,chunks:int)->SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition    (self.aws, chunks)))
    def __iter__(self) -> abcs.Iterator[abcs.Awaitable[T]]:
        return iter(self.aws)
    @classmethod
    def safe(cls, awaitables:abcs.Iterable[abcs.Awaitable[T]]) -> SuperAsyncList[T]: # noqa # IDE being foolish here
        self = cls.__new__(cls)
        self.aws = list(awaitables)
        return self
    @classmethod
    def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncList[T]:
        inst = cls.__new__(cls)
        inst.aws = list(map(func, *iterables))
        return inst
    @classmethod
    def starmap(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncList[T]:
        inst = cls.__new__(cls)
        inst.aws = list(itertools.starmap(func, *iterables))
        return inst
    def to_safe(self, /) -> SuperAsyncListSafe[T]:
        return SuperAsyncListSafe(self.aws)
class SuperAsyncListSafe(t.Generic[T], SASafeBase[T], SAListBase[T]):
    extend = SAListBase.extend # for IDE to understand
    append = SAListBase.append # for IDE to understand
    clear  = SAListBase.clear # for IDE to understand
    map_inplace = SAListBase.map_inplace # for IDE to understand
    __slots__ = __match_args__ = ('aws','_awaited',)
    def __init__(self, /, awaitables:list[abcs.Awaitable[T]], _already_awaited:bool=False):
        self.aws:list[abcs.Awaitable[T]] = awaitables
        self._awaited:bool = _already_awaited
    def chunked_gather(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLenUnsafe(self.aws_for_awaiting, chunk_sizes)))
    def partitioned_gather(self, /, chunks:int) -> SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition_unsafe(self.aws_for_awaiting, chunks     )))
    def chunked_gather_safe(self,/,chunk_sizes:int)->SuperAsync[tuple[T|BaseException,...]]:return SuperAsync(itertools.starmap(asyncio.gather, PartitionLen(self.aws_for_awaiting, chunk_sizes)))
    def partitioned_gather_safe(self,/,chunks:int)->SuperAsync[tuple[T|BaseException,...]]: return SuperAsync(itertools.starmap(asyncio.gather, partition    (self.aws_for_awaiting, chunks)))
    def __repr__(self, /):
        return f"{self.__class__.__name__}({self.aws!r}, _already_awaited={self._awaited})"
    @classmethod
    def safe(cls, awaitables:abcs.Iterable[abcs.Awaitable[T]], _emptied:bool=False, _already_awaited:bool=False):
        self = cls.__new__(cls)
        self._aws = list(awaitables)
        self._awaited = _already_awaited
        return self
    @classmethod
    def map(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncListSafe[T]:
        inst = cls.__new__(cls)
        inst._aws = list(map(func, *iterables))
        inst._awaited = False
        return inst
    @classmethod
    def starmap(cls, func:abcs.Callable[...,abcs.Coroutine[t.Any,t.Any,T]], *iterables:abcs.Iterable) -> SuperAsyncListSafe[T]:
        inst = cls.__new__(cls)
        inst._aws = list(itertools.starmap(func, *iterables))
        inst._awaited = False
        return inst
    def to_fast(self, /) -> SuperAsyncList[T]:
        return SuperAsyncList(self.aws)
    @property
    def aws_for_awaiting(self, /) -> list[abcs.Awaitable[T]]:
        if self._awaited:
            raise RuntimeError("Coroutines have already awaited")
        self._awaited = True
        return self.aws

# INVERSION EASY OF ACCESS CREATORS
SuperAsync.Safe = SuperAsyncSafe
SuperAsync.List = SuperAsyncList
SuperAsync.ListSafe = SuperAsyncListSafe

SuperAsyncSafe.Fast = SuperAsync
SuperAsyncSafe.List = SuperAsyncListSafe
SuperAsyncSafe.ListFast = SuperAsyncListSafe

SuperAsyncList.Std  = SuperAsync
SuperAsyncList.StdSafe  = SuperAsync
SuperAsyncList.Safe = SuperAsyncListSafe

SuperAsyncListSafe.Fast = SuperAsyncList
SuperAsyncListSafe.Std  = SuperAsyncSafe
SuperAsyncListSafe.StdFast  = SuperAsync


void = lambda x:x
class AsyncTasks(t.Generic[T], abcs.Sized, abcs.Container[asyncio.Task[T]], abcs.Reversible[asyncio.Task[T]]):
    __slots__    = ('_tasks','_rename_task', '__weakref__')
    __match_args__=('_tasks','_rename_task')
    def __init__(self, /, aws:abcs.Iterable[abcs.Awaitable[T]], *, rename_tasks:bool=True):
        self._tasks:list[asyncio.Task[T]] = []
        self._rename_task:abcs.Callable[[asyncio.Task], asyncio.Task] = self._do_rename_task if rename_tasks else self._no_rename_task
        self.register_aws(aws)
    @classmethod
    def from_empty(cls, *, rename_tasks:bool=True) -> AsyncTasks:
        inst = cls.__new__(cls)
        inst._tasks = []
        inst._rename_task = inst._do_rename_task if rename_tasks else inst._no_rename_task
        return inst
    @classmethod
    def from_tasks(cls, tasks:abcs.Iterable[asyncio.Task[T]], *, rename_tasks:bool=True) -> AsyncTasks[T]:
        """Create manager from existing tasks"""
        inst = cls.__new__(cls)
        inst._tasks = []
        inst._rename_task = inst._do_rename_task if rename_tasks else inst._no_rename_task
        inst.register_tasks(tasks)
        return inst
    @classmethod
    def from_non_tasks(cls, aws:abcs.Iterable[abcs.Awaitable[T]], *, rename_tasks:bool=True) -> AsyncTasks[T]:
        """Create manager from existing NON-task awaitables"""
        inst = cls.__new__(cls)
        inst._tasks = []
        inst._rename_task = inst._do_rename_task if rename_tasks else inst._no_rename_task
        inst.register_non_tasks(aws)
        return inst
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}.{self.__class__.from_tasks.__name__}({self._tasks!r}, rename_tasks={self._rename_task is self._do_rename_task})"
    def repr_showing_coros(self, /) -> str:
        return f"{self.__class__.__name__}.{self.__class__.from_non_tasks.__name__}({', '.join(map(repr, map(asyncio.Task.get_coro, self._tasks)))}, rename_tasks={self._rename_task is self._do_rename_task})"
    def __len__(self, /) -> int:
        return len(self._tasks)
    def __bool__(self) -> bool:
        return not not self._tasks
    if t.TYPE_CHECKING:
        @t.final
        def not_empty(self) -> bool:
            return not not self
    else:
        not_empty = __bool__
    def __iter__(self, /) -> abcs.Iterator[asyncio.Task[T]]:
        return iter(self._tasks)
    def __contains__(self, /, item) -> bool:
        return item in self._tasks
    def __reversed__(self, /) -> abcs.Iterator[asyncio.Task[T]]:
        return reversed(self._tasks)
    async def await_one(self, /, index:int) -> T:
        """Pop and await a task"""
        return await self._tasks.pop(index)
    # noinspection PyMethodMayBeStatic
    def _no_rename_task(self, /, task:asyncio.Task[T]) -> asyncio.Task[T]: return task
    def _do_rename_task(self, /, task:asyncio.Task[T]) -> asyncio.Task[T]:
        """Sets the name of tasks"""
        task.set_name(f"task: {task.get_name()!r} at {padded_hex(id(task))} | owner: {self.__class__.__name__} at {padded_hex(id(self))} ")
        return task
    Y = t.TypeVar('Y')
    def absorb(self, /, *others:AsyncTasks[T|Y], clear_others:bool=False) -> None:
        """Absorb other instances
        If `clear_others` is False (default): Other instances still work, and share the same tasks
            else: Other instances will lose access to the tasks"""
        self._tasks.extend(map(self._rename_task, itertools.chain.from_iterable(other._tasks for other in others)))
        if clear_others:
            __cls_clear = self.__class__.clear
            for other in others:
                __cls_clear(other)
    def register_task(self, /, task:asyncio.Task[T]) -> None:
        self._tasks.append(self._rename_task(task))
    def register_task_named(self, /, name:str, task:asyncio.Task[T]) -> None:
        task.set_name(name)
        self._tasks.append(self._rename_task(task))
    def register_tasks(self, /, tasks:abcs.Iterable[asyncio.Task[T]]) -> None:
        self._tasks.extend(map(self._rename_task, tasks))
    def register_tasks_named(self, /, tasks:abcs.Mapping[str,asyncio.Task[T]]) -> None:
        for n,tsk in tasks.items(): tsk.set_name(n)
        self._tasks.extend(map(self._rename_task, tasks.values()))
    def register_non_task(self, /, aw:abcs.Awaitable[T]) -> None:
        """Register and awaitable **NOT TASK**"""
        self._tasks.append(self._rename_task(asyncio.create_task(aw)))
    def register_non_task_named(self, /, name:str, aw:abcs.Awaitable[T]) -> None:
        """Register and awaitable **NOT TASK**"""
        self._tasks.append(self._rename_task(asyncio.create_task(aw, name=name)))
    def register_non_tasks(self, /, aws:abcs.Iterable[abcs.Awaitable[T]]) -> None:
        """Register multiple awaitables **NOT TASKS**"""
        self._tasks.extend(map(self._rename_task, map(asyncio.create_task, aws)))
    def register_non_tasks_named(self, /, aws:abcs.Mapping[str, abcs.Awaitable[T]]) -> None:
        """Register multiple awaitables **NOT TASKS**"""
        __self__rename_task = self._rename_task
        __asyncio_create_task = asyncio.create_task
        self._tasks.extend(__self__rename_task(__asyncio_create_task(aw, name=name)) for name,aw in aws.items())
    def register(self, /, aw:asyncio.Task | abcs.Awaitable[T]) -> None:
        """Register an awaitable or task"""
        self._tasks.append(self._rename_task(aw if isinstance(aw, asyncio.Task) else asyncio.create_task(aw)))
    def register_named(self, /, name:str, aw:asyncio.Task | abcs.Awaitable[T]) -> None:
        """Register an awaitable or task"""
        self._tasks.append(self._rename_task(rename_task((aw if isinstance(aw, asyncio.Task) else asyncio.create_task(aw)), name)))
    def register_aws(self, /, aws:abcs.Iterable[abcs.Awaitable[T]]) -> None:
        """Register multiple awaitables and tasks"""
        self._tasks.extend(self._rename_task(aw if isinstance(aw, asyncio.Task) else asyncio.create_task(aw)) for aw in aws)
    def register_aws_named(self, /, aws:abcs.Mapping[str,abcs.Awaitable[T]]) -> None:
        """Register multiple awaitables and tasks"""
        __self__rename_task = self._rename_task
        __asyncio_create_task = asyncio.create_task
        self._tasks.extend(__self__rename_task(rename_task(aw,n) if isinstance(aw, asyncio.Task) else __asyncio_create_task(aw, name=n)) for n,aw in aws)
    def manager(self, /, *, share_list:bool=True) -> SuperAsyncList[T]:
        """Create a SuperAsyncList of the tasks; Instance remains valid
        `share_list` is whether or not the manager should use the same underlying list of tasks
        if `share_list` is True, `single_use` is forced False"""
        if share_list:
            return SuperAsyncList(self._tasks)
        return SuperAsyncList(self._tasks.copy())
    def clear(self, /) -> None:
        """Discard all tasks, they remain running; Use AsyncTasks.cancel_all(...) to cancel them beforehand"""
        self._tasks.clear()
    def cancel_all(self, /, msg:t.Optional[str]=None) -> None:
        __Task_cancel = asyncio.Task.cancel
        for tsk in self._tasks:
            __Task_cancel(tsk, msg=msg)
    def timeout_all(self, /, timeout:t.Optional[float]) -> AsyncTasks:
        return self.__class__.from_non_tasks(map(functools.partial(asyncio.wait_for, timeout=timeout), self._tasks))
    def exceptions(self, /) -> abcs.Generator[t.Optional[BaseException], None, None]:
        for tsk in self._tasks:
            try: yield tsk.exception()
            except asyncio.InvalidStateError: yield None
    def coros(self) -> abcs.Generator[abcs.Coroutine[t.Any, t.Any, T], t.Any, None]:
        __Task_get_coro = asyncio.Task.get_coro
        for tsk in self._tasks:
            yield __Task_get_coro(tsk)
    def filtered_out_done     (self, /) -> AsyncTasks[T]: return self.__class__.from_tasks(itertools.filterfalse(asyncio.Task.done, self._tasks))
    def filtered_out_cancelled(self, /) -> AsyncTasks[T]: return self.__class__.from_tasks(itertools.filterfalse(asyncio.Task.cancelled, self._tasks))
    def all_done     (self, /) -> bool: return all(map(asyncio.Task.done,      self._tasks))
    def all_cancelled(self, /) -> bool: return all(map(asyncio.Task.cancelled, self._tasks))
    def any_done     (self, /) -> bool: return any(map(asyncio.Task.done,      self._tasks))
    def any_cancelled(self, /) -> bool: return any(map(asyncio.Task.cancelled, self._tasks))





@contextlib.asynccontextmanager
async def nullasynccontext():
    yield


































