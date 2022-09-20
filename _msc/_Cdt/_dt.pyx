
__all__ = [
    'convert_tz',
    'convert_tz_clean'
]

from gll.__common import *
from gll.__static.__cimports cimport *
# from gll.__static import *

# cimport cython
# from cpython cimport int as PyInt
from cpython cimport datetime
datetime.import_datetime()

cpdef datetime.datetime convert_tz(datetime.datetime dt, str from_tz, str to_tz): # (dt:datetime.datetime, from_tz:str, to_tz:str) -> datetime.datetime:
    return dt.replace(tzinfo=zoneinfo.ZoneInfo(from_tz)).astimezone(zoneinfo.ZoneInfo(to_tz))
cpdef datetime.datetime convert_tz_clean(datetime.datetime dt, str from_tz, str to_tz): # (dt:datetime.datetime, from_tz:str, to_tz:str) -> datetime.datetime:
    return dt.replace(tzinfo=zoneinfo.ZoneInfo(from_tz)).astimezone(zoneinfo.ZoneInfo(to_tz)).replace(tzinfo=None)












