def estimate_unique_items_using_ones(items, m=100, k=5):
    """
    Estimate the number of unique items inserted into a Bloom filter
    based on the number of 1 bits (set bits) instead of zeros.

    Formula: #TODO: write the formula you are using here
      
    """
    bf = BloomFilter(m, k)

    #TODO: complete your code here
    for item in items:
        bf.add(item)
    
    num_one_bits = np.sum(bf.bits == 1)

    if num_one_bits == m:
        return m  # All bits are set, cannot estimate
    estimated_n = - (m / k) * np.log(1 - num_one_bits / m)
    return estimated_n

