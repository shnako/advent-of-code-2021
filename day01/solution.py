from time import time

from util.file_input_processor import read_integer_lines


def part_1():
    depths = read_integer_lines()
    increases = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            increases += 1
    return increases


def part_2():
    depths = read_integer_lines()
    increases = 0
    for i in range(1, len(depths) - 2):
        if depths[i] + depths[i + 1] + depths[i + 2] > depths[i - 1] + depths[i] + depths[i + 1]:
            increases += 1
    return increases


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
