import sqlite3
import unittest

from quote_store import initialize, save_quote, load_quote


class QuoteStoreTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        initialize(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_round_trip(self):
        expected = save_quote(self.connection, "q-1", 1250, 10)
        self.assertEqual(load_quote(self.connection, "q-1"), expected)

    def test_missing_record(self):
        self.assertIsNone(load_quote(self.connection, "absent"))

    def test_duplicate_does_not_replace(self):
        save_quote(self.connection, "q-1", 1250, 10)
        with self.assertRaises(sqlite3.IntegrityError):
            save_quote(self.connection, "q-1", 100, 1)
        self.assertEqual(
            load_quote(self.connection, "q-1")["total_cents"], 11250
        )
