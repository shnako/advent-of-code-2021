import itertools
from functools import reduce

from util.file_input_processor import *
from util.grid_util import initialize_zero_grid


def parse_line(input_line):
    coordinates = input_line.split(" -> ")
    return [[int(coord) for coord in coordinates[0].split(",")], [int(coord) for coord in coordinates[1].split(",")]]


def read_input():
    input_lines = read_lines()
    return list(map(parse_line, input_lines))


def is_oblique_line(line):
    return line[0][0] != line[1][0] and line[0][1] != line[1][1]


def flip_reversed_lines(lines):
    for line in lines:
        if line[0][0] > line[1][0] or line[0][1] > line[1][1]:
            line[0], line[1] = line[1], line[0]


def populate_straight_lines(vents, lines):
    for line in lines:
        if not is_oblique_line(line):
            for i in range(line[0][0], line[1][0] + 1):
                for j in range(line[0][1], line[1][1] + 1):
                    vents[j][i] += 1


def populate_oblique_lines(vents, lines):
    for line in lines:
        if is_oblique_line(line):
            i = line[0][0]
            j = line[0][1]
            increment_i = 1 if line[0][0] <= line[1][0] else -1
            increment_j = 1 if line[0][1] <= line[1][1] else -1
            while ((increment_i == 1 and i <= line[1][0]) or (increment_i == -1 and i >= line[1][0])) and (
                    (increment_j == 1 and j <= line[1][1]) or (increment_j == -1 and j >= line[1][1])):
                vents[j][i] += 1
                i += increment_i
                j += increment_j


def count_overlaps(vents):
    return sum(1 for vent in itertools.chain.from_iterable(vents) if vent > 1)


def part_1():
    lines = read_input()
    flip_reversed_lines(lines)
    vents = initialize_zero_grid(reduce(list.__add__, lines))
    populate_straight_lines(vents, lines)
    return count_overlaps(vents)


def part_2():
    lines = read_input()
    flip_reversed_lines(lines)
    vents = initialize_zero_grid(reduce(list.__add__, lines))
    populate_straight_lines(vents, lines)
    populate_oblique_lines(vents, lines)
    return count_overlaps(vents)


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
