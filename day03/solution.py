from copy import deepcopy
from time import time

from util.file_input_processor import read_lines


def find_most_common_at_position(binaries, position):
    ones_at_position = sum(binary[position] == '1' for binary in binaries)
    return 1 if ones_at_position >= len(binaries) / 2 else 0


def find_rating(binaries, use_most_common):
    bits = len(binaries[0])
    for i in range(bits):
        most_common_at_position = find_most_common_at_position(binaries, i)
        binaries = list(filter(lambda binary: (binary[i] == str(most_common_at_position)) == use_most_common, binaries))

        if len(binaries) == 1:
            return int(binaries[0], 2)


def part_1():
    binaries = read_lines()
    bits = len(binaries[0])

    gamma = epsilon = 0
    for i in range(bits):
        most_common_at_position = find_most_common_at_position(binaries, i)
        gamma = 2 * gamma + most_common_at_position
        epsilon = 2 * epsilon + abs(most_common_at_position - 1)

    return gamma * epsilon


def part_2():
    binaries = read_lines()

    oxygen_value = find_rating(deepcopy(binaries), True)
    co2_value = find_rating(deepcopy(binaries), False)

    return oxygen_value * co2_value


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
