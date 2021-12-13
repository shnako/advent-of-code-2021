from copy import deepcopy

from util.file_input_processor import *
from util.grid_util import print_grid


def read_input():
    lines = read_lines()

    points = set()
    folds = []
    for line in lines:
        if ',' in line:
            x, y = line.split(',', 1)
            points.add((int(x), int(y)))
        elif '=' in line:
            axis, value = line.split(' ')[-1].split('=', 1)
            folds.append((axis, int(value)))

    return points, folds


def fold_up(points, fold_line):
    for point in deepcopy(points):
        if point[1] > fold_line:
            points.add((point[0], fold_line - (point[1] - fold_line)))
            points.remove(point)


def fold_left(points, fold_line):
    for point in deepcopy(points):
        if point[0] > fold_line:
            points.add((fold_line - (point[0] - fold_line), point[1]))
            points.remove(point)


def fold_paper(points, folds):
    for fold in folds:
        if fold[0] == 'y':
            fold_up(points, fold[1])
        else:
            fold_left(points, fold[1])


def part_1():
    points, folds = read_input()
    folds = [folds[0]]
    fold_paper(points, folds)
    return len(points)


def part_2():
    points, folds = read_input()
    fold_paper(points, folds)
    print("The result is printed below:")
    print_grid(points, ' ', '█')
    return len(points)


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
