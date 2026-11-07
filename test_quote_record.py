import unittest

from quote_record import make_record


class QuoteRecordTests(unittest.TestCase):
    def test_record_fields(self):
        record = make_record("demo-001", 1250, 10)
        self.assertEqual(record["record_id"], "demo-001")
        self.assertEqual(record["total_cents"], 11250)
        self.assertEqual(record["policy_version"], "group10-v1")

    def test_rejects_invalid_identifier(self):
        for value in ("", "with space", "x" * 41, "a\nb"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    make_record(value, 1250, 1)
