import heapq
import sys
from copy import deepcopy
from time import time

from util.file_input_processor import read_int_grid
from util.grid_util import find_neighbours

"""
We use Dijkstra's algorithm to find the minimum risk from the starting point to every other point.
The result for both parts is then the minimum path risk for the destination point.
"""


def get_minimum_path_risk_map(risk_map, start_x, start_y):
    minimum_risk_map = [[sys.maxsize] * len(risk_map[i]) for i in range(len(risk_map))]
    minimum_risk_map[start_y][start_x] = 0

    visited = set()
    next_positions = [(0, (start_y, start_x))]

    while len(next_positions) > 0:
        current_position = heapq.heappop(next_positions)[1]
        current_risk = minimum_risk_map[current_position[0]][current_position[1]]

        neighbours = filter(lambda neighbour: neighbour not in visited, find_neighbours(risk_map, current_position))
        for neighbour in neighbours:
            if current_risk + risk_map[neighbour[0]][neighbour[1]] < minimum_risk_map[neighbour[0]][neighbour[1]]:
                minimum_risk_map[neighbour[0]][neighbour[1]] = current_risk + risk_map[neighbour[0]][neighbour[1]]
                heapq.heappush(next_positions, (minimum_risk_map[neighbour[0]][neighbour[1]], neighbour))

        visited.add(current_position)

    return minimum_risk_map


def place_map_tile(risk_map, tile, start_y, start_x):
    for i in range(len(tile)):
        for j in range(len(tile[i])):
            risk_map[start_y + i][start_x + j] = tile[i][j]


def get_increased_risk_tile(risk_tile):
    increased_risk_tile = []
    for i in range(len(risk_tile)):
        increased_risk_tile.append([])
        for j in range(len(risk_tile[i])):
            increased_risk_tile[i].append(risk_tile[i][j] + 1 if risk_tile[i][j] < 9 else 1)
    return increased_risk_tile


def build_larger_map(initial_tile):
    tile_height = len(initial_tile)
    tile_width = len(initial_tile[0])

    larger_risk_map = [[0] * tile_width * 5 for _ in range(tile_height * 5)]

    current_tile = initial_tile
    for i in range(5):
        previous_vertical_map_tile = deepcopy(current_tile)
        for j in range(5):
            place_map_tile(larger_risk_map, current_tile, i * tile_height, j * tile_width)
            current_tile = get_increased_risk_tile(current_tile)
        current_tile = get_increased_risk_tile(previous_vertical_map_tile)

    return larger_risk_map


def part_1():
    risk_map = read_int_grid()
    minimum_path_risk_map = get_minimum_path_risk_map(risk_map, 0, 0)
    return minimum_path_risk_map[-1][-1]


def part_2():
    risk_map = read_int_grid()
    larger_risk_map = build_larger_map(risk_map)
    minimum_path_risk_map = get_minimum_path_risk_map(larger_risk_map, 0, 0)
    return minimum_path_risk_map[-1][-1]


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
