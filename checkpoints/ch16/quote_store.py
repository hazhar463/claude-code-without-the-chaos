import sqlite3

from quote_record import make_record


SCHEMA = """
CREATE TABLE IF NOT EXISTS quotes (
    record_id TEXT PRIMARY KEY NOT NULL,
    unit_cents INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_cents INTEGER NOT NULL,
    policy_version TEXT NOT NULL,
    CHECK (unit_cents BETWEEN 0 AND 1000000),
    CHECK (quantity BETWEEN 1 AND 200),
    CHECK (total_cents >= 0)
)
"""


INSERT_SQL = (
    "INSERT INTO quotes (record_id, unit_cents, quantity, "
    "total_cents, policy_version) VALUES (?, ?, ?, ?, ?)"
)


def initialize(connection):
    connection.execute(SCHEMA)
    connection.commit()

def save_quote(connection, record_id, unit_cents, quantity):
    record = make_record(record_id, unit_cents, quantity)
    values = (
        record["record_id"], record["unit_cents"],
        record["quantity"], record["total_cents"],
        record["policy_version"],
    )
    with connection:
        connection.execute(
            INSERT_SQL, values
        )
    return record


def load_quote(connection, record_id):
    row = connection.execute(
        "SELECT record_id, unit_cents, quantity, "
        "total_cents, policy_version FROM quotes "
        "WHERE record_id = ?", (record_id,)
    ).fetchone()
    if row is None:
        return None
    names = ("record_id", "unit_cents", "quantity",
             "total_cents", "policy_version")
    return dict(zip(names, row))
