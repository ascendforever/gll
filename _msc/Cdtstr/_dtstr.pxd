


cimport cython
from cpython cimport datetime




cpdef datetime.datetime load(str dt, object tzinfo=*)

cpdef datetime.datetime load_mil(str dt, object tzinfo=*)


cpdef str t     (datetime.datetime dt_)
cpdef str t_mil (datetime.datetime dt_)
cpdef str d     (datetime.datetime dt_)
cpdef str dt    (datetime.datetime dt_)
cpdef str dt_mil(datetime.datetime dt_)
cpdef str td    (datetime.datetime dt_)
cpdef str td_mil(datetime.datetime dt_)

cpdef str t_now     ()
cpdef str t_mil_now ()
cpdef str d_now     ()
cpdef str dt_now    ()
cpdef str now       ()
cpdef str dt_mil_now()
cpdef str td_now    ()
cpdef str td_mil_now()













