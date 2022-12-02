import re
from time import time

from util.file_input_processor import *


# Christmas things took priority and I didn't get the time to code this. Maybe one day I will.

def part_1():
    steps = read_input()
    steps = list(filter(lambda step: -50 < step.a[0] < 50, steps))

    space = {}
    for step in steps:
        for x in range(step.a[0], step.b[0] + 1):
            for y in range(step.a[1], step.b[1] + 1):
                for z in range(step.a[2], step.b[2] + 1):
                    space[(x, y, z)] = step.state

    return sum(state for state in space.values())


def part_2():
    steps = read_input()


class Cuboid:
    def __init__(self, state, a, b):
        self.state = state
        self.a = a
        self.b = b


def read_input():
    input_lines = read_lines()
    return list(map(parse_line, input_lines))


def parse_line(input_line):
    components = input_line.split(" ")
    state = components[0] == "on"
    coordinates = re.split('[xyz=.,]+', components[1])
    return Cuboid(
        state,
        (int(coordinates[1]), int(coordinates[3]), int(coordinates[5])),
        (int(coordinates[2]), int(coordinates[4]), int(coordinates[6]))
    )


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
