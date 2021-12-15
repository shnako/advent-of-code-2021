import unittest

from solution import part_1, part_2


class TestSolution(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(part_1(), 472)

    def test_part_2(self):
        self.assertEqual(part_2(), 2851)
