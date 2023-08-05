import cython
import numpy as np

cimport cython
cimport numpy as np
from libc.math cimport ceil


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cpdef ind2sub(unsigned int k, unsigned int n):
  """
  Computes the row and column location in a dense matrix for an index
  in a condensed matrix.
  
  Parameters
  ----------
  k : unsigned int 
    The index value to transform.
  n : unsigned int
    The number of nodes in the distance matrix.
  Returns
  -------
    A tuple with the (row, col) value. (-1 , -1) if the given index does not 
    exist in a condensed matrix of the given size.
  """
  cdef int i = calc_row_idx(k, n)
  cdef int j = calc_col_idx(k, i, n)
  if i < 0 or j > int(n) or j < 0 or i > int(n):
    return -1, -1
  return i, j


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline int calc_row_idx(unsigned int k, unsigned int n):
    return int(
      ceil((1/2.) * (- (-8*k + 4 *n**2 -4*n - 7)**0.5 + 2*n -1) - 1)
    )


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline unsigned int elem_in_i_rows(unsigned int i, unsigned int n):
    return i * (n - 1 - i) + (i*(i + 1))//2


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline int calc_col_idx(unsigned int k, unsigned int i,
                             unsigned int n):
    return n - elem_in_i_rows(i + 1, n) + k
