import unittest
from weighting_platform.functions import general_functions


class GfTest(unittest.TestCase):
    def test_get_percent(self):
        first = 1000
        second = 500
        result_must = 50
        result = general_functions.get_change_percent(first, second)
        self.assertEqual(result, result_must)


if __name__ == '__main__':
    unittest.main()
