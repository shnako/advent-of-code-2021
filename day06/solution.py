from collections import deque
from time import time

from util.file_input_processor import read_integer_line

"""
This solution is based on the observation that the number of fish is going to be extremely large after not many days,
but the number of days we care about is limited to 8.
Therefore, instead of having a list of all the fish, we use a deque of the number of fish that will spawn by day.
The number at the front of the deque is the number of fish that will spawn in 0 days and in 8 days at the back.
Every day we pop the number of fish at the left (day 0 - the fish ready to reproduce), moving all the spawn days down.
We add them to the number of fish ready to reproduce after 6 days and set their offspring (same number) as
the fish that will reproduce after 8 days.
This way we can efficiently simulate any number of days so the solutions to part 1 and part 2 become the same.
"""


def read_spawn_queue():
    fish_spawn_days = read_integer_line()
    spawn_days = [0] * 9
    for fish in fish_spawn_days:
        spawn_days[fish] += 1
    return deque(spawn_days)


def simulate_spawn_days(spawn_q, days):
    for day in range(days):
        spawned_fish = spawn_q.popleft()
        spawn_q[6] += spawned_fish
        spawn_q.append(spawned_fish)


def part_1():
    spawn_q = read_spawn_queue()
    simulate_spawn_days(spawn_q, 80)
    return sum(spawn_q)


def part_2():
    spawn_q = read_spawn_queue()
    simulate_spawn_days(spawn_q, 256)
    return sum(spawn_q)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
