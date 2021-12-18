from unittest import TestCase

from solution_list import part_1, part_2


class TestSolution(TestCase):
    def test_part_1(self):
        self.assertEqual(part_1(), 3691)

    def test_part_2(self):
        self.assertEqual(part_2(), 4756)
