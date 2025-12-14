
def estimate_unique_items_trailing_ones(items):
    """
    Estimate the number of unique items using the maximum number of trailing ones
    in the binary representation of a hashed value for each item.

    Parameters:
        items (list): List of items (can include duplicates).

    Returns:
        float: Estimated number of unique items.
    """
    if not items:
        return 0 
    
    max_trailing_ones = 0

    for item in items:
        # hash item to a large integer
        digest = int(hashlib.md5(str(item).encode()).hexdigest(), 16)

        # convert to binary string
        binary_repr = bin(digest)[2:]

        # count trailing ones in the binary representation
        trailing_ones = len(binary_repr) - len(binary_repr.rstrip('1'))

        max_trailing_ones = max(max_trailing_ones, trailing_ones) 
    

    return 2 ** max_trailing_ones

