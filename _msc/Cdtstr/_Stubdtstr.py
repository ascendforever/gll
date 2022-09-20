
__all__ = [
    '_load_regex',
    'load',
    '_load_mil_regex',
    'load_mil',
    't',
    't_mil',
    'd',
    'dt',
    'dt_mil',
    'td',
    'td_mil',
    't_now',
    't_mil_now',
    'd_now',
    'dt_now',
    'now',
    'dt_mil_now',
    'td_now',
    'td_mil_now',
]

# [Created 11/11/21]

from gll.__common import *
from gll.__static import *


_load_regex:t.Final[re.Pattern] = re.compile(
    # 1                   2                                3        4                   5              6
    r'(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](?:20)?(\d\d) +?(0?[1-9]|1[012])(?::([0-5]?\d))? *?([ap]m)?',
    re.I
)
# noinspection PyUnusedLocal
def load(dt:str, tzinfo:t.Optional[datetime.tzinfo]=None) -> t.Optional[datetime.datetime]:
    """Convert a datetime string to a datetime
    Returns None if the string was invalid
    Year is considered to be after 2000 only!"""


_load_mil_regex:t.Final[re.Pattern] = re.compile(
    # 1                   2                                3        4                     5
    r'(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](?:20)?(\d\d) +?(0?[1-9]|1\d|2[0-4]):?([0-5]?\d)?',
    re.I
)
# noinspection PyUnusedLocal
def load_mil(dt:str, tzinfo:t.Optional[datetime.tzinfo]=None) -> t.Optional[datetime.datetime]:
    """Convert a military datetime string to a datetime
    Returns None if the string was invalid
    Year is considered to be after 2000 only!"""


def t     (dt:datetime.datetime) -> str: ...
def t_mil (dt:datetime.datetime) -> str: ...
def d     (dt:datetime.datetime) -> str: ...
def dt    (dt:datetime.datetime) -> str: ...
def dt_mil(dt:datetime.datetime) -> str: ...
def td    (dt:datetime.datetime) -> str: ...
def td_mil(dt:datetime.datetime) -> str: ...

def t_now     () -> str: ...
def t_mil_now () -> str: ...
def d_now     () -> str: ...
def dt_now() -> str: ...
now = dt_now
def dt_mil_now() -> str: ...
def td_now    () -> str: ...
def td_mil_now() -> str: ...













