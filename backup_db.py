"""Copy a SQLite database safely: python3 backup_db.py FROM TO"""
from pathlib import Path
import sqlite3
import sys

source_path, target_path = Path(sys.argv[1]), Path(sys.argv[2])
if target_path.exists():
    raise SystemExit(f"{target_path} exists; choose a new name")
source_uri = source_path.resolve().as_uri() + "?mode=ro"
source = sqlite3.connect(source_uri, uri=True)
target = sqlite3.connect(target_path)
source.backup(target)
target.close()
source.close()
print("Backed up", source_path, "to", target_path)
