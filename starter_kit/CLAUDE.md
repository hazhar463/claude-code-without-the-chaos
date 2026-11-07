# <Project name>: rules for Claude

<One sentence: what this project does.>
SPEC.md is the source of truth. If code and SPEC.md disagree,
stop and ask; do not change SPEC.md unless I ask you to.

## How to check your work
- Run the tests: `python3 -m unittest -v`
- Show me the real test output. Do not just say "tests pass".

## Code rules
- <Language and version>. Ask before installing anything.
- Keep each change small: one request, one change.
- After a change, show the diff and list the files you touched.

## Never do this
- Never edit, skip, or delete a test to make it pass.
  If a test looks wrong, tell me why and wait.
- Never touch real data or secrets; never read `.env` files.
