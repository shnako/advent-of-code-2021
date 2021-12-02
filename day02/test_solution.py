import unittest

from solution import part_1, part_2


class TestSolution(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(part_1(), 1693300)

    def test_part_2(self):
        self.assertEqual(part_2(), 1857958050)
