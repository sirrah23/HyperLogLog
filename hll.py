"""
Contains an implementation of the HyperLogLog algorithm.
"""
import hashlib
from collections import defaultdict


def hash_string(s):
    """
    Return the SHA-1 hash for a given string.
    """
    return hashlib.sha1(str.encode(s)).hexdigest()

def hexstring_to_int(s):
    """
    Convert a hexadecimal number to a base 10 integer.
    """
    return int(s, 16)

def get_hll_register_num(hs):
    """
    Designates the first three elements of a hexadecimal number as the
    HyperLogLog register.
    """
    return hs[:3]

def get_hll_hash(hs):
    """
    Designates the last 14 elements of a hexadecimal number as the HyperLogLog
    hash.
    """
    return hs[-14:]

def int_to_bin(i):
    """
    Convert an integer to a binary number.
    """
    return bin(i)

def first_nonzero_bit(bs):
    """
    Return the one-based array index of the first non-zero bit (from the left)
    for a given binary string.
    """
    bs = bs[2:]
    #return len(bs) - bs.index('1')
    return bs[::-1].index('1')

def element_to_register_nonzero(elem):
    """
    Given an element, return it's register # and the index of first-non-zero
    bit of its HyperLogLog hash.
    """
    elem_hash = hash_string(elem)
    register = hexstring_to_int(get_hll_register_num(elem_hash))
    hll_hash = get_hll_hash(elem_hash)
    fnz_bit = first_nonzero_bit(int_to_bin(hexstring_to_int(hll_hash)))
    return (register, fnz_bit)

def cardinality_estimate(maxbits):
    """
    Given the the first non-zero indices for a register, perform a cardinality
    estimate using the HyperLogLog formula.
    """
    tot_regs = len(maxbits)
    two_inv_sum = sum(map(lambda m: pow(2, -1*m), maxbits))
    return 0.7213/(1 + 1.079/tot_regs) * pow(tot_regs,2) * 1/two_inv_sum

def HLL(items):
    """
    Given a list of (dimension, element) pairs, get a probabilistic, distinct
    element count for each value of dimension using the HyperLogLog algorithm.
    """
    # For each item in the list
    # 1. Add the dimension to dictionary
    # 2. Get the register #, and first non-zero for the associated element
    # 3. Add the (register #, first non-zero) to the dimension's dictionary if the
    #    first non-zero value for the register is greater than the current one
    # 4. Perform the cardinality estimate for each dimension
    dim_reg_maxbit = defaultdict(lambda: defaultdict(int))
    for item in items:
        i_dim, i_elem = item
        i_reg, i_fnz_bit = element_to_register_nonzero(i_elem)
        dim_reg_maxbit[i_dim][i_reg] = max(dim_reg_maxbit[i_dim][i_reg], i_fnz_bit)
    estimates = []
    for dim in dim_reg_maxbit:
        maxbits = [v for _, v in dim_reg_maxbit[dim].items()]
        estimates.append((dim, cardinality_estimate(maxbits)))
    return estimates

def count(items):
    """
    Given a list of (dimension, element) pairs, compute the number of distinct
    elements for each dimension. Can be used to compare results of the
    HyperLogLog implementation.
    """
    res = defaultdict(lambda: set([]))
    for dim, elem in items:
        res[dim].add(elem)
    return [(k, len(v)) for k, v in res.items()]

if __name__ == "__main__":
    fname = input("Name of file with input data? ")
    with open(fname) as f:
        items = [r.split(',') for r in f.read().splitlines()]
        items = items[1:] # drop header
    hll_counts = HLL(items)
    actual_counts = count(items)
    print(hll_counts)
    print(actual_counts)

