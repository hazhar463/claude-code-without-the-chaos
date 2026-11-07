def total_cents(unit_cents, quantity):
    """Return a workshop total in integer cents."""
    if type(unit_cents) is not int:
        raise TypeError("unit_cents must be an int")
    if type(quantity) is not int:
        raise TypeError("quantity must be an int")

    if not 0 <= unit_cents <= 1_000_000:
        raise ValueError("unit_cents is out of range")
    if not 1 <= quantity <= 200:
        raise ValueError("quantity is out of range")

    subtotal = unit_cents * quantity
    if quantity >= 10:
        return (subtotal * 90 + 50) // 100
    return subtotal
