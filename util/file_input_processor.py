INPUT_FILE_NAME = "input.txt"


def read_text():
    with open(INPUT_FILE_NAME) as f:
        return f.read()


def read_lines():
    with open(INPUT_FILE_NAME) as f:
        return f.read().splitlines()


def read_integers():
    input_lines = read_lines()
    return [int(i) for i in input_lines]
