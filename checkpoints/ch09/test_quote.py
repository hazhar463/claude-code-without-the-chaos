import unittest

from quote import total_cents


class TotalCentsTests(unittest.TestCase):
    def test_ordinary_total(self):
        self.assertEqual(total_cents(1250, 4), 5000)

    def test_below_threshold(self):
        self.assertEqual(total_cents(1250, 9), 11250)

    def test_at_threshold(self):
        self.assertEqual(total_cents(1250, 10), 11250)

    def test_above_threshold(self):
        self.assertEqual(total_cents(1250, 11), 12375)

    def test_half_cent_rounds_up(self):
        self.assertEqual(total_cents(105, 11), 1040)

    def test_fraction_below_half_rounds_down(self):
        self.assertEqual(total_cents(101, 17), 1545)

    def test_free_workshop(self):
        self.assertEqual(total_cents(0, 10), 0)

    def test_minimum_quantity(self):
        self.assertEqual(total_cents(1250, 1), 1250)

    def test_upper_bounds(self):
        self.assertEqual(
            total_cents(1_000_000, 200), 180_000_000
        )

    def test_invalid_prices(self):
        for value in (-1, 1_000_001):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    total_cents(value, 1)

    def test_invalid_quantities(self):
        for value in (0, -1, 201):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    total_cents(1250, value)

    def test_wrong_types(self):
        for value in (True, False, 1.0, "1", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    total_cents(value, 1)
                with self.assertRaises(TypeError):
                    total_cents(1250, value)

        with self.assertRaises(TypeError):
            total_cents(-1, "1")

    def test_result_type(self):
        self.assertIs(type(total_cents(105, 11)), int)


if __name__ == "__main__":
    unittest.main()
