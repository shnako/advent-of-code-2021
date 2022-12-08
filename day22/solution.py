import re
import uuid
from time import time

from util.file_input_processor import *

"""
Christmas things took priority and I didn't get the time to code this in 2021, but did it during AoC 2022.
For part 1, we turn on and off every individual cube as described and then count the cubes that are on.
For part 2, the above is way too inefficient so a more optimal solution is needed.
For every ON cuboid, we determine the volume that has no intersections with any of the FOLLOWING ones.
We then add these volumes up to get the result.
The tricky bit here is that intersections can also have intersections, so we recursively check them against
all the following cuboids, and those intersections too and so on.
"""


def part_1():
    cuboids = read_input()
    cuboids = list(filter(lambda step: -50 < step.a[0] < 50, cuboids))

    space = {}
    for cuboid in cuboids:
        for x in range(cuboid.a[0], cuboid.b[0] + 1):
            for y in range(cuboid.a[1], cuboid.b[1] + 1):
                for z in range(cuboid.a[2], cuboid.b[2] + 1):
                    space[(x, y, z)] = cuboid.state

    return sum(cube for cube in space.values())


def part_2():
    cuboids = read_input()

    total = 0
    for i in range(0, len(cuboids)):
        volume = find_volume_without_intersection(cuboids[i], cuboids[i + 1:])
        if cuboids[i].state:
            total += volume

    return total


def find_volume_without_intersection(cuboid, following_steps):
    volume = cuboid.get_volume()
    intersections = list()
    for step in following_steps:
        intersection = get_cuboid_intersection(cuboid, step)
        if intersection:
            intersections.append(intersection)

    for i in range(len(intersections)):
        volume -= find_volume_without_intersection(intersections[i], intersections[i + 1:])

    return volume


def get_cuboid_intersection(c1, c2):
    x_intersection = get_axis_intersection(c1.a[0], c1.b[0], c2.a[0], c2.b[0])
    if x_intersection is None:
        return None

    y_intersection = get_axis_intersection(c1.a[1], c1.b[1], c2.a[1], c2.b[1])
    if y_intersection is None:
        return None

    z_intersection = get_axis_intersection(c1.a[2], c1.b[2], c2.a[2], c2.b[2])
    if z_intersection is None:
        return None

    return Cuboid(
        c2.state,
        (x_intersection[0], y_intersection[0], z_intersection[0]),
        (x_intersection[1], y_intersection[1], z_intersection[1])
    )


def get_axis_intersection(a1, a2, b1, b2):
    # Swap coordinates if they're flipped to make calculations simpler.
    if a1 > a2:
        a1, a2 = a2, a1
    if b1 > b2:
        b1, b2 = b2, b1

    # No overlap
    if a2 < b1 or b2 < a1:
        return None

    # a contains b
    if a1 <= b1 <= b2 <= a2:
        return b1, b2

    # b contains a
    if b1 <= a1 <= a2 <= b2:
        return a1, a2

    # Partial overlaps
    if a1 <= b1 <= a2 <= b2:
        return b1, a2
    if b1 <= a1 <= b2 <= a2:
        return a1, b2

    raise Exception("Could not determine intersection.")


class Cuboid:
    def __init__(self, state, a, b):
        self.id = uuid.uuid4()
        self.state = state
        self.a = a
        self.b = b
        self.intersections = list()

    def __str__(self):
        return f'{"on" if self.state else "off"} ' \
               f'[{self.a[0]},{self.a[1]},{self.a[2]}] [{self.b[0]},{self.b[1]},{self.b[2]}] '

    def __repr__(self):
        return self.__str__()

    def get_volume(self):
        return (abs(self.a[0] - self.b[0]) + 1) * (abs(self.a[1] - self.b[1]) + 1) * (abs(self.a[2] - self.b[2]) + 1)


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
