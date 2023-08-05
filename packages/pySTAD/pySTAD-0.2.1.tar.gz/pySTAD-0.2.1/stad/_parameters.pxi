UTYPE = np.uint32
ctypedef np.uint32_t UTYPE_t

ITYPE = np.int32
ctypedef np.int32_t ITYPE_t

IBTYPE = np.int64
ctypedef np.int64_t IBTYPE_t

FSTYPE = np.float32
ctypedef np.float32_t FSTYPE_t

FTYPE = np.float64
ctypedef np.float64_t FTYPE_t

BTYPE = np.uint8
ctypedef np.uint8_t BTYPE_t

ctypedef fused BASETYPE_t:
  UTYPE_t
  ITYPE_t
  IBTYPE_t
  FTYPE_t
  FSTYPE_t
  BTYPE_t

DEF NULL_IDX = -9999
