def bloom_filter_jaccard(A, B, m=100, k=5):
    """
    Estimate Jaccard similarity using Bloom filters.
    
    Parameters:
        A, B: lists or sets of items
        m: Bloom filter size
        k: number of hash functions
    
    Returns:
        Estimated Jaccard similarity (float)
    """
    bf_A = BloomFilter(m, k)
    bf_B = BloomFilter(m, k)

    for a in A:
        bf_A.add(a)

    for b in B:
        bf_B.add(b)

    bits_A = bf_A.bits
    bits_B = bf_B.bits

    intersect = [i for i, (a, b) in enumerate(zip(bits_A, bits_B)) if a and b]
    union = [i for i, (a, b) in enumerate(zip(bits_A, bits_B)) if a or b]

    return len(intersect) / len(union)

