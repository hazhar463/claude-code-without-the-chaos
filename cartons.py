def cartons_needed(packs, capacity):
    if type(packs) is not int or type(capacity) is not int:
        raise TypeError("Use exact integers")
    if not 0 <= packs <= 1_000_000:
        raise ValueError("packs is out of range")
    if not 1 <= capacity <= 1000:
        raise ValueError("capacity is out of range")
    return (packs + capacity - 1) // capacity
