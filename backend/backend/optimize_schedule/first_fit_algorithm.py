def first_fit(items, bin_capacity):
    """
    Implements the First-Fit algorithm for the bin packing problem.

    Parameters:
    - items (list of int): The sizes of the items to be packed.
    - bin_capacity (int): The capacity of each bin.

    Returns:
    - bins (list of list of int): The arrangement of items in bins.
    - bin_count (int): The total number of bins used.
    """
    bins = []  # To store the arrangement of items in bins
    for item in items:
        placed = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    
    bin_count = len(bins)
    return bins, bin_count

# Example usage
items = [2, 5, 4, 7, 1, 3, 8]
bin_capacity = 10

bins, bin_count = first_fit(items, bin_capacity)

print(f"Total bins used: {bin_count}")
for i, bin in enumerate(bins):
    print(f"Bin {i+1}: {bin}")
