# Workshop Quote calculation

R1. total_cents(unit_cents, quantity) returns an int.
R2. Both arguments must be exact built-in int values.
    Reject bool, float, string, and other types
    with TypeError.
    Check both types before checking either range.
R3. unit_cents must be from 0 to 1000000 inclusive.
    Otherwise raise ValueError.
R4. quantity must be from 1 to 200 inclusive.
    Otherwise raise ValueError.
R5. Subtotal equals unit_cents multiplied by quantity.
R6. Quantities 1 through 9 receive no discount.
R7. Quantities 10 through 200 receive 10 percent
    off the entire subtotal.
R8. Round the discounted total once to the nearest
    cent; an exact half cent rounds upward.
R9. Return the total without printing, saving files,
    changing external state, or using the network.

Outside the scope of total_cents: tax, payments,
seat availability, multiple currencies, and storage.
Saved quotes (Part III) have their own rules,
written as tests: test_quote_record.py and
test_quote_store.py.
