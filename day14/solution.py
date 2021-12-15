from collections import defaultdict
from time import time

from util.file_input_processor import read_lines

"""
This solution relies on the observation that on each step,
each polymer pair splits into 2 polymer pairs and adds 1 new element to the polymer.
Therefore, we only need to keep track of how many of each pair we have and how many elements have been added.
On each step we go through all the pairs that have already occurred and split them,
resulting in the same number of the 2 resulting pairs being added, along with the same number of the new element.
"""


def read_input():
    lines = read_lines()

    template = lines[0]
    rules = dict(line.split(' -> ') for line in lines[2:])

    return template, rules


def create_element_occurrence_dict(polymer_template):
    occurrences = defaultdict(lambda: 0)
    for element in polymer_template:
        occurrences[element] += 1
    return occurrences


def create_pair_occurrence_dict(polymer_template):
    occurrences = defaultdict(lambda: 0)
    for i in range(1, len(polymer_template)):
        occurrences[polymer_template[i - 1] + polymer_template[i]] += 1
    return occurrences


def execute_step(element_occurrences, pair_occurrences, rules):
    new_pair_occurrences = defaultdict(lambda: 0)
    for polymer in pair_occurrences.keys():
        element_occurrences[rules[polymer]] += pair_occurrences[polymer]
        new_pair_occurrences[polymer[0] + rules[polymer]] += pair_occurrences[polymer]
        new_pair_occurrences[rules[polymer] + polymer[1]] += pair_occurrences[polymer]
    return element_occurrences, new_pair_occurrences


def get_result_after_steps(steps):
    polymer_template, rules = read_input()
    element_occurrences = create_element_occurrence_dict(polymer_template)
    pair_occurrences = create_pair_occurrence_dict(polymer_template)

    for _ in range(steps):
        element_occurrences, pair_occurrences = execute_step(element_occurrences, pair_occurrences, rules)

    least_common_element = min(element_occurrences, key=element_occurrences.get)
    most_common_element = max(element_occurrences, key=element_occurrences.get)

    return element_occurrences[most_common_element] - element_occurrences[least_common_element]


def part_1():
    return get_result_after_steps(10)


def part_2():
    return get_result_after_steps(40)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
