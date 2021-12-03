from copy import deepcopy

from util.file_input_processor import *


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
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
