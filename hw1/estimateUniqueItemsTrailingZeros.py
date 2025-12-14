
def estimate_unique_items_trailing_zeros(items):
    """
    Estimate the number of unique items using the maximum number of trailing zeros
    in the binary representation of a hashed value for each item.

    Parameters:
        items (list): List of items (can include duplicates).

    Returns:
        float: Estimated number of unique items.
    """
    true_unique = len(set(items))
    if true_unique == 0:
        return 0

    # l = ceil(log2(n))
    l = math.ceil(math.log2(true_unique))
    max_trailing_zeros = 0

    for item in items:
        # hash item to a large integer
        digest = int(hashlib.md5(str(item).encode()).hexdigest(), 16)

        # restrict digest to l bits using modulo 2^l
        digest_l_bits = digest % (2 ** l)

        # convert to binary string of length l
        binary_repr = bin(digest_l_bits)[2:].zfill(l)

        # count trailing zeros in those l bits
        trailing_zeros = len(binary_repr) - len(binary_repr.rstrip('0'))

        max_trailing_zeros = max(max_trailing_zeros, trailing_zeros)

    return 2 ** max_trailing_zeros
