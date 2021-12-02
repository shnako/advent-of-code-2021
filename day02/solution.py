from util.file_input_processor import *


def parse_line(line):
    components = line.split()
    return tuple((components[0], int(components[1])))


def read_input():
    return list(map(parse_line, read_lines()))


def part_1():
    commands = read_input()

    position = depth = 0
    for command in commands:
        if command[0] == 'forward':
            position += command[1]
        elif command[0] == 'up':
            depth -= command[1]
        elif command[0] == 'down':
            depth += command[1]

    return position * depth


def part_2():
    commands = read_input()

    position = depth = aim = 0
    for command in commands:
        if command[0] == 'forward':
            position += command[1]
            depth += aim * command[1]
        elif command[0] == 'up':
            aim -= command[1]
        elif command[0] == 'down':
            aim += command[1]

    return position * depth


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
