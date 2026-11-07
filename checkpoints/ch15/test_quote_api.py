import sqlite3
import unittest

from quote_api import create_quote
from quote_store import initialize, load_quote


class QuoteApiTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        initialize(self.db)

    def tearDown(self):
        self.db.close()

    def test_create(self):
        payload = {"record_id": "api-1",
                   "unit_cents": 1250, "quantity": 10}
        status, body = create_quote(payload, self.db)
        self.assertEqual(status, 201)
        self.assertEqual(body["total_cents"], 11250)
        self.assertEqual(load_quote(self.db, "api-1"), body)

    def test_reject_extra_field(self):
        payload = {"record_id": "api-1", "unit_cents": 1250,
                   "quantity": 10, "confirmed": True}
        status, body = create_quote(payload, self.db)
        self.assertEqual(status, 400)
        self.assertIsNone(load_quote(self.db, "api-1"))
