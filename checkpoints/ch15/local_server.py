"""Loopback learning adapter. Not a production web server."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sqlite3

from quote_api import create_quote
from quote_store import initialize

ROOT = Path(__file__).resolve().parent


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Nonstandard JSON number")


class QuoteHandler(BaseHTTPRequestHandler):
    timeout = 5

    def log_message(self, format, *args):
        # Keep request paths and arbitrary client text out of the demo log.
        return

    def allowed_origin(self):
        address, port = self.server.server_address
        host = f"{address}:{port}"
        origins = self.headers.get_all("Origin") or []
        return (self.headers.get_all("Host") == [host]
                and (not origins or origins == ["http://" + host]))

    def respond(self, status, body, content_type="application/json"):
        if content_type == "application/json":
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        else:
            data = body
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self.allowed_origin():
            return self.respond(403, {"error": "Unexpected host or origin"})
        if self.path != "/":
            return self.respond(404, {"error": "Not found"})
        return self.respond(200, (ROOT / "quote_ui.html").read_bytes(),
                            "text/html")

    def do_POST(self):
        if not self.allowed_origin():
            return self.respond(403, {"error": "Unexpected host or origin"})
        if self.path != "/quotes":
            return self.respond(404, {"error": "Not found"})
        if self.headers.get_content_type() != "application/json":
            return self.respond(415, {"error": "Send application/json"})
        lengths = self.headers.get_all("Content-Length") or []
        if self.headers.get("Transfer-Encoding") or len(lengths) != 1:
            return self.respond(400, {"error": "Supply one body length"})
        if not lengths[0].isascii() or not lengths[0].isdigit():
            return self.respond(400, {"error": "Invalid body length"})
        length = int(lengths[0])
        if not 1 <= length <= 4096:
            return self.respond(413, {"error": "Body must be 1 to 4096 bytes"})
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError("Incomplete body")
            payload = json.loads(raw.decode("utf-8"),
                                 object_pairs_hook=unique_object,
                                 parse_constant=reject_constant)
        except (UnicodeError, ValueError):
            return self.respond(400, {"error": "Malformed JSON body"})
        except OSError:
            return self.respond(408, {"error": "Request timed out"})
        connection = None
        try:
            connection = sqlite3.connect(self.server.database_path)
            status, body = create_quote(payload, connection)
        except sqlite3.Error:
            status, body = 500, {"error": "Storage operation failed"}
        finally:
            if connection is not None:
                connection.close()
        return self.respond(status, body)


def make_server(database_path, port=8765):
    connection = sqlite3.connect(database_path)
    try:
        initialize(connection)
    finally:
        connection.close()
    server = ThreadingHTTPServer(("127.0.0.1", port), QuoteHandler)
    server.database_path = str(database_path)
    return server


if __name__ == "__main__":
    server = make_server(ROOT / "workshop_quotes.sqlite3")
    print("Local learning exercise: http://127.0.0.1:8765")
    print("No reservations or payments. Stop with Ctrl+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
