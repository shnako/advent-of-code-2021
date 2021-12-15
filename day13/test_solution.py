from unittest import TestCase

from solution import part_1, part_2


class TestSolution(TestCase):
    def test_part_1(self):
        self.assertEqual(part_1(), 687)

    # The actual result is printed so need to check the output for the below result as well:
    # ████  ██  █  █  ██  █  █ ███  ████  ██ 
    # █    █  █ █ █  █  █ █ █  █  █    █ █  █
    # ███  █    ██   █    ██   ███    █  █   
    # █    █ ██ █ █  █    █ █  █  █  █   █ ██
    # █    █  █ █ █  █  █ █ █  █  █ █    █  █
    # █     ███ █  █  ██  █  █ ███  ████  ███
    # For simplicity, the method returns the number of points. This is sufficient to detect regression issues.
    def test_part_2(self):
        self.assertEqual(part_2(), 98)
