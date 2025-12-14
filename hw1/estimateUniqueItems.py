
def estimate_unique_items(items, m=100, k=5):
    """
    Estimate the number of unique items inserted into a Bloom filter
    based on the number of zero bits remaining.

    Parameters:
        items (list): The items to insert.
        m (int): Number of bits in the Bloom filter.
        k (int): Number of hash functions.

    Returns:
        float: Estimated number of unique items.
    """
    # Initialize Bloom filter
    bf = BloomFilter(m, k)
    
    #TODO: complete your code here
    for item in items:
        bf.add(item)
    
    num_zero_bits = np.sum(bf.bits == 0)

    if num_zero_bits == 0:
        return m  # All bits are set, cannot estimate
    estimated_n = - (m / k) * np.log(num_zero_bits / m)
    return estimated_n
