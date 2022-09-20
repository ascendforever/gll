
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
from gll.__static.__cimports cimport *
# from gll.__static import *

# cimport cython
# from cpython cimport int as PyInt
from cpython cimport datetime
datetime.import_datetime()

_load_regex:t.Final[re.Pattern] = re.compile(
    # 1                   2                                3        4                   5              6
    r'(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](?:20)?(\d\d) +?(0?[1-9]|1[012])(?::([0-5]?\d))? *?([ap]m)?',
    re.I
)
cpdef datetime.datetime load(str dt, object tzinfo=None): # (dt:str, tzinfo:t.Optional[datetime.tzinfo]=None) -> t.Optional[datetime.datetime]:
    """Convert a datetime string to a datetime
    Returns None if the string was invalid
    Year is considered to be after 2000 only!"""
    cdef object m = _load_regex.fullmatch(dt) # t.Optional[re.Match[str]]
    if m is None: return None
    cdef str ampm = m[6]
    cdef bint am_time = ampm is None or ampm.lower()=='am' # true if am else pm
    cdef cython.uchar hour = int(m[4])
    if am_time: # if am
        if hour==12: # if its midnight
            hour = 0 # then we are at 0 hours
    else: # don't make this an elif, it is more concise this way
        if hour!=12: # if it is not noon
            hour += 12 # we need to make the hour right
    cdef str minute_str = m[5]
    cdef cython.uchar minute = 0 if minute_str is None else int(minute_str)
    return datetime.datetime(month=int(m[1]), day=int(m[2]), year=2000+int(m[3]), hour=hour, minute=minute, tzinfo=tzinfo)


_load_mil_regex:t.Final[re.Pattern] = re.compile(
    # 1                   2                                3        4                     5
    r'(0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])[-/](?:20)?(\d\d) +?(0?[1-9]|1\d|2[0-4]):?([0-5]?\d)?',
    re.I
)
cpdef datetime.datetime load_mil(str dt, object tzinfo=None): # (dt:str, tzinfo:t.Optional[datetime.tzinfo]=None) -> t.Optional[datetime.datetime]:
    """Convert a military datetime string to a datetime
    Returns None if the string was invalid
    Year is considered to be after 2000 only!"""
    cdef object m = _load_mil_regex.fullmatch(dt) # t.Optional[re.Match[str]]
    if m is None: return None
    cdef cython.uchar hour = int(m[4])
    if hour==24: # sometimes it is 24, but we prefer 0
        hour = 0
    cdef str minute_str = m[5]
    cdef cython.uchar minute = 0 if minute_str is None else int(minute_str)
    return datetime.datetime(month=int(m[1]), day=int(m[2]), year=2000+int(m[3]), hour=hour, minute=minute, tzinfo=tzinfo)



__datetime_datetime_strfttime = datetime.datetime.strftime
__datetime_datetime_now = datetime.datetime.now # note: datetime.datetime.now is faster than its equivalent of datetime.datetime.fromtimestamp(time.time())

# we don't use lambdas for this because we lose the type annotations - NO MATTER WHAT
cpdef str t     (datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%I:%M %p"         ) # dt:datetime.datetime
cpdef str t_mil (datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%H:%M"            ) # dt:datetime.datetime
cpdef str d     (datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%m/%d/%y"         ) # dt:datetime.datetime
cpdef str dt    (datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%m/%d/%y %I:%M %p") # dt:datetime.datetime
cpdef str dt_mil(datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%m/%d/%y %H:%M"   ) # dt:datetime.datetime
cpdef str td    (datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%I:%M %p %m/%d/%y") # dt:datetime.datetime
cpdef str td_mil(datetime.datetime dt_): return __datetime_datetime_strfttime(dt_, "%H:%M %m/%d/%y"   ) # dt:datetime.datetime

cpdef str t_now     ():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%I:%M %p"         )
cpdef str t_mil_now ():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%H:%M"            )
cpdef str d_now     ():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%m/%d/%y"         )
cpdef str dt_now    ():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%m/%d/%y %I:%M %p")
cpdef str now       (): # yes this is identical to the above
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%m/%d/%y %I:%M %p")
cpdef str dt_mil_now():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%m/%d/%y %H:%M"   )
cpdef str td_now    ():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%I:%M %p %m/%d/%y")
cpdef str td_mil_now():
    cdef object dt_class = datetime.datetime
    return dt_class.strftime(dt_class.now(), "%H:%M %m/%d/%y"   )













