import os

REQUIRED_FIELDS = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")


def read_passports():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    passports = []
    with open(file_path) as f:
        tmp_dict = {}
        for line in f:
            line = line.strip()

            if line == "":
                passports.append(tmp_dict)
                tmp_dict = {}
            else:
                parts = line.split(" ")
                for k, v in (part.split(":") for part in parts):
                    tmp_dict[k] = v

        last_passport = tmp_dict
        passports.append(last_passport)

    return passports


def count_valid_passports(passports: [dict]) -> int:
    counter = 0
    for passport in passports:
        if all(key in passport for key in REQUIRED_FIELDS):
            counter += 1

    return counter


print(count_valid_passports(read_passports()))
