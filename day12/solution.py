from collections import defaultdict
from time import time

from util.file_input_processor import read_lines

"""
This solution keeps track of each cave's adjacent caves in a dict
and uses a Depth-First Search algorithm to navigate all the valid paths and recursively sum them up.
The solution to the second part keeps track of the revisited cave
whereas the solution to the first part overwrites it from the beginning to prevent revisiting.
"""

START = 'start'
END = 'end'

global adjacent_caves


def read_input():
    lines = read_lines()

    global adjacent_caves
    adjacent_caves = defaultdict(list)
    for line in lines:
        cave1, cave2 = line.split('-', 1)
        adjacent_caves[cave1].append(cave2)
        adjacent_caves[cave2].append(cave1)


def find_valid_paths(path, current_cave, revisited_cave):
    if current_cave == END:
        return 1

    if current_cave.islower() and current_cave in path:
        if current_cave == START or revisited_cave:
            return 0
        else:
            revisited_cave = current_cave

    return sum(map(lambda adjacent_cave: find_valid_paths(path + [current_cave], adjacent_cave, revisited_cave),
                   adjacent_caves[current_cave]))


def part_1():
    read_input()
    return find_valid_paths([], START, "revisiting not allowed")


def part_2():
    read_input()
    return find_valid_paths([], START, None)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
