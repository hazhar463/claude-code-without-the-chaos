---
name: verify-change
description: Verify the current change in Workshop Quote with evidence. Use after any code change, or when asked to check, verify, or prove that a change works.
---
# Verify a change (the Verify step of the loop)

Verify the change described here: $ARGUMENTS
If nothing is described, verify all uncommitted changes.

Work through these steps in order. Change no files.

1. Run `python3 -m unittest -v`. Then run `python3 verify.py`.
   Copy the last lines of each output (the `Ran N tests` line
   and `OK` or `FAILED`) exactly as printed.
2. Run `git diff --stat`. List every file that changed.
   Flag any test file in the list: tests change only on request.
3. Open SPEC.md. For each requirement (R1, R2, ...) that the
   change touches, name the test that checks it, or say
   "no test covers this".
4. Report in two short lists:
   - **Evidence**: what you ran and saw (commands and output).
   - **Claims**: anything you believe but did not check.
5. End with one line: `VERIFIED` only if every test passed and
   no test file changed unasked; otherwise `NOT VERIFIED` and why.
