from collections import deque
from itertools import chain
from time import time

from util.file_input_processor import read_int_grid
from util.grid_util import find_neighbours


def increase_energy_levels(energy_levels):
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[i])):
            energy_levels[i][j] += 1


def detect_flashes(energy_levels):
    flashed_octopuses = []
    flash_queue = deque()
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[i])):
            if energy_levels[i][j] > 9:
                flash_queue.append((i, j))

    while len(flash_queue) > 0:
        octopus = flash_queue.popleft()
        energy_levels[octopus[0]][octopus[1]] += 1

        if energy_levels[octopus[0]][octopus[1]] > 9 and octopus not in flashed_octopuses:
            flashed_octopuses.append(octopus)
            flash_queue.extend(find_neighbours(energy_levels, octopus, True))

    return len(flashed_octopuses)


def decrease_energy_levels(energy_levels):
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[i])):
            if energy_levels[i][j] > 9:
                energy_levels[i][j] = 0


def simulate_step(energy_levels):
    increase_energy_levels(energy_levels)
    flashes = detect_flashes(energy_levels)
    decrease_energy_levels(energy_levels)
    return flashes


def part_1():
    energy_levels = read_int_grid()

    return sum(simulate_step(energy_levels) for _ in range(100))


def part_2():
    energy_levels = read_int_grid()

    step = 0
    while True:
        step += 1
        simulate_step(energy_levels)
        if all(energy_level == 0 for energy_level in chain(*energy_levels)):
            return step


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
