from typing import Any, List

ctypedef unsigned int uint32_t

cdef uint32_t DEFAULT_SEED = 0
cdef uint32_t c1 = 0xcc9e2d51
cdef uint32_t c2 = 0x1b873593

cdef inline uint32_t rotl32 (uint32_t x, char r):
    return (x << r) | (x >> (32 - r))

cdef inline uint32_t fmix32 (uint32_t h):
    h ^= h >> 16
    h *= <uint32_t>0x85ebca6b
    h ^= h >> 13
    h *= <uint32_t>0xc2b2ae35
    h ^= h >> 16

    return h

def initialize(seed: int = DEFAULT_SEED) -> int:
    return seed

cpdef int _update(hash_val: int, value: int):
    cdef uint32_t k1 = <uint32_t>(<int>value)
    cdef uint32_t h1 = <uint32_t>(<int>hash_val)

    k1 *= c1
    k1 = rotl32(k1, 15)
    k1 *= c2
    
    h1 ^= k1
    h1 = rotl32(h1, 13)
    h1 = h1 * <uint32_t>(5) + <uint32_t>(0xe6546b64)

    return h1

def update(hash_val: int, value: Any) -> int:
    return _update(hash_val, hash(value) if value is not None else 0)

def finish(hash_val: int, numberOfWords: int) -> int:
    cdef uint32_t h1 = <uint32_t>(<int>hash_val)
    h1 ^= numberOfWords * 4
    h1 = fmix32(h1)
    return <int>h1

def hashCode(data: List[Any], seed: int) -> int:
    hash_val = initialize(seed)
    for value in data:
        hash_val = update(hash_val, value)

    hash_val = finish(hash_val, len(data))
    return hash_val
