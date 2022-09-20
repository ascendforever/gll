

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from ._Stubargparse import *
else:
    from ._argparse import * # noqa


