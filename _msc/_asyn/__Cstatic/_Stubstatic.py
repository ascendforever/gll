
__all__ = [
    'rename_task',
    'bind_tasks'
]

from gll.__common import *
from gll.__static import *


# noinspection PyUnusedLocal
def rename_task(task:asyncio.Task[T], name:str) -> asyncio.Task[T]: ...

# noinspection PyUnusedLocal
def _callback(other:asyncio.Task, this:asyncio.Task) -> None: ...
# noinspection PyUnusedLocal
def bind_tasks(main:asyncio.Task, other:asyncio.Task) -> None:
    """Bind two tasks together such that when one is completed, the other is cancelled"""

async def ignore_asyncio_timeout(aw:abcs.Awaitable[T], default_return:Y=None) -> T|Y:
    """Await `aw`, if an asyncio.TimeoutError occurs, return `default_return`
    [Created 1/28/22]"""












