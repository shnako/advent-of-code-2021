import itertools
from collections import deque

from util.file_input_processor import read_lines
from util.grid_util import find_neighbours


def read_input():
    lines = read_lines()
    return list(map(lambda line: [int(energy) for energy in line], lines))


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
    energy_levels = read_input()

    return sum(simulate_step(energy_levels) for _ in range(100))


def part_2():
    energy_levels = read_input()

    step = 0
    while True:
        step += 1
        simulate_step(energy_levels)
        if all(energy_level == 0 for energy_level in itertools.chain(*energy_levels)):
            return step


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
