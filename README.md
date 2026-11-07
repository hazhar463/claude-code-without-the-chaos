# Workshop Quote: companion code

Companion to *Claude Code Without the Chaos* by Hassan Azhar
(BriskNest Tech Guides). Latest version:
https://github.com/hazhar463/claude-code-without-the-chaos

Workshop Quote prices seats for a fictional workshop. It is a local
learning project: it creates quote records, but it does not reserve
seats, take payment, or provide production security. Use invented
data only.

Requires Python 3.11 or later, standard library only (no `pip install`).
The tests were run with CPython 3.11, 3.12, and 3.13. On Windows,
use WSL (Ubuntu) and type the commands as printed; in Git Bash, type
`py` instead of `python3`.

## Run it
Open a terminal in this folder, then:

- `python3 -m unittest -v` runs the tests in this folder.
- `python3 verify.py` runs every test, including local HTTP checks
  on 127.0.0.1 only.
- `python3 quote_cli.py 1250 4` prints `Total: USD 50.00`.
- `python3 batch_cli.py sample_batch.json learning.sqlite3` imports
  two records. Run it again and it reports a duplicate; the first
  two records stay unchanged. All records commit together or none do
  (1 to 100 records; input file at most 1,000,000 bytes). A rejected
  import into a new database name can leave an empty database file
  behind; it holds no quotes.
- `python3 local_server.py` starts http://127.0.0.1:8765. Open that
  exact address; stop with Ctrl+C. Quotes are saved beside the script
  in `workshop_quotes.sqlite3`. This server is a learning adapter,
  not production infrastructure, and has no accounts.

SPEC.md is the source of truth for prices (R1 to R9).

## Chapter checkpoints
Stuck? `checkpoints/` holds the project as it stands at the end of
Chapters 5, 9, 13, 14, 15, and 16. Each folder is complete: `cd` into
it and run its tests to compare with your own work. Its CHECKPOINT.md
says what the folder contains and which chapter it matches.

## Starter kit (Chapter 24)
`starter_kit/` holds the same Claude Code files with the Workshop
Quote details taken out: a CLAUDE.md template, a SPEC_TEMPLATE.md,
`.claude/settings.json`, the test hook, the `/verify-change` skill,
and the read-only spec reviewer. Copy the whole folder (including
the hidden `.claude`) into a new project; its README.md lists the
five things to change.

## Claude Code files (Chapters 7 and 17 to 21)
- `CLAUDE.md`: project rules Claude reads at the start of a session.
- `.claude/settings.json`: Manual mode by default, allow rules for
  the test commands only, deny rules for `.env` files, and one hook.
- `.claude/hooks/run_tests.py`: the hook. After Claude edits a Python
  file, it runs the tests and reports any failure to Claude.
- `.claude/skills/verify-change/SKILL.md`: the `/verify-change` skill
  for the Verify step of the loop.
- `.claude/agents/spec-reviewer.md`: a read-only subagent that checks
  a change against SPEC.md.

Read each file before you use it: a hook runs as a command with
your user's permissions on your computer.

## Labs and extras
`test_extended.py`, `test_labs.py`, `reconcile_quote.py`,
`bounded_tools.py`, `compare_arithmetic.py`, and the lab helpers
support the extended labs at the back of the book
(`measure_calculation.py` and `compare_arithmetic.py` for Lab 6,
`reconcile_quote.py` for Lab 7).

When sharing this folder, leave out `.venv`, caches, databases,
`.env` files, and `.claude/settings.local.json`.

## Changes in newer Claude Code versions
The book was written and checked with Claude Code 2.1.311
(November 2026). Screens, option labels, and defaults can change in
later versions. When a change affects a step in the book, it is
listed here with the chapter and what to do instead.

- No changes recorded yet.

## License
The code in this repository is released under the MIT License
(see LICENSE). The book's text is not included and is not licensed.
