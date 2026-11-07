import sqlite3
import unittest

from quote_batch import save_batch
from quote_store import initialize, save_quote, load_quote


class QuoteBatchTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        initialize(self.db)

    def tearDown(self):
        self.db.close()

    def test_conflict_rolls_back_new_record(self):
        save_quote(self.db, "existing", 1250, 10)
        payloads = [
            {"record_id": "new", "unit_cents": 100, "quantity": 1},
            {"record_id": "existing", "unit_cents": 200,
             "quantity": 1},
        ]
        with self.assertRaises(sqlite3.IntegrityError):
            save_batch(self.db, payloads)
        self.assertIsNone(load_quote(self.db, "new"))
        self.assertEqual(
            load_quote(self.db, "existing")["total_cents"], 11250
        )
