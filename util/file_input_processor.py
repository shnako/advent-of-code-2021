INPUT_FILE_NAME = "input.txt"


def read_text():
    with open(INPUT_FILE_NAME) as f:
        return f.read()


def read_lines():
    with open(INPUT_FILE_NAME) as f:
        return f.read().splitlines()


def read_integer_lines():
    input_lines = read_lines()
    return [int(i) for i in input_lines]


def read_integer_line():
    input_lines = read_lines()
    return [int(i) for i in input_lines[0].split(",")]


def read_int_grid():
    input_lines = read_lines()
    return [list(map(lambda val: int(val), line)) for line in input_lines]
