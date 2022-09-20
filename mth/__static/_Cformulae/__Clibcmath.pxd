


# from libc.math cimport sinl, asinl, sin, asin, sinf, asinf, cosl, acosl, cos, acos, cosf, acosf, tanl, atanl, tan, atan, tanf, atanf



cdef extern from "<math.h>" nogil:
    double sqrt(double x)
    float sqrtf(float)
    long double sqrtl(long double)

    long double asinl(long double)
    double asin(double x)
    float asinf(float)
    long double sinl(long double)
    double sin(double x)
    float sinf(float)

    long double acosl(long double)
    double acos(double x)
    float acosf(float)
    long double cosl(long double)
    double cos(double x)
    float cosf(float)

    long double tanl(long double)
    double tan(double x)
    float tanf(float)
    long double atanl(long double)
    double atan(double x)
    float atanf(float)


