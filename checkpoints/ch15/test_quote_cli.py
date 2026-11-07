import contextlib
import io
import unittest

from quote_cli import format_usd, main


class QuoteCliTests(unittest.TestCase):
    def test_format_small_total(self):
        self.assertEqual(format_usd(5), "USD 0.05")

    def test_success(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["1250", "4"])
        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), "Total: USD 50.00\n")

    def test_invalid_range(self):
        error_output = io.StringIO()
        with contextlib.redirect_stderr(error_output):
            with self.assertRaises(SystemExit) as caught:
                main(["1250", "0"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("quantity is out of range",
                      error_output.getvalue())
