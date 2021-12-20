from collections import defaultdict
from time import time

from util.file_input_processor import read_lines

"""
We start by storing the image in a defaultdict mapping the coordinates tuple to the pixel value.
This gives us 2 advantages:
    - We don't have to resize the pixel grid when increasing it.
    - We can rely on it to provide the default value for the pixels outside of the defined area.

The gotcha here is that if the first value in the algorithm is '#' and the last one is '.', 
the pixels outside of the defined area will flip between on and off on every enhancement.
Therefore on even enhancement passes, for pixels outside of the defined area, 
we use the first algorithm value and for odd enhancement passes we use the last.
On each step we increase the image bounds in each direction by 1 as that's as far as any derived changes will go.
The result for each part is the number of lit pixels after 2 and 50 enhancement steps.
"""


def read_input():
    lines = read_lines()
    algorithm = lines[0]
    lines = lines[2:]

    image = defaultdict(lambda: '.')
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            image[(i, j)] = lines[i][j]

    return algorithm, image


def get_surrounding_pixels_number(pixel_coordinates, image):
    binary = ''
    for i in range(pixel_coordinates[0] - 1, pixel_coordinates[0] + 2):
        for j in range(pixel_coordinates[1] - 1, pixel_coordinates[1] + 2):
            binary += '1' if image[(i, j)] == '#' else '0'
    return int(binary, 2)


def enhance(image, algorithm, iteration):
    min_y = min(map(lambda key: key[0], image.keys())) - 1
    max_y = max(map(lambda key: key[0], image.keys())) + 1
    min_x = min(map(lambda key: key[1], image.keys())) - 1
    max_x = max(map(lambda key: key[1], image.keys())) + 1

    enhanced_image = defaultdict(lambda: algorithm[0] if iteration % 2 == 0 else algorithm[-1])
    for i in range(min_y, max_y + 1):
        for j in range(min_x, max_x + 1):
            algorithm_index = get_surrounding_pixels_number((i, j), image)
            enhanced_image[(i, j)] = algorithm[algorithm_index]
    return enhanced_image


def solve(iterations):
    algorithm, image = read_input()
    for iteration in range(iterations):
        image = enhance(image, algorithm, iteration)

    return sum(map(lambda key: 1 if image[key] == '#' else 0, image.keys()))


def part_1():
    return solve(2)


def part_2():
    return solve(50)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
