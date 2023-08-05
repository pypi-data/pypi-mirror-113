import cython
import numpy as np
import multiprocessing
from cython.parallel import parallel
from cython.parallel import prange
from scipy.special import binom

cimport cython
cimport numpy as np
from libc.stdlib cimport abort
from libc.stdlib cimport free
from libc.stdlib cimport malloc
from libc.string cimport memcpy
from libc.string cimport memset

include "../../_parameters.pxi"


@cython.wraparound(False)
@cython.boundscheck(False)
cpdef network_distances(sparse_adjacency_matrix, int num_threads = -1,
                        unsigned int chunk_size=30u):
    """ Computes distance of unweighted undirected networks

    Computes node distances for undirected unweighted networks containing 
    a single connected component. Implements a parallel breadth-first search
    using MPI. MPI's interface can be used to specify the number of cores
    to use.

    Parameters
    ----------
    sparse_adjacency_matrix : scipy sparse matrix
        A sparse matrix containing only the edges of the objective to evaluate.
    num_threads : integer
        A parameter for MPI, specifying the number of threads to use. When -1,
        MPI's default is used. To disable parallelism, specify 1 thread.
    chunk_size : unsigned integer
        A parameter for MPI, specifying how to distribute work. Can be tuned
        to improve performance for specific objective sizes.
    Returns
    -------
    a condensed distance matrix (1d numpy array)
    """

    # @TODO implement tocsr ourselves to avoid untyped variables
    # would allow running the sweep loops in cython as well!
    sparse_adjacency_matrix = sparse_adjacency_matrix.tocsr()
    sparse_adjacency_matrix_T = sparse_adjacency_matrix.T.tocsr()

    cdef int N = sparse_adjacency_matrix.shape[0]
    cdef int head_node
    cdef unsigned int idx_start
    cdef unsigned int chunk_size_ = chunk_size
    cdef int *buf_start

    cdef np.ndarray[ITYPE_t, ndim=1] distances = np.empty(int(binom(N, 2)),
                                                          dtype=ITYPE)

    # Extract buffers for parallel nogil access
    cdef int[::1] indices1 = sparse_adjacency_matrix.indices
    cdef int[::1] indptr1 = sparse_adjacency_matrix.indptr
    cdef int[::1] indices2 = sparse_adjacency_matrix_T.indices
    cdef int[::1] indptr2 = sparse_adjacency_matrix_T.indptr
    cdef int[::1] distances_view = distances

    if num_threads < 0:
        num_threads = multiprocessing.cpu_count()

    with nogil, parallel(num_threads = num_threads):
        # setup thread local storage:
        local_node_list = <int *> malloc(sizeof(int) * N)
        if local_node_list is NULL:
            abort()

        local_distances = <int *> malloc(sizeof(int) * N)
        if local_distances is NULL:
            free(local_node_list)
            abort()

        # run breadth first search for every node
        for head_node in prange(N - 1, chunksize=chunk_size_, schedule='dynamic'):
        # for head_node in range(N - 1):
            # fill distances with the null_idx value
            memset(local_distances, -235802127, sizeof(int) * N)

            idx_start = _sub2ind(head_node + 1u, head_node, N)
            buf_start = _breadth_first_distances(
                head_node, indices1, indptr1, indices2, indptr2,
                local_node_list, local_distances, N
            )
            memcpy(&distances_view[idx_start], buf_start,
                   sizeof(int) * (N - 1u - head_node))

        free(local_node_list)
        free(local_distances)

    return distances


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef int *_breadth_first_distances(const unsigned int head_node,
                                   const int [::1] indices1,
                                   const int [::1] indptr1,
                                   const int [::1] indices2,
                                   const int [::1] indptr2,
                                   int *node_list, int *distances,
                                   unsigned int N) nogil:
    # Inputs:
    #  head_node: (input) index of the node from which traversal starts
    #  indices1: (input) CSR indices of graph
    #  indptr1:  (input) CSR indptr of graph
    #  indices2: (input) CSR indices of transposed graph
    #  indptr2:  (input) CSR indptr of transposed graph
    #  node_list: (output) breadth-first tree (thread local array length N)
    #  distances: (output) breadth-first distance (same as node list)
    cdef unsigned int parent_node
    cdef unsigned int i_nl, i_nl_end

    node_list[0] = head_node
    distances[head_node] = 0
    i_nl = 0
    i_nl_end = 1

    while i_nl < i_nl_end:
        parent_node = node_list[i_nl]
        _walk_edges(head_node, parent_node, indptr1, indices1, node_list,
                    distances, &i_nl_end)
        _walk_edges(head_node, parent_node, indptr2, indices2, node_list,
                    distances, &i_nl_end)
        i_nl += 1

    return &distances[head_node+1]


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline void _walk_edges(const unsigned int head_node,
                             const unsigned int parent_node,
                             const int [::1] indptr, const int [::1] indices,
                             int *node_list, int *distances,
                             unsigned int *i_nl_end) nogil:
    cdef int i
    cdef unsigned int child_node
    for i in range(indptr[parent_node], indptr[parent_node + 1u]):
        child_node = indices[i]
        if child_node == head_node:
            continue

        if distances[child_node] == -235802127:

            distances[child_node] = distances[parent_node] + 1
            node_list[i_nl_end[0]] = child_node
            i_nl_end[0] += 1


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline unsigned int _sub2ind(unsigned int i,  unsigned int j,
                                  unsigned int n) nogil:
    # assert i != j, "no diagonal elements in condensed matrix"
    # if i < j:
    #     i, j = j, i
    return n*j - j*(j+1)//2 + i - 1 - j