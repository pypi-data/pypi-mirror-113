import cython
import numpy as np
from scipy.special import binom


cimport cython
cimport numpy as np

include "../../_parameters.pxi"


@cython.wraparound(False)
@cython.boundscheck(False)
cpdef np.ndarray[ITYPE_t, ndim=1] _triu_rows(unsigned int num_points):
  cdef int length = int(binom(num_points - 1 + 1, 2))
  cdef np.ndarray[ITYPE_t, ndim=1] result = np.zeros(length, dtype=ITYPE)
  cdef int idx = 0
  cdef unsigned int value = 0
  cdef unsigned int repeat = 0
  for value in range(num_points - 1u):
    for repeat in range(num_points - 1u - value, 0, -1):
      result[idx] = value
      idx += 1
  return result