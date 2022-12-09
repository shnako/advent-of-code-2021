from time import time

from util.file_input_processor import *


# I coded the solution to part 1 in 2021 on my work laptop but didn't push it as I wanted to push both parts together.
# Since then, I switched jobs and lost the solution when my laptop was wiped.
# During AoC 2022 I finished all the remaining problems and coded this one again for completeness.

# For part 1, we simulate the movements until no more movements are possible.
# We look at all eastbound urchins, determine if they can move and create a matrix with the same indices,
# containing True if they can move and False if not.
# We then use this map to move all the eastbound urchins, after which we do the same thing with the southbound ones.
# Once we determine that no urchins can move (no True value in either matrix), we return the result (number of moves).

# For part 2, we simply need to have solved all the previous problems to get the star so nothing to code.

def part_1():
    cucumbers = [list(line) for line in read_lines()]

    movements = 0
    while True:
        east_movement_matrix = get_movement_matrix(cucumbers, ">")
        move(cucumbers, east_movement_matrix)
        south_movement_matrix = get_movement_matrix(cucumbers, "v")
        move(cucumbers, south_movement_matrix)

        movements += 1
        if not any(True in sublist for sublist in east_movement_matrix + south_movement_matrix):
            break

    return movements


def part_2():
    return "Merry Christmas!"


def get_movement_matrix(cucumbers, direction):
    movement_array = list()

    for i in range(len(cucumbers)):
        movement_line = list()

        for j in range(len(cucumbers[i])):
            if direction == cucumbers[i][j] == ">" and cucumbers[i][nexti(j, cucumbers[i])] == ".":
                movement_line.append(True)
            elif direction == cucumbers[i][j] == "v" and cucumbers[nexti(i, cucumbers)][j] == ".":
                movement_line.append(True)
            else:
                movement_line.append(False)

        movement_array.append(movement_line)

    return movement_array


def move(cucumbers, movement_array):
    for i in range(len(cucumbers)):
        for j in range(len(cucumbers[i])):
            if movement_array[i][j]:
                if cucumbers[i][j] == ">":
                    cucumbers[i][j], cucumbers[i][nexti(j, cucumbers[i])] = cucumbers[i][nexti(j, cucumbers[i])], cucumbers[i][j]
                elif cucumbers[i][j] == "v":
                    cucumbers[i][j], cucumbers[nexti(i, cucumbers)][j] = cucumbers[nexti(i, cucumbers)][j], cucumbers[i][j]


def nexti(index, lst):
    return index + 1 if index + 1 < len(lst) else 0


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
