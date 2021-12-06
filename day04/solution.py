from util.file_input_processor import *

BOARD_SIZE = 5
DRAWN = -1


def read_board(lines):
    return list(map(lambda line: list(map(int, line.split())), lines))


def read():
    input_lines = read_lines()

    numbers = list(map(int, input_lines[0].split(',')))

    boards = []
    for i in range(2, len(input_lines), BOARD_SIZE + 1):
        boards.append(read_board(input_lines[i:i + BOARD_SIZE]))

    return numbers, boards


def mark_number_on_boards(number, boards):
    for board in boards:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == number:
                    board[i][j] = DRAWN


def check_if_winner(board):
    # Check lines
    for line in board:
        if all(number == DRAWN for number in line):
            return True

    # Check columns
    for column in range(BOARD_SIZE):
        valid_column = True
        for line in board:
            if line[column] != DRAWN:
                valid_column = False
                break
        if valid_column:
            return True

    return False


def sum_board(board):
    return sum(map(lambda line: sum(filter(lambda number: number != DRAWN, line)), board))


def part_1():
    numbers, boards = read()

    for number in numbers:
        mark_number_on_boards(number, boards)
        winner = list(filter(check_if_winner, boards))
        if winner:
            return number * sum_board(winner[0])


def part_2():
    numbers, boards = read()

    for number in numbers:
        mark_number_on_boards(number, boards)
        winners = list(filter(check_if_winner, boards))
        if winners:
            boards = list(filter(lambda board: board not in winners, boards))
        if len(boards) == 0:
            return number * sum_board(winners[0])


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
