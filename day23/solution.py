import sys
from copy import deepcopy
from time import time

from util.file_input_processor import *


# Christmas things took priority and I didn't get the time to code this in 2021.
# In 2022, day 2, I decided to give it a go.

# I managed to find the result to part 1 manually while trying to understand the problem on my input: 19046.
# I had a quick try to do the same thing for part 2 but obviously no luck as it's much harder.
# This is Advent of CODE after all, so I decided to code a solution.

# The implementation below uses an Amp class to store the current location of an amphipod
# and the State class to store the state for the entire burrow at any one time.
# I use a Breadth-First Search algorithm to find all the valid possible next states given a state.

# The algorithm works, but it is extremely slow.
# In order to optimise it, I've decided to sort the states by lowest cost after a state is processed.
# This pairs well with limiting the amount of potential states to process next, keeping only the best X.

# This works just fine for part 2, and I quickly got the answer - 47484.
# For part 1 it doesn't get the correct result, but it does get very close - 19092 instead of 19046.
# I got both stars after spending far too long on it so this is good enough for me :)


def part_1():
    return run_part(False, 100)


def part_2():
    return run_part(True, 2000)


def run_part(part2, keep_best_number):
    initial_state = read_input(part2)
    states = [initial_state]
    min_cost = sys.maxsize
    while states:
        states.sort(key=lambda s: s.cost)
        states = states[:keep_best_number]
        current_state = states.pop(0)
        if current_state.is_complete():
            print(f"Found solution with cost {current_state.cost}")
            if current_state.cost < min_cost:
                min_cost = current_state.cost
                break

        for amp in current_state.amps:
            possible_new_states = find_possible_new_states(current_state, amp)
            [states.append(state) for state in possible_new_states]

    return min_cost


hallway_door_indices = [0, 3, 5, 7, 9]


def find_possible_new_states(current_state, amp):
    if amp.is_in_room():
        return find_moves_to_hallway(current_state, amp)
    else:
        return find_moves_to_room(current_state, amp)


def find_moves_to_hallway(current_state, amp):
    # Check if this amp is in a valid position already.
    if amp.amp_type == amp.room and all(space in [0, amp.amp_type] for space in current_state.rooms[amp.room]):
        return []

    # Check if this amp is not blocked by another amp in the room.
    for depth in range(amp.depth):
        if current_state.rooms[amp.room][depth] != 0:
            return []

    new_possible_states = []

    # Move left
    for i in reversed(range(1, hallway_door_indices[amp.room])):
        # Can't stop in front of doors
        if i in hallway_door_indices:
            continue

        # Can't move here or any further as there's an amp in the way.
        if current_state.hallway[i] != 0:
            break

        new_possible_state = deepcopy(current_state)
        move_amp_to_hallway(new_possible_state, amp, i)
        new_possible_states.append(new_possible_state)

    # Move right
    for i in range(hallway_door_indices[amp.room], len(current_state.hallway)):
        # Can't stop in front of doors
        if i in hallway_door_indices:
            continue

        # Can't move here or any further as there's an amp in the way.
        if current_state.hallway[i] != 0:
            break

        new_possible_state = deepcopy(current_state)
        move_amp_to_hallway(new_possible_state, amp, i)
        new_possible_states.append(new_possible_state)

    return new_possible_states


def find_moves_to_room(current_state, amp):
    # Check if the room is in a good state for moving in.
    for space in current_state.rooms[amp.amp_type]:
        if space not in [0, amp.amp_type]:
            return []

    # Check if there aren't any obstacles on the way to the room.
    room_door_index = hallway_door_indices[amp.amp_type]
    for other_amp in current_state.amps:
        if amp == other_amp or other_amp.is_in_room():
            continue
        if amp.hallway < other_amp.hallway < room_door_index or room_door_index < other_amp.hallway < amp.hallway:
            return []

    # Move is possible, do it.
    new_possible_state = deepcopy(current_state)
    move_amp_to_room(new_possible_state, amp)
    return [new_possible_state]


def move_amp_to_room(new_possible_state, old_amp):
    amp = next(new_amp for new_amp in new_possible_state.amps
               if new_amp.hallway == old_amp.hallway)

    for i in reversed(range(len(new_possible_state.rooms[amp.amp_type]))):
        if new_possible_state.rooms[amp.amp_type][i] == 0:
            move_distance = abs(amp.hallway - hallway_door_indices[amp.amp_type]) + i
            new_possible_state.cost += move_distance * pow(10, amp.amp_type - 1)

            # Move
            new_possible_state.hallway[amp.hallway] = 0
            new_possible_state.rooms[amp.amp_type][i] = amp.amp_type
            amp.room = amp.amp_type
            amp.depth = i
            amp.hallway = None
            break


def move_amp_to_hallway(new_possible_state, old_amp, i):
    amp = next(new_amp for new_amp in new_possible_state.amps
               if new_amp.room == old_amp.room and new_amp.depth == old_amp.depth)

    move_distance = abs(i - hallway_door_indices[amp.room]) + amp.depth
    new_possible_state.cost += move_distance * pow(10, amp.amp_type - 1)

    new_possible_state.hallway[i] = amp.amp_type
    new_possible_state.rooms[amp.room][amp.depth] = 0
    amp.room = None
    amp.depth = None
    amp.hallway = i


class Amp:
    def __init__(self, amp_type, hallway, room, depth):
        self.amp_type = amp_type
        self.hallway = hallway
        self.room = room
        self.depth = depth

    def is_in_room(self):
        return self.room is not None and self.depth is not None

    def __str__(self):
        location = f"Hallway {self.hallway}" if self.hallway else f"Room {self.room} at depth {self.depth}"
        return f'Type: {self.amp_type} | {location}'

    def __repr__(self):
        return self.__str__()


class State:
    def __init__(self, hallway, rooms):
        self.hallway = hallway
        self.rooms = rooms
        self.amps = self.locate_amps()
        self.cost = 0

    def locate_amps(self):
        amps = []
        for i in range(len(self.hallway)):
            if self.hallway[i] != 0:
                amps.append(Amp(self.hallway[i], i, None, None))
        for ri in range(len(self.rooms)):
            for depth in range(len(self.rooms[ri])):
                if self.rooms[ri][depth] != 0:
                    amps.append(Amp(self.rooms[ri][depth], None, ri, depth))
        return amps

    def is_complete(self):
        for amp in self.amps:
            if amp.hallway is not None:
                return False
            if amp.room != amp.amp_type:
                return False
        return True

    def __str__(self):
        return f'{self.hallway} - {self.rooms}'

    def __repr__(self):
        return self.__str__()


def read_input(part2):
    lines = read_lines()
    hallway = [0] * (len(lines[1]) - 1)
    lines = lines[2:-1]
    if part2:
        lines.insert(1, "  #D#C#B#A#")
        lines.insert(2, "  #D#B#A#C#")

    rooms = [[0] for _ in range(4)]
    rooms.insert(0, [])
    for line in lines:
        rooms[1].append(room_letter_to_int(line[3]))
        rooms[2].append(room_letter_to_int(line[5]))
        rooms[3].append(room_letter_to_int(line[7]))
        rooms[4].append(room_letter_to_int(line[9]))

    return State(hallway, rooms)


def room_letter_to_int(letter):
    if letter == 'A':
        return 1
    if letter == 'B':
        return 2
    if letter == 'C':
        return 3
    if letter == 'D':
        return 4
    raise Exception


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
