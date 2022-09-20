
__all__ = [
    'procedural_argparser',
]


from gll.__common import *
from gll.__static import *


# noinspection PyUnusedLocal
def __error(message:str) -> argparse.ArgumentError: ...
# noinspection PyUnusedLocal
def procedural_argparser(prog:str, description:t.Optional[str]=None, exit_on_error:bool=False, conflict_handler:str='resolve', add_help:bool=False) -> argparse.ArgumentParser:
    """Create an argparse.Argument Parser that does not exit one error, resolves conflicts, and has no help
    Useful for propagating many argument parsers in a single program run
    On error, argparse.ArgumentError is raised"""





















