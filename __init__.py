


from sys import version_info as ____version_info
if ____version_info >= (3,9,2):
    from warnings import warn as ____warn
    ____warn(f"Python version should be 3.9 or greater", ImportWarning)

PYXIMPORT_INSTALLED:bool = False
from .__common import __imports as _ # for the checks
try:
    from .__static import *
    from ._msc import *
    from . import conv
    from . import mth
except ImportError:
    from pyximport import install as ____pyximport_install
    from warnings import warn as ____warn
    ____warn("Pyximport has been installed because this is the first time the package is running", ImportWarning)
    # you cannot redirect pyximport compilation messages
    ____pyximport_install(language_level=3, inplace=True)
    PYXIMPORT_INSTALLED = True
    from . import __static as _
    from . import _msc as _
    from . import conv as _
    from . import mth as _

    from .__static import *
    from ._msc import *
    from . import conv
    from . import mth


__version__ = '1.36.0'
