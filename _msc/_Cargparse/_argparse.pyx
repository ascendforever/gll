
__all__ = [
    'procedural_argparser',
]


from gll.__common import *
from gll.__static.__cimports cimport *
# from gll.__static import *

# cimport cython
# from cpython cimport int as PyInt

cdef object __error(str message): #  -> argparse.ArgumentError:
    raise argparse.ArgumentError(None,message)
cpdef object procedural_argparser(str prog, object description=None, bint exit_on_error=False, str conflict_handler='resolve', bint add_help=False): #  -> argparse.ArgumentParser:
    """Create an argparse.Argument Parser that does not exit one error, resolves conflicts, and has no help
    Useful for propagating many argument parsers in a single program run
    On error, argparse.ArgumentError is raised"""
    parser:argparse.ArgumentParser = argparse.ArgumentParser(prog=prog, exit_on_error=exit_on_error,conflict_handler=conflict_handler, add_help=add_help, description=description)
    parser.error = __error
    # parser.add_argument('-h', '--help',
    #                     action='store_true', default=False, dest='__VOID', help="No effect")
    return parser





















