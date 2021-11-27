import os
import re
from typing import List

REQUIRED_FIELDS = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")


def read_passports() -> List[dict]:
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    passports = []
    with open(file_path) as f:
        tmp_dict: dict = {}
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


def count_valid_passports(passports):
    counter = 0
    for passport in passports:
        if all(key in passport for key in REQUIRED_FIELDS) and do_passport_respect_rules(passport):
            counter += 1

    return counter


def do_passport_respect_rules(passport: dict) -> bool:
    try:
        byr = int(passport["byr"])
        iyr = int(passport["iyr"])
        eyr = int(passport["eyr"])
        hgt = passport["hgt"]
        hcl = passport["hcl"]
        ecl = passport["ecl"]
        pid = passport["pid"]

        if (byr < 1920 or byr > 2002 or
            iyr < 2010 or iyr > 2020 or
                eyr < 2020 or eyr > 2030):
            return False

        numb = int(hgt[:-2])
        if hgt.endswith("cm"):
            if numb < 150 or numb > 193:
                return False
        else:
            if numb < 59 or numb > 76:
                return False

        if not re.match("^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", hcl):
            return False

        if ecl not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            return False

        if len(pid) != 9:
            return False

    except:
        return False

    return True


print(count_valid_passports(read_passports()))
