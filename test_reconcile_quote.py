import sqlite3
import unittest

from quote_store import initialize, load_quote, save_quote
from reconcile_quote import reconcile_quote


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        initialize(self.db)
        self.record = save_quote(self.db, 'retry-01', 1250, 10)
        self.changes = self.db.total_changes

    def tearDown(self):
        self.assertEqual(self.db.total_changes, self.changes)
        self.assertEqual(load_quote(self.db, 'retry-01'), self.record)
        self.assertEqual(self.db.execute(
            'SELECT COUNT(*) FROM quotes').fetchone(), (1,))
        self.db.close()

    def test_matching_request(self):
        self.assertEqual(reconcile_quote(self.db, 'retry-01', 1250, 10),
                         ('matches', self.record))

    def test_same_total_different_quantity(self):
        state, saved = reconcile_quote(self.db, 'retry-01', 1250, 9)
        self.assertEqual(state, 'different')
        self.assertEqual(saved['total_cents'], 11250)
        self.assertEqual(saved['quantity'], 10)

    def test_absent_request(self):
        self.assertEqual(reconcile_quote(self.db, 'unused-01', 1250, 10),
                         ('absent', None))

    def test_invalid_request(self):
        with self.assertRaises(ValueError):
            reconcile_quote(self.db, 'retry-01', 1250, 0)
