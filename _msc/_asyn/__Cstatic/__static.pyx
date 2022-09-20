
__all__ = [
    # 'create_task_named',
    'rename_task',
    'bind_tasks',
    'ignore_asyncio_timeout',
]

from gll.__common import *
from gll.__static.__cimports cimport *
# from gll.__static import *

# cimport cython
# from cpython cimport int as PyInt

# cpdef object create_task_named(str name, object coro): # (name:str, coro:col.abc.Awaitable[T]) -> asyncio.Task[T]:
#     tsk:asyncio.Task = asyncio.create_task(coro)
#     tsk.set_name(name)
#     return tsk
cpdef object rename_task(object task, str name): # (task:asyncio.Task[T], name:str) -> asyncio.Task[T]:
    task.set_name(name)
    return task


cdef void _callback(object other, object this): # (other:asyncio.Task, this:asyncio.Task) -> None:
    if not other.done():
        other.cancel()
cpdef void bind_tasks(object main, object other): # (main:asyncio.Task, other:asyncio.Task) -> None:
    main.add_done_callback(functools.partial(_callback, other))
    other.add_done_callback(functools.partial(_callback, main))


async def ignore_asyncio_timeout(object aw, object default_return=None) -> object:
    try: 
        return await aw
    except asyncio.TimeoutError:
        return None












