# Workshop Quote checkpoint ch14

Where the project stands at the end of
Chapter 14: Give It an API.
Adds the API function and the local learning server.
The web page (`quote_ui.html`) arrives in Chapter 15. Until
then, POST /quotes works, but opening http://127.0.0.1:8765/
fails and the server prints a FileNotFoundError for the page.

Compare your folder with this one, or copy a file you
are stuck on. Run these commands inside this folder:

    python3 verify.py
    python3 local_server.py

Files: `.gitignore`, `CLAUDE.md`, `hello.py`, `local_server.py`,
`quote.py`, `quote_api.py`, `quote_cli.py`, `quote_record.py`,
`quote_store.py`, `README.md`, `SPEC.md`, `test_quote.py`,
`test_quote_api.py`, `test_quote_cli.py`,
`test_quote_record.py`, `test_quote_store.py`, `verify.py`.
Use invented data only. Python 3.11+, standard library
only. Windows: use `py` instead of `python3`.
