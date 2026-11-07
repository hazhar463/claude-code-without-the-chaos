from quote_record import make_record
from quote_store import INSERT_SQL


FIELDS = {"record_id", "unit_cents", "quantity"}


def save_batch(connection, payloads):
    if type(payloads) is not list or not 1 <= len(payloads) <= 100:
        raise ValueError("Batch must contain one to 100 objects")
    if connection.in_transaction:
        raise RuntimeError("Batch requires an idle connection")

    records = []
    for payload in payloads:
        if type(payload) is not dict or set(payload) != FIELDS:
            raise ValueError("Each object needs the three quote fields")
        records.append(make_record(**payload))

    values = [
        (record["record_id"], record["unit_cents"],
         record["quantity"], record["total_cents"],
         record["policy_version"])
        for record in records
    ]
    # One explicit transaction: every record is saved, or none is,
    # whatever the connection's commit settings are.
    connection.execute("BEGIN")
    try:
        connection.executemany(INSERT_SQL, values)
    except BaseException:
        if connection.in_transaction:  # SQLite may have rolled back
            connection.execute("ROLLBACK")
        raise
    connection.execute("COMMIT")
    return records
