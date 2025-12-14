def simulate_false_positive_rate(m, k, n=100, test_size=5000):
    """
    Simulate the empirical false positive rate of a Bloom filter.

    Parameters:
        m (int): Number of bits in the Bloom filter.
        k (int): Number of hash functions.
        n (int): Number of items to insert.
        test_size (int): Number of unseen items to test.

    Returns:
        float: Empirical false positive rate.
    """
    # TODO: Create a BloomFilter object with the given m and k
    bf = BloomFilter(m, k)

    # TODO: Generate n distinct items to insert into the filter
    inserted = [f"item_{i}" for i in range(n)]

    # TODO: Insert all items into the Bloom filter
    for item in inserted:
        bf.add(item)

    # Create items that were NOT inserted
    test_items = [f"test_{i}" for i in range(test_size)]

    # TODO: Count how many of the test items cause a false positive
    false_positives = 0
    for item in test_items:
        if bf.check(item):
            false_positives += 1
   

    # TODO: Return the false positive rate
    return false_positives / test_size
