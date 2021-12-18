from copy import deepcopy
from math import floor, ceil
from time import time

from util.file_input_processor import read_lines


"""
This is the first solution I implemented and structures the data into a binary tree. Part 2 runs in about 4 seconds.
While implementing the binary tree solution I realised that the operations can be done much easier on a list,
so have also implemented the list-based solution in solution_list.py after implementing this.

We first parse the input into a tree of elements by recursively processing the contents of each pair of brackets.
We then reduce the tree of elements by recursively traversing it and applying the relevant operations.
The result for the first part is found by recursively calculating the magnitude of the summed lines. 
The result for the second part is found by recursively calculating the maximum magnitude of all pairs of lines. 
"""


class Element:
    def __init__(self, left=None, right=None, number=None):
        self.left = left
        self.right = right
        self.number = number

    def __str__(self):
        return str(self.number) if self.number is not None else f'[{self.left},{self.right}]'

    def __repr__(self):
        return self.__str__()


def find_index_of_matching_closing_bracket(text, opening_bracket_index):
    open_brackets = 0
    for i in range(opening_bracket_index, len(text)):
        if text[i] == '[':
            open_brackets += 1
        elif text[i] == ']':
            open_brackets -= 1

        if open_brackets == 0:
            return i


def read_element(text):
    left_closing_bracket_index = 0
    if text[0].isdigit():
        left = Element(number=int(text[0]))
    else:
        left_closing_bracket_index = find_index_of_matching_closing_bracket(text, 0)
        left = read_element(text[1:left_closing_bracket_index])

    if text[left_closing_bracket_index + 2].isdigit():
        right = Element(number=int(text[left_closing_bracket_index + 2]))
    else:
        right_closing_bracket_index = find_index_of_matching_closing_bracket(text, left_closing_bracket_index + 2)
        right = read_element(text[left_closing_bracket_index + 3:right_closing_bracket_index])

    return Element(left, right)


def add_to_leftmost_element(element, value):
    if element.number is not None:
        element.number += value
        return True

    added = add_to_leftmost_element(element.left, value)
    if not added:
        added = add_to_leftmost_element(element.right, value)

    return added


def add_to_rightmost_element(element, value):
    if element.number is not None:
        element.number += value
        return True

    added = add_to_rightmost_element(element.right, value)
    if not added:
        added = add_to_rightmost_element(element.left, value)

    return added


def explode_element(element, nesting_depth=0):
    if element.number is not None:
        return False, None, None

    if nesting_depth == 4:
        return True, element.left.number, element.right.number

    has_reduced, exploded_value_left, exploded_value_right = explode_element(element.left, nesting_depth + 1)
    if has_reduced:
        if exploded_value_left is not None and exploded_value_right is not None:
            element.left = Element(number=0)
        if exploded_value_right is not None:
            added = add_to_leftmost_element(element.right, exploded_value_right)
            if added:
                exploded_value_right = None
        return has_reduced, exploded_value_left, exploded_value_right

    has_reduced, exploded_value_left, exploded_value_right = explode_element(element.right, nesting_depth + 1)
    if has_reduced:
        if exploded_value_left is not None and exploded_value_right is not None:
            element.right = Element(number=0)
        if exploded_value_left is not None:
            added = add_to_rightmost_element(element.left, exploded_value_left)
            if added:
                exploded_value_left = None
        return has_reduced, exploded_value_left, exploded_value_right

    return False, None, None


def split_element(element, nesting_depth=0):
    if element.number is not None:
        if element.number >= 10:
            return True, Element(Element(number=floor(element.number / 2)), Element(number=ceil(element.number / 2)))
        else:
            return False, None

    has_reduced, split_value = split_element(element.left, nesting_depth + 1)
    if has_reduced:
        if split_value is not None:
            element.left = split_value
            split_value = None
        return has_reduced, split_value

    has_reduced, split_value = split_element(element.right, nesting_depth + 1)
    if has_reduced:
        if split_value is not None:
            element.right = split_value
            split_value = None
        return has_reduced, split_value

    return False, None


def reduce_element(element):
    has_reduced = True
    while has_reduced:
        has_reduced = explode_element(element)
        if has_reduced[0]:
            continue
        has_reduced = split_element(element)[0]


def calculate_magnitude(element):
    if element.number is not None:
        return element.number

    return 3 * calculate_magnitude(element.left) + 2 * calculate_magnitude(element.right)


def part_1():
    lines = read_lines()
    elements = list(map(lambda line: read_element(line[1:-1]), lines))
    result = elements[0]
    for i in range(1, len(elements)):
        result = Element(result, elements[i])
        reduce_element(result)

    magnitude = calculate_magnitude(result)
    return magnitude


def part_2():
    lines = read_lines()
    elements = list(map(lambda line: read_element(line[1:-1]), lines))
    max_magnitude = 0
    for element1 in elements:
        for element2 in elements:
            if element1 == element2:
                continue
            added_element = Element(deepcopy(element1), deepcopy(element2))
            reduce_element(added_element)
            magnitude = calculate_magnitude(added_element)
            if magnitude > max_magnitude:
                max_magnitude = magnitude
    return max_magnitude


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
