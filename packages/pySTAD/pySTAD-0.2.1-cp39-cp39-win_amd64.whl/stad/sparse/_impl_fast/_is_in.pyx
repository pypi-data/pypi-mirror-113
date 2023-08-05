import cython
import numpy as np

cimport cython
cimport numpy as np

include "../../_parameters.pxi"

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef np.ndarray[BTYPE_t, ndim=1] _is_in(np.ndarray[ITYPE_t, ndim=1] distance_row,
                                        np.ndarray[ITYPE_t, ndim=1] distance_col,
                                        np.ndarray[ITYPE_t, ndim=1] network_row,
                                        np.ndarray[ITYPE_t, ndim=1] network_col):
  """ Implementation of is_in

  Creates a masks for the distance matrix indicating which edges are also
  in the given network. Assumes that edges occur in the same order and that
  all edges in the network exist in the distance matrix.

  Parameters
  ----------
  distance_row : Integer numpy array
      The row-indices of a sparse distance matrix
  distance_col : Integer numpy array
      The column-indices of a sparce distance matrix
  network_row : Integer numpy array
      The row-indices of a sparse network
  network_col : Integer numpy array
      The column-indices of a sparse network
  Returns
  -------
  A 1D boolean numpy array indicating which edges in the distance matrix
  occur in the network.
  """
  cdef Py_ssize_t n_distances = len(distance_row)
  cdef Py_ssize_t n_edges = len(network_row)
  cdef np.ndarray[BTYPE_t, ndim=1, cast=True] output_mask = np.zeros(
    n_distances, dtype = bool)

  cdef bint is_same_edge = False
  cdef UTYPE_t idx = 0
  cdef UTYPE_t network_idx = 0

  for idx in range(n_distances):
    is_same_edge = (distance_row[idx] == network_row[network_idx]) and \
                   (distance_col[idx] == network_col[network_idx])
    if is_same_edge:
      output_mask[idx] = True
      network_idx += 1
      if network_idx == n_edges:
        break
  return output_mask
