import cython
import numpy as np
from scipy.special import binom


cimport cython
cimport numpy as np

include "../../_parameters.pxi"

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef np.ndarray[ITYPE_t, ndim=1] _triu_cols(unsigned int num_points):
  cdef int length = int(binom(num_points, 2))
  cdef np.ndarray[ITYPE_t, ndim=1] result = np.zeros(length, dtype=ITYPE)
  cdef unsigned int idx = 0
  cdef unsigned int start = 0
  for start in range(1, num_points):
    for value in range(start, num_points):
      result[idx] = value
      idx += 1
  return result