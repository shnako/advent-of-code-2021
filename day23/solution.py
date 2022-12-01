from time import time

from util.file_input_processor import *


# Christmas things took priority and I didn't get the time to code this. Maybe one day I will.

def part_1():
    inp = read_integer_lines()


def part_2():
    inp = read_integer_lines()


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
