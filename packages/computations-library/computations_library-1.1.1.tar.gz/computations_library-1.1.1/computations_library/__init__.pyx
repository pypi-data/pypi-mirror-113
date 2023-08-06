cimport numpy as np
ctypedef np.npy_double DOUBLE
ctypedef np.npy_intp INTP

cpdef np.ndarray[DOUBLE,ndim=1,mode='c'] RAVI(np.ndarray[DOUBLE,ndim=1,mode='c'] vidya, np.ndarray[DOUBLE,ndim=1,mode='c'] alpha, np.ndarray[DOUBLE,ndim=1,mode='c'] base, int smoothing_period, double smoothing_factor):
    cdef int i
    for i in range(smoothing_period,len(vidya)):
        if i > smoothing_period -1:
            vidya[i] = alpha[i] * smoothing_factor * base[i] + vidya[i-1] * (1 - smoothing_factor * alpha[i])
    return vidya