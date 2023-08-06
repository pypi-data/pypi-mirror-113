import unittest
from helpsk import example


# noinspection PyMethodMayBeStatic
class MyTestCase(unittest.TestCase):
    def test_add_one(self):
        assert example.add_one(14) == 15

    def test_add_two(self):
        assert example.add_two(14) == 16

    def test_add_three(self):
        assert example.add_three4(14) == 17


if __name__ == '__main__':
    unittest.main()
