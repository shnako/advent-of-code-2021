from statistics import median, mean

from util.file_input_processor import *

"""
The solution is based on the observation that the destination point is:
- for part 1: the median of the crab submarine positions
- for part 2: the mean   of the crab submarine positions
The result for each part is then the sum of the fuel consumed by each submarine to reach the destination point.
"""


def get_distances_to_destination(positions, destination):
    return map(lambda position: abs(destination - position), positions)


def part_1():
    positions = read_integer_line()
    destination = int(median(positions))
    distances_to_destination = get_distances_to_destination(positions, destination)
    return sum(distances_to_destination)


def part_2():
    positions = read_integer_line()
    destination = int(mean(positions))
    distances_to_destination = get_distances_to_destination(positions, destination)
    return sum(map(lambda distance: distance * (distance + 1) // 2, distances_to_destination))


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
