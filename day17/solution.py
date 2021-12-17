from math import sqrt
from time import time

from util.file_input_processor import read_text

"""
This solution assumes that the target area is always to the right and below of the submarine.
No attempt is made to generalise it to work regardless of where the submarine is in relation to the target area.

We start by determining the absolute minimum and maximum speeds that could potentially be valid.
We then simulate each combination of potentially valid horizontal and vertical speeds and keep track of the valid ones.
The result for part 1 is the maximum vertical position, calculated using Gauss' Formula based on the top speed.
The result to part 2 is simply the number of valid speeds found.
"""


def read_target_area():
    components = read_text().split(' ')[2:]
    x_components = components[0].strip('x=,').split('..')
    y_components = components[1].strip('y=,').split('..')
    return (int(x_components[0]), int(x_components[1])), (int(y_components[0]), int(y_components[1]))


def is_in_target_area(x, y, target_area):
    return target_area[0][0] <= x <= target_area[0][1] and target_area[1][0] <= y <= target_area[1][1]


def is_valid_velocity(x_velocity, y_velocity, target_area):
    x = y = 0

    while x <= target_area[0][1] and y >= target_area[1][0]:
        x += x_velocity
        y += y_velocity

        if is_in_target_area(x, y, target_area):
            return True

        if x_velocity > 0:
            x_velocity -= 1
        y_velocity -= 1

    return False


def find_valid_velocities(target_area):
    # Because the speed keeps decreasing by 1, we need to make sure it doesn't reach 0 before reaching the target area.
    # We can use the inverse of Gauss' formula to determine the minimum speed needed for this.
    # This works because if we start with speed 5 for example, it will have speeds 5, 4, 3, 2, 1, before reaching 0.
    minimum_horizontal_velocity = int(sqrt(2 * target_area[0][0]))

    # At this speed it will reach the right limit of the target area on the first step.
    # If it goes any faster it will overshoot on the first step.
    maximum_horizontal_velocity = target_area[0][1]

    # At this speed it will reach the bottom limit of the target area on the first step.
    # If it goes any faster it will overshoot on the first step.
    minimum_vertical_velocity = target_area[1][0]

    # If the vertical speed is positive it will create an arc, with the top being reached when the vertical speed is 0.
    # The probe will pass the starting vertical position on the way back at the same negated speed it left the sub.
    # Therefore if its speed at this time is greater than this it will overshoot on the way back.
    maximum_vertical_velocity = -minimum_vertical_velocity

    valid_velocities = []
    for horizontal_velocity in range(minimum_horizontal_velocity, maximum_horizontal_velocity + 1):
        for vertical_velocity in range(minimum_vertical_velocity, maximum_vertical_velocity + 1):
            if is_valid_velocity(horizontal_velocity, vertical_velocity, target_area):
                valid_velocities.append((horizontal_velocity, vertical_velocity))
    return valid_velocities


def part_1():
    target_area = read_target_area()
    valid_velocities = find_valid_velocities(target_area)
    maximum_vertical_velocity_reached = max(map(lambda velocity: velocity[1], valid_velocities))
    return maximum_vertical_velocity_reached * (maximum_vertical_velocity_reached + 1) // 2


def part_2():
    target_area = read_target_area()
    valid_velocities = find_valid_velocities(target_area)
    return len(valid_velocities)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
