from math import prod
from time import time

from util.file_input_processor import read_text


class Packet:
    def __init__(self, version_binary, type_id_binary, literal, sub_packets):
        self.version = int(version_binary, 2)
        self.type_id = int(type_id_binary, 2)
        self.literal = None if literal is None else int(literal, 2)
        self.sub_packets = sub_packets


def take_bits(bits_to_take, bits):
    return bits[:bits_to_take], bits[bits_to_take:]


def parse_packet(transmission):
    version, transmission = take_bits(3, transmission)
    type_id, transmission = take_bits(3, transmission)

    if int(type_id, 2) == 4:
        number = prefix = ''
        while prefix != '0':
            group, transmission = take_bits(5, transmission)
            prefix, group_number = take_bits(1, group)
            number += group_number
        return Packet(version, type_id, number, None), transmission
    else:
        length_type_id, transmission = take_bits(1, transmission)
        if length_type_id == '0':
            sub_packets_length, transmission = take_bits(15, transmission)
            sub_packets_transmission, transmission = take_bits(int(sub_packets_length, 2), transmission)
            sub_packets = parse_packets(sub_packets_transmission)
            return Packet(version, type_id, None, sub_packets), transmission
        else:
            sub_packets_number, transmission = take_bits(11, transmission)
            sub_packets = []
            for _ in range(int(sub_packets_number, 2)):
                sub_packet, transmission = parse_packet(transmission)
                sub_packets.append(sub_packet)
            return Packet(version, type_id, None, sub_packets), transmission


def parse_packets(transmission):
    packets = []
    while not all(bit == '0' for bit in transmission):
        packet, transmission = parse_packet(transmission)
        packets.append(packet)
    return packets


def read_packets():
    hexadecimal_transmission = read_text()
    binary_transmission = bin(int(hexadecimal_transmission, 16))[2:].zfill(len(hexadecimal_transmission) * 4)
    return parse_packets(binary_transmission)


def sum_packet_versions(packets):
    version_sum = 0
    for packet in packets:
        version_sum += packet.version
        if packet.sub_packets:
            version_sum += sum_packet_versions(packet.sub_packets)
    return version_sum


def get_value(packet):
    if packet.type_id == 0:
        return sum(map(get_value, packet.sub_packets))
    elif packet.type_id == 1:
        return prod(map(get_value, packet.sub_packets))
    elif packet.type_id == 2:
        return min(map(get_value, packet.sub_packets))
    elif packet.type_id == 3:
        return max(map(get_value, packet.sub_packets))
    elif packet.type_id == 4:
        return packet.literal
    elif packet.type_id == 5:
        return 1 if get_value(packet.sub_packets[0]) > get_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 6:
        return 1 if get_value(packet.sub_packets[0]) < get_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 7:
        return 1 if get_value(packet.sub_packets[0]) == get_value(packet.sub_packets[1]) else 0


def part_1():
    packets = read_packets()
    return sum_packet_versions(packets)


def part_2():
    packets = read_packets()
    return get_value(packets[0])


if __name__ == "__main__":
    start = time()
    result_part_1 = part_1()
    end = time()
    print(f'Part 1 ran in {round(end - start, 2)} seconds and the result is {result_part_1}')

    start = time()
    result_part_2 = part_2()
    end = time()
    print(f'Part 2 ran in {round(end - start, 2)} seconds and the result is {result_part_2}')
