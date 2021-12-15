from statistics import median, mean
from time import time

from util.file_input_processor import read_integer_line

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
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
