import sqlite3

from quote_store import save_quote


FIELDS = {"record_id", "unit_cents", "quantity"}


def create_quote(payload, connection):
    if type(payload) is not dict or set(payload) != FIELDS:
        return 400, {"error": "Expected exactly three quote fields"}

    try:
        record = save_quote(
            connection, payload["record_id"],
            payload["unit_cents"], payload["quantity"]
        )
    except (TypeError, ValueError) as error:
        return 422, {"error": str(error)}
    except sqlite3.IntegrityError as error:
        if error.sqlite_errorname != "SQLITE_CONSTRAINT_PRIMARYKEY":
            raise  # Not a duplicate: let the caller see it.
        return 409, {"error": "Quote identifier already exists"}

    return 201, record
