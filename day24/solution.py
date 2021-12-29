import functools
from math import floor, ceil
from time import time

from util.file_input_processor import read_lines

'''
An efficient generalised solution to the problem sadly doesn't seem achievable as it would take way too long to run.
The solution is based on the observation that the input is made up of 18 identical instructions, repeated 14 times.
There are only 3 variables changing in the instructions so we need to only read those from the input (a, b, c).
This information was probably in the documentation the tanuki ate.

With this information, we can write those 18 instructions as a parameterized function and simplify it (run_algorithm).
We then try all the numbers, digit by digit, using a recursive function.
We use memoization to avoid recalculating the potential solutions from a step if we've already calculated it.

The solution to both parts is the same, searching for the largest valid number in part 1 and the smallest in part 2.
Part 1 runs in about 10 seconds while part 2 takes about 10 minutes.
'''

global differences


def read_input():
    lines = read_lines()
    a = []
    b = []
    c = []
    for i in range(0, len(lines)):
        if i % 18 == 4:
            a.append(int(lines[i].split(' ')[-1]))
        if i % 18 == 5:
            b.append(int(lines[i].split(' ')[-1]))
        if i % 18 == 15:
            c.append(int(lines[i].split(' ')[-1]))

    global differences
    differences = (a, b, c)


# This is a simplified version of the input algorithm.
def run_algorithm(z, w, step):
    global differences

    a = differences[0][step]
    b = differences[1][step]
    c = differences[2][step]

    x = z % 26
    z /= a
    z = floor(z) if z > 0 else ceil(z)
    if x + b != w:
        z *= 26
        z += w + c

    return z


@functools.cache
def find_solution(digit, result, step, digit_range):
    if step == 14:
        return ' ' if result == 0 else None
    new_result = run_algorithm(result, digit, step) if step > -1 else 0
    for potential_digit in digit_range:
        partial_solution = find_solution(potential_digit, new_result, step + 1, digit_range)
        if partial_solution:
            return str(potential_digit) + partial_solution
    return None


def part_1():
    read_input()
    result = find_solution(0, 0, -1, range(9, 0, -1))
    return int(result[:-2])


def part_2():
    read_input()
    result = find_solution(0, 0, -1, range(1, 10))
    return int(result[:-2])


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
