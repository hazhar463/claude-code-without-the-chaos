# Starter kit

Copy everything in this folder (including the hidden `.claude`
folder) into a new project folder. Then:

1. Rename SPEC_TEMPLATE.md to SPEC.md and write your rules.
2. Fill in the <placeholders> in CLAUDE.md.
3. In .claude/settings.json, change the allow rules to your
   own test command, and check the hook command.
4. If your tests are not Python unittest, edit
   .claude/hooks/run_tests.py to run your test command.
5. Commit, then start Claude Code in Manual mode:
   `claude --permission-mode default`

To see hidden files: macOS Finder, Cmd+Shift+. ; terminal,
`ls -a`.
