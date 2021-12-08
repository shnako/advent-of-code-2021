from util.file_input_processor import *


def parse_signals(signals):
    return list(map(lambda signal: ''.join(sorted(signal)), signals.split()))


def read_entry(line):
    components = line.split(' | ')

    signal_patterns = parse_signals(components[0])
    output_patterns = parse_signals(components[1])

    return signal_patterns, output_patterns


def read_entries():
    lines = read_lines()
    return list(map(read_entry, lines))


def determine_signal_to_digit_mapping(signals):
    mapping = dict()

    # Find digit 1 - the digit containing 2 segments
    mapping[1] = next(signal for signal in signals
                      if len(signal) == 2)

    # Find digit 7 - the digit containing 3 segments
    mapping[7] = next(signal for signal in signals
                      if len(signal) == 3)

    # Find digit 4 - the digit containing 4 segments
    mapping[4] = next(signal for signal in signals
                      if len(signal) == 4)

    # Find digit 8 - the digit containing 7 segments
    mapping[8] = next(signal for signal in signals
                      if len(signal) == 7)

    # Find digit 3 - the digit containing 5 segments and digit 1
    mapping[3] = next(signal for signal in signals
                      if len(signal) == 5 and set(mapping[1]).issubset(signal))

    # Find digit 9 - the digit containing 6 segments and digit 4
    mapping[9] = next(signal for signal in signals
                      if len(signal) == 6 and set(mapping[4]).issubset(signal))

    # Find digit 0 - the digit containing 6 segments and digit 1 and is not digit 9
    mapping[0] = next(signal for signal in signals
                      if len(signal) == 6 and set(mapping[1]).issubset(signal) and signal != mapping[9])

    # Find digit 6 - the digit containing 6 segments and is not digit 9 and is not digit 0
    mapping[6] = next(signal for signal in signals
                      if len(signal) == 6 and signal != mapping[9] and signal != mapping[0])

    # Find digit 5 - the digit containing 5 segments and has only 1 segment different from digit 6
    mapping[5] = next(signal for signal in signals
                      if len(signal) == 5 and len(set(mapping[6]) - set(signal)) == 1)

    # Find digit 2 - the digit containing 5 segments and is not digit 3 and is not digit 5
    mapping[2] = next(signal for signal in signals
                      if len(signal) == 5 and signal != mapping[3] and signal != mapping[5])

    # Flip the dict so that is maps signals to digits
    return {v: k for k, v in mapping.items()}


def determine_output_value(entry):
    signal_to_digit_mapping = determine_signal_to_digit_mapping(entry[0])

    decoded_outputs = map(lambda output_signal: signal_to_digit_mapping[output_signal], entry[1])

    return int(''.join(map(str, decoded_outputs)))


def count_occurrences_of_digits_in_numbers(digits, numbers):
    occurrences = 0
    for number in numbers:
        str_value = str(number)
        for digit in digits:
            occurrences += str_value.count(digit)
    return occurrences


def part_1():
    entries = read_entries()

    output_values = list(map(determine_output_value, entries))

    return count_occurrences_of_digits_in_numbers(['1', '4', '7', '8'], output_values)


def part_2():
    entries = read_entries()

    output_values = list(map(determine_output_value, entries))

    return sum(output_values)


if __name__ == "__main__":
    print(f'Part 1 solution: {part_1()}')
    print(f'Part 2 solution: {part_2()}')
