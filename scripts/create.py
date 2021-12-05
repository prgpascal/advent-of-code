import os
from pathlib import Path
from shutil import copyfile
from os.path import exists
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("year", type=str, help="Selected year")
arg_parser.add_argument("day", type=str, help="Selected day")
args = arg_parser.parse_args()
year = args.year
day = args.day


def create_dir(parent_dir, dir_name):
    directory = os.path.join(parent_dir, dir_name)
    try:
        os.mkdir(directory)
    except OSError:
        pass

    return directory


def create_empty_file(parent_dir, filename):
    file = os.path.join(parent_dir, filename)
    if exists(file):
        print("The file already exists")
    else:
        with open(os.path.join(parent_dir, filename), "w"):
            pass


def generate():
    root_path = Path(os.getcwd())

    year_dir = create_dir(root_path, year)
    day_dir = create_dir(year_dir, f"day-{day}" if len(day) > 1 else f"day-0{day}")

    teplate_input_file = os.path.join(root_path, "utils", "template.py")
    template_output_file = os.path.join(str(day_dir), "solution.py")
    copyfile(teplate_input_file, template_output_file)
    create_empty_file(day_dir, "input.txt")
    create_empty_file(day_dir, "output.txt")

    print("DONE. Good luck!")


if __name__ == "__main__":
    generate()
