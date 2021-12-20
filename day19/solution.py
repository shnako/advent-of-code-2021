from collections import defaultdict
from time import time

from util.file_input_processor import read_text

ORIENTATIONS = [
    [+1, +1, +1],
    [+1, +1, -1],
    [+1, -1, +1],
    [+1, -1, -1],
    [-1, +1, +1],
    [-1, +1, -1],
    [-1, -1, +1],
    [-1, -1, -1],
]

FLIPS = [
    [0, 1, 2],
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 0, 1],
    [2, 1, 0],
]


def rotate_beacons(beacons, orientation, flip):
    new_beacons = []
    for beacon in beacons:
        new_beacons.append(Point(
            beacon[flip[0]] * orientation[0],
            beacon[flip[1]] * orientation[1],
            beacon[flip[2]] * orientation[2]
        ))
    return new_beacons


def create_beacon_distance_map(beacons):
    beacon_distance_map = [[None] * len(beacons) for _ in range(len(beacons))]
    for i in range(len(beacons)):
        for j in range(len(beacons)):
            beacon_distance_map[i][j] = [beacons[i][0] - beacons[j][0],
                                         beacons[i][1] - beacons[j][1],
                                         beacons[i][2] - beacons[j][2]]
    return beacon_distance_map


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, coordinates):
        return cls(coordinates[0], coordinates[1], coordinates[2])

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z

    def __str__(self):
        return f'[{self.x},{self.y},{self.z}]'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))


class Orientation:
    def __init__(self, beacons):
        self.beacons = beacons
        self.beacon_distance_map = create_beacon_distance_map(beacons)


class Scanner:
    def __init__(self, beacons, is_rotation=False):
        self.position = None
        self.beacons = beacons
        self.correct_orientation = None

        self.orientations = []
        if not is_rotation:
            for orientation in ORIENTATIONS:
                for flip in FLIPS:
                    new_beacons = rotate_beacons(beacons, orientation, flip)
                    self.orientations.append(Orientation(new_beacons))


def read_input():
    scanner_texts = read_text().split('\n\n')
    scanners = []
    for scanner_text in scanner_texts:
        scanner_lines = scanner_text.split('\n')[1:]
        beacons = list(map(lambda line: Point.from_list(list(map(int, line.split(',')))), scanner_lines))
        scanners.append(Scanner(beacons))

    return scanners


def find_matching_beacons(correct_orientation, orientation):
    matching_beacons = set()
    for i1 in range(len(correct_orientation.beacons)):
        for j1 in range(0, i1):
            for i2 in range(len(orientation.beacons)):
                for j2 in range(0, i2):
                    if correct_orientation.beacon_distance_map[i1][j1] == orientation.beacon_distance_map[i2][j2]:
                        matching_beacons.add((correct_orientation.beacons[i1], orientation.beacons[i2]))
                        matching_beacons.add((correct_orientation.beacons[j1], orientation.beacons[j2]))
    return list(matching_beacons)


def find_most_common_distance(matching_beacons):
    distance_frequency_map = defaultdict(lambda: 0)

    for matching_beacon_pair in matching_beacons:
        distance = Point(
            matching_beacon_pair[0].x - matching_beacon_pair[1].x,
            matching_beacon_pair[0].y - matching_beacon_pair[1].y,
            matching_beacon_pair[0].z - matching_beacon_pair[1].z,
        )
        distance_frequency_map[distance] += 1

    most_common_distance = most_common_distance_count = -1
    for distance in distance_frequency_map:
        if most_common_distance_count < distance_frequency_map[distance]:
            most_common_distance = distance
            most_common_distance_count = distance_frequency_map[distance]

    return most_common_distance, most_common_distance_count


def find_overlapping_orientation(positioned_scanner, positionable_scanner):
    for orientation in positionable_scanner.orientations:
        matching_beacons = find_matching_beacons(positioned_scanner.correct_orientation, orientation)
        most_common_distance, most_common_distance_count = find_most_common_distance(matching_beacons)
        if most_common_distance_count >= 11:
            return most_common_distance, orientation
    return None, None


def find_overlaps(scanners):
    for positioned_scanner in filter(lambda scanner: scanner.position is not None, scanners):
        for positionable_scanner in filter(lambda scanner: scanner.position is None, scanners):
            distance, overlapping_orientation = find_overlapping_orientation(positioned_scanner, positionable_scanner)
            if overlapping_orientation:
                positionable_scanner.position = Point(
                    positioned_scanner.position.x + distance.x,
                    positioned_scanner.position.y + distance.y,
                    positioned_scanner.position.z + distance.z
                )
                print(f"Found scanner at position: {positionable_scanner.position}")

                positionable_scanner.correct_orientation = overlapping_orientation
                return


def calculate_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])


def part_1():
    scanners = read_input()
    scanners[0].position = Point(0, 0, 0)
    scanners[0].correct_orientation = scanners[0].orientations[0]

    while any(scanner.position is None for scanner in scanners):
        print('Scanners positioned: ' + str(len(list(filter(lambda scanner: scanner.position is not None, scanners)))))
        find_overlaps(scanners)

    beacons = set()
    for scanner in scanners:
        for beacon in scanner.correct_orientation.beacons:
            beacons.add(Point(
                scanner.position.x + beacon.x,
                scanner.position.y + beacon.y,
                scanner.position.z + beacon.z
            ))

    # build map
    return len(beacons)


def part_2():
    scanners = read_input()
    scanners[0].position = Point(0, 0, 0)
    scanners[0].correct_orientation = scanners[0].orientations[0]

    while any(scanner.position is None for scanner in scanners):
        print('Scanners positioned: ' + str(len(list(filter(lambda scanner: scanner.position is not None, scanners)))))
        find_overlaps(scanners)

    max_distance = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            manhattan_distance = calculate_manhattan_distance(scanner1.position, scanner2.position)
            if manhattan_distance > max_distance:
                max_distance = manhattan_distance
    return max_distance


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
