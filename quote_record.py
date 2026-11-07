import re

from quote import total_cents


POLICY_VERSION = "group10-v1"


def make_record(record_id, unit_cents, quantity):
    if type(record_id) is not str:
        raise TypeError("record_id must be text")
    if re.fullmatch(r"[A-Za-z0-9_-]{1,40}", record_id) is None:
        raise ValueError("record_id has an invalid format")

    total = total_cents(unit_cents, quantity)
    return {
        "record_id": record_id,
        "unit_cents": unit_cents,
        "quantity": quantity,
        "total_cents": total,
        "policy_version": POLICY_VERSION,
    }
