import json
import os
from pathlib import Path
import tempfile


def export_json(record, destination):
    destination = Path(destination)
    payload = json.dumps(record, ensure_ascii=False, indent=2)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix="quote-", suffix=".tmp", delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(payload + "\n")
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
