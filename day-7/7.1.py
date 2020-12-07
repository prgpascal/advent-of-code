import os
import re


def read_input():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines


def get_outer_bags_for_bag(bag, all_bags, seen):
    if bag in all_bags:
        seen.update(all_bags[bag])
        for b in all_bags[bag]:
            get_outer_bags_for_bag(b, all_bags, seen)
    return seen


def count_inner_bags_for_bag(bag, all_bags):
    counter = 0
    if bag in all_bags:
        for b in all_bags[bag]:
            counter += int(b[0])
            counter += int(b[0]) * count_inner_bags_for_bag(b[1], all_bags)
    return counter


def solve_1(rules):
    items_dict = {}
    for rule in rules:
        outer_bag = " ".join(rule.split()[:2])
        for match in re.finditer(r"\d+\s(\w+\s\w+)\sbag", rule):
            item = match.group(1)
            item_set = items_dict.get(item, set())
            item_set.add(outer_bag)
            items_dict[item] = item_set
    return len(get_outer_bags_for_bag("shiny gold", items_dict, set()))


def solve_2(rules):
    items_dict = {}
    for rule in rules:
        outer_bag = " ".join(rule.split()[:2])
        for match in re.finditer(r"(\d+)\s(\w+\s\w+)\sbag", rule):
            content_tuple = (match.group(1), match.group(2))
            item_set = items_dict.get(outer_bag, set())
            item_set.add(content_tuple)
            items_dict[outer_bag] = item_set
    return count_inner_bags_for_bag("shiny gold", items_dict)


input = read_input()
print(solve_1(input))
print(solve_2(input))
