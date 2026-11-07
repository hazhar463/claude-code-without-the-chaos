from quote_store import load_quote
from quote_record import make_record


def reconcile_quote(connection, record_id, unit_cents, quantity):
    expected = make_record(record_id, unit_cents, quantity)
    saved = load_quote(connection, record_id)
    if saved is None:
        return "absent", None
    if saved == expected:
        return "matches", saved
    return "different", saved
