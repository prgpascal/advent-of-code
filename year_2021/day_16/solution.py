import os
from functools import reduce
from utils.io import write_output

HEX_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return file.readline().strip()


def binary_to_int(binary):
    return int("".join(str(x) for x in binary), 2)


def hex_to_binary(hex):
    return reduce(lambda acc, x: acc + HEX_TABLE[x], hex, "")


def decode_packet(binary):
    version = binary_to_int(binary[:3])
    type_id = binary_to_int(binary[3:6])
    subpackets = []
    pointer = 6
    value = 0

    if type_id == 4:
        # literal value
        acc = []
        has_next = True
        while has_next:
            sub = binary[pointer : pointer + 5]
            pointer += 5
            acc += sub[1:]
            if sub[0] == "0":
                has_next = False
        value = binary_to_int(acc)
    else:
        # operator
        type = binary_to_int(binary[6:7])
        if type == 0:
            total_bits_length = binary_to_int(binary[7:22])
            start = pointer = 22
            while pointer < start + total_bits_length:
                subpacket = decode_packet(binary[pointer:])
                subpackets.append(subpacket)
                pointer += subpacket["pointer"]
        if type == 1:
            subpackets_number = binary_to_int(binary[7:18])
            pointer = 18
            for _ in range(subpackets_number):
                subpacket = decode_packet(binary[pointer:])
                subpackets.append(subpacket)
                pointer += subpacket["pointer"]

        # compute the value based on subpackets
        if type_id == 0:
            value = reduce(lambda acc, p: acc + p["value"], subpackets, 0)
        elif type_id == 1:
            value = reduce(lambda acc, p: acc * p["value"], subpackets, 1)
        elif type_id == 2:
            value = min(p["value"] for p in subpackets)
        elif type_id == 3:
            value = max(p["value"] for p in subpackets)
        elif type_id == 5:
            value = 1 if subpackets[0]["value"] > subpackets[1]["value"] else 0
        elif type_id == 6:
            value = 1 if subpackets[0]["value"] < subpackets[1]["value"] else 0
        elif type_id == 7:
            value = 1 if subpackets[0]["value"] == subpackets[1]["value"] else 0

    return {
        "version": version,
        "type_id": type_id,
        "subpackets": subpackets,
        "pointer": pointer,
        "value": value,
    }


def sum_packet_versions(packet):
    total = packet["version"]
    for x in packet["subpackets"]:
        total += sum_packet_versions(x)
    return total


def solve_1():
    binary = hex_to_binary(read_input())
    packet = decode_packet(binary)
    return sum_packet_versions(packet)


def solve_2():
    binary = hex_to_binary(read_input())
    packet = decode_packet(binary)
    return packet["value"]


write_output(solve_1(), solve_2())
