from __future__ import annotations

__all__ = [
    'DatetimeStr'
]

from gll.__common import *
from gll.__static import *

class DatetimeStr(TrulyHashable):
    """Easy string representation of a datetime
    Uses MM/DD/YY format
    [Created ?/?/20] cython // python 5/30/21"""
    __slots__ = ('_dt', '__weakref__')
    __match_args = ('_dt',)
    def __new__(cls, *args, **kwargs):
        warnings.warn('gll._msc.DatetimeStr is deprecated for speed reasons; use gll.msc.dtstr instead', DeprecationWarning)
        return super(DatetimeStr, self).__new__(cls)
    def __init__(self, /, dt:datetime.datetime):
        self._dt:datetime.datetime = dt
    @classmethod
    def now(cls) -> DatetimeStr:
        return cls(datetime.datetime.now())
    def __hash__(self, /):
        return hash(self._dt)
    def __eq__(self, /, other:datetime.datetime|DatetimeStr) -> bool:
        isinstance = builtins.isinstance # noqa
        if isinstance(other, datetime.datetime):
            return self._dt == other
        if isinstance(other, DatetimeStr):
            return self._dt == other._dt
        return NotImplemented
    def __ne__(self, /, other:datetime.datetime|DatetimeStr) -> bool:
        return not self==other
    def __add__(self, /, other:datetime.timedelta|int|float) -> DatetimeStr:
        if isinstance(other, datetime.timedelta):
            return self.__class__(self._dt + other)
        if isinstance(other, (int,float)):
            return self.__class__(self._dt + datetime.timedelta(seconds=other))
        raise NotImplementedError
    def __iadd__(self, /, other:datetime.timedelta) -> None:
        if isinstance(other, datetime.timedelta):
            self._dt += other
        else:
            raise NotImplementedError
    def __sub__(self, /, other:datetime.timedelta) -> DatetimeStr:
        if isinstance(other, datetime.timedelta):
            return self.__class__(self._dt - other)
        raise NotImplementedError
    def __isub__(self, /, other:datetime.timedelta) -> None:
        if isinstance(other, datetime.timedelta):
            self._dt -= other
        else:
            raise NotImplementedError
    def __str__(self, /) -> str:
        return self.datetime
    def __repr__(self, /) -> str:
        return f"{self.__class__.__name__}(dt={self._dt!r})"
    def copy(self, /) -> DatetimeStr:
        return self.__class__(self._dt)
    @property
    def source_datetime(self, /) -> datetime.datetime:
        return self._dt
    def strftime(self, /, fmt:str) -> str:
        """Uses str.format first, passing time, time_military, date, datetime, datetime_military, timedate, timedate_military
        Then passes the result to datetime.datetime.strftime"""
        return self._dt.strftime(fmt.format(
            time=self.time, time_military=self.time_military, date=self.date, datetime=self.datetime,
            datetime_military=self.datetime_military, timedate=self.timedate,
            timedate_military=self.timedate_military
        ))
    @property
    def time(self, /) -> str:
        return self._dt.strftime("%I:%M %p")
    @property
    def time_military(self, /) -> str:
        return self._dt.strftime("%H:%M")
    @property
    def date(self, /) -> str:
        return self._dt.strftime("%m/%d/%y")
    @property
    def datetime(self, /) -> str:
        return self._dt.strftime("%m/%d/%y %I:%M %p")
    @property
    def datetime_military(self, /) -> str:
        return self._dt.strftime("%m/%d/%y %H:%M")
    @property
    def timedate(self, /) -> str:
        return self._dt.strftime("%I:%M %p %m/%d/%y")
    @property
    def timedate_military(self, /) -> str:
        return self._dt.strftime("%H:%M %m/%d/%y")






