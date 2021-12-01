from src.util.file_input_processor import *


def part_1():
    depths = read_integers()
    increases = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            increases += 1
    return increases


def part_2():
    depths = read_integers()
    increases = 0
    for i in range(1, len(depths) - 2):
        if depths[i] + depths[i + 1] + depths[i + 2] > depths[i - 1] + depths[i] + depths[i + 1]:
            increases += 1
    return increases


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
