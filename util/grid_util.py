def find_neighbours(grid, point, include_diagonals=False):
    x = point[0]
    y = point[1]

    points = []
    if x - 1 >= 0:
        points.append((x - 1, y))
    if y - 1 >= 0:
        points.append((x, y - 1))
    if x + 1 < len(grid):
        points.append((x + 1, y))
    if y + 1 < len(grid[x]):
        points.append((x, y + 1))

    if include_diagonals:
        if x - 1 >= 0 and y - 1 >= 0:
            points.append((x - 1, y - 1))
        if x + 1 < len(grid) and y - 1 >= 0:
            points.append((x + 1, y - 1))
        if x - 1 >= 0 and y + 1 < len(grid[x]):
            points.append((x - 1, y + 1))
        if x + 1 < len(grid) and y + 1 < len(grid[x]):
            points.append((x + 1, y + 1))

    return points


def initialize_zero_grid(points):
    max_x = max(map(lambda point: point[0], points)) + 1
    max_y = max(map(lambda point: point[1], points)) + 1
    return [[0] * max_x for _ in range(max_y)]


def map_list_of_points_to_grid(points, char_to_use):
    grid = initialize_zero_grid(points)
    for point in points:
        grid[point[1]][point[0]] = char_to_use
    return grid


def print_grid(points, char_0, char_1):
    folded_paper = map_list_of_points_to_grid(points, 1)
    for line in folded_paper:
        print(''.join(map(lambda char: char_1 if char else char_0, line)))
