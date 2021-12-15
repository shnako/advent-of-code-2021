from time import time

from util.file_input_processor import read_int_grid
from util.grid_util import find_neighbours

"""
Part1:
We navigate through the heightmap and find the points where all the neighbours are higher. These are the low points.
The risk level for each low point is its height + 1. 
The result is the sum of the risk levels.

Part 2:
We start from every low point and do a Breadth First Search to find all neighbours with a height less than 9.
At the end of the BFS, the BFS list will contain all the points in the basin starting from that low point.
The size of each basin is therefore the size of its BFS list.
The result is the product of the sizes of the 3 largest basins.
"""


def is_local_minimum(heightmap, x, y):
    neighbours = find_neighbours(heightmap, (x, y))
    for neighbour in neighbours:
        if heightmap[x][y] >= heightmap[neighbour[0]][neighbour[1]]:
            return False
    return True


def find_low_points(heightmap):
    low_points = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if is_local_minimum(heightmap, i, j):
                low_points.append((i, j))
    return low_points


def find_basin_size(heightmap, low_point):
    basin_points = [low_point]

    i = 0
    while i < len(basin_points):
        neighbours = find_neighbours(heightmap, basin_points[i])
        for neighbour in neighbours:
            if heightmap[neighbour[0]][neighbour[1]] < 9 and neighbour not in basin_points:
                basin_points.append(neighbour)
        i += 1

    return len(basin_points)


def part_1():
    heightmap = read_int_grid()

    low_points = find_low_points(heightmap)

    return sum(map(lambda point: heightmap[point[0]][point[1]] + 1, low_points))


def part_2():
    heightmap = read_int_grid()

    low_points = find_low_points(heightmap)

    basin_sizes = list(map(lambda low_point: find_basin_size(heightmap, low_point), low_points))

    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
