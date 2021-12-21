import functools
from time import time

from util.file_input_processor import read_lines


"""
For part 1 we simply play the game as instructed until one of the players wins, keeping track of the game parameters.
For part 2 we recursively simulate the game for each possible universe until we see a win.
We then recursively sum up the winning scenarios from each sub-universe to get the total number of wins for each player.
We use memoization to avoid recalculating already observed universes.
"""


TRACK_LENGTH = 10
MAX_DICE_VALUE_P1 = 100
WINNING_SCORE_P1 = 1000
WINNING_SCORE_P2 = 21


def read_input():
    starting_positions = list(map(lambda line: int(line.split(' ')[-1]), read_lines()))
    return starting_positions[0], starting_positions[1]


def roll_dice(position, score, next_dice_value):
    move_positions = 3 * (next_dice_value + 1)
    next_dice_value = (next_dice_value + 3) % MAX_DICE_VALUE_P1
    next_dice_value = MAX_DICE_VALUE_P1 if next_dice_value == 0 else next_dice_value
    position = (position + move_positions) % TRACK_LENGTH
    position = TRACK_LENGTH if position == 0 else position
    score += position
    return position, score, next_dice_value


def part_1():
    player1_position, player2_position = read_input()
    player1_score = player2_score = 0
    next_dice_value = 1
    dice_rolls = 0
    while True:
        player1_position, player1_score, next_dice_value = roll_dice(player1_position, player1_score, next_dice_value)
        dice_rolls += 3
        if player1_score >= WINNING_SCORE_P1:
            break

        player2_position, player2_score, next_dice_value = roll_dice(player2_position, player2_score, next_dice_value)
        dice_rolls += 3
        if player2_score >= WINNING_SCORE_P1:
            break

    return min([player1_score, player2_score]) * dice_rolls


@functools.cache
def find_wins(p1_position, p1_score, p2_position, p2_score, turn, rolled):
    if turn <= 3:
        p1_position = (p1_position + rolled) % TRACK_LENGTH
        p1_position = TRACK_LENGTH if p1_position == 0 else p1_position
    else:
        p2_position = (p2_position + rolled) % TRACK_LENGTH
        p2_position = TRACK_LENGTH if p2_position == 0 else p2_position

    if turn == 3:
        p1_score += p1_position
        if p1_score >= WINNING_SCORE_P2:
            return 1, 0
    elif turn == 6:
        p2_score += p2_position
        if p2_score >= WINNING_SCORE_P2:
            return 0, 1

    p1_wins = p2_wins = 0
    for roll in [1, 2, 3]:
        p1_roll_wins, p2_roll_wins = find_wins(p1_position, p1_score, p2_position, p2_score, turn % 6 + 1, roll)
        p1_wins += p1_roll_wins
        p2_wins += p2_roll_wins

    return p1_wins, p2_wins


def part_2():
    player1_position, player2_position = read_input()
    player1_wins, player2_wins = find_wins(player1_position, 0, player2_position, 0, 0, 0)
    return max(player1_wins, player2_wins)


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
