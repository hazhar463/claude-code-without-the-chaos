import re


def parse_catalog_price(text):
    if type(text) is not str:
        raise TypeError("Price field must be text")
    if re.fullmatch(r"[0-9]+", text) is None:
        raise ValueError("Price must contain ASCII digits only")
    if len(text) > 7:
        raise ValueError("Price is too long")
    value = int(text)
    if not 0 <= value <= 1_000_000:
        raise ValueError("Price is out of range")
    return value
