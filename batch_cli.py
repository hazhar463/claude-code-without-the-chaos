import argparse
import json
from pathlib import Path
import sqlite3

from quote_batch import save_batch
from quote_store import initialize


def main(argv=None):
    parser = argparse.ArgumentParser(description="Import quote records")
    parser.add_argument("input_file")
    parser.add_argument("database_file")
    args = parser.parse_args(argv)
    try:
        with Path(args.input_file).open("rb") as source:
            raw = source.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("Input exceeds one million bytes")
        payloads = json.loads(raw.decode("utf-8"))
        connection = sqlite3.connect(args.database_file)
        try:
            initialize(connection)
            records = save_batch(connection, payloads)
        finally:
            connection.close()
    except (OSError, UnicodeError, ValueError, TypeError,
            sqlite3.Error) as error:
        parser.error(str(error))
    print(f"Saved {len(records)} quote records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
