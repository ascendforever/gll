

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from ._Stubbytes import *
else:
    from ._bytes import * # noqa

