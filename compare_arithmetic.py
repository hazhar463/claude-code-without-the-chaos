from decimal import Decimal, ROUND_HALF_UP

from quote import total_cents


for price in range(0, 301):
    for seats in range(1, 201):
        subtotal = price * seats
        if seats < 10:
            expected = subtotal
        else:
            amount = Decimal(subtotal) * Decimal("0.90")
            expected = int(amount.quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            ))
        assert total_cents(price, seats) == expected

print("Compared 60200 valid input pairs")
