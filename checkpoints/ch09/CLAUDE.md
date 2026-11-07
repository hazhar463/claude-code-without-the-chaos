# Workshop Quote: rules for Claude

Workshop Quote prices seats for a fictional workshop.
SPEC.md is the source of truth. If code and SPEC.md disagree,
stop and ask; do not change SPEC.md unless I ask you to.

## How to check your work
- Run the tests: `python3 -m unittest -v`
- Show me the real test output. Do not just say "tests pass".

## Code rules
- Python 3.11+ standard library only. Ask before any `pip install`.
- Money is always integer cents (an int). Never use float for money.
- Keep each change small: one request, one change.
- After a change, show the diff and list the files you touched.

## Never do this
- Never edit, skip, or delete a test to make it pass.
  If a test looks wrong, tell me why and wait.
- Never touch real data: use invented quote records only.
- Never use the network (tests use only 127.0.0.1).
- Never read or print `.env` files or other secrets.
