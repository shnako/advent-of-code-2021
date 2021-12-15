from statistics import median
from time import time

from util.file_input_processor import read_lines

SYNTAX_ERROR_SCORE_TABLE = dict({
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
})

POINT_VALUE_TABLE = dict({
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
})

CHAR_PAIRS = dict({
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
})


def process_line(line):
    stack = []

    for char in line:
        if char in CHAR_PAIRS.keys():
            stack.append(char)
        else:
            previous_char = stack.pop()
            if CHAR_PAIRS[previous_char] != char:
                return stack, char

    return stack, None


def calculate_completion_string_score(stack):
    score = 0
    while len(stack) > 0:
        score = score * 5 + POINT_VALUE_TABLE[stack.pop()]
    return score


def part_1():
    lines = read_lines()

    score = 0
    for line in lines:
        remaining_stack, illegal_character = process_line(line)
        if illegal_character:
            score += SYNTAX_ERROR_SCORE_TABLE[illegal_character]

    return score


def part_2():
    lines = read_lines()

    incomplete_stacks = []
    for line in lines:
        remaining_stack, illegal_character = process_line(line)
        if not illegal_character:
            incomplete_stacks.append(remaining_stack)

    scores = map(calculate_completion_string_score, incomplete_stacks)

    return median(scores)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
