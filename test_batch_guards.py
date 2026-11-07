import sqlite3
import unittest

from quote_batch import save_batch
from quote_store import initialize


def quote(n):
    return {"record_id": f"g-{n}", "unit_cents": 100, "quantity": 1}


class BatchGuardTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        initialize(self.db)

    def tearDown(self):
        self.db.close()

    def assert_rejected(self, payloads):
        with self.assertRaises(ValueError):
            save_batch(self.db, payloads)
        count = self.db.execute("SELECT COUNT(*) FROM quotes")
        self.assertEqual(count.fetchone()[0], 0)

    def test_rejects_empty_batch(self):
        self.assert_rejected([])

    def test_rejects_101_objects(self):
        self.assert_rejected([quote(n) for n in range(101)])

    def test_rejects_extra_field(self):
        self.assert_rejected([dict(quote(1), paid=True)])


class BatchAutocommitTests(unittest.TestCase):
    def test_rolls_back_without_implicit_transactions(self):
        db = sqlite3.connect(":memory:", isolation_level=None)
        try:
            initialize(db)
            payloads = [quote(1), quote(1)]
            with self.assertRaises(sqlite3.IntegrityError):
                save_batch(db, payloads)
            count = db.execute("SELECT COUNT(*) FROM quotes")
            self.assertEqual(count.fetchone()[0], 0)
        finally:
            db.close()
