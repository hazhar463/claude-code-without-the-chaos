"""PostToolUse hook: run the tests after Claude edits a Python file.

Claude Code runs this after every Edit or Write (see
.claude/settings.json). It reads the hook's JSON from standard input,
runs the test suite quietly, and stays silent when all tests pass.
When a test fails, it prints a short summary to stderr and exits
with code 2, so Claude sees the failure. Local only: no network,
no installs, and it never changes a file.
"""
import json
from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[2]


def edited_file():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return ""
    return str(event.get("tool_input", {}).get("file_path", ""))


def main():
    if not edited_file().endswith(".py"):
        return 0  # Only Python edits can break the tests.
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-q"],
            cwd=PROJECT, capture_output=True, text=True, timeout=100,
        )
    except subprocess.TimeoutExpired:
        print("Hook: tests took over 100 seconds.", file=sys.stderr)
        return 2
    if result.returncode == 0:
        return 0
    lines = result.stderr.strip().splitlines()
    failed = [line for line in lines
              if line.startswith(("FAIL:", "ERROR:"))]
    print("Hook: tests FAILED after this edit.", file=sys.stderr)
    print("\n".join(failed[:10] + lines[-1:]), file=sys.stderr)
    print("Run python3 -m unittest -v to see details.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
