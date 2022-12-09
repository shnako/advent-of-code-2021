from unittest import TestCase

from solution import part_1, part_2


class TestSolution(TestCase):
    def test_part_1(self):
        self.assertEqual(part_1(), 489)

    def test_part_2(self):
        self.assertEqual(part_2(), "Merry Christmas!")
